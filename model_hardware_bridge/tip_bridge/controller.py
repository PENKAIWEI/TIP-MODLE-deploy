import argparse,json,math,os,signal,threading,time
import numpy as np
from .common import ROOT,FPS,emit,pack,rpc,reset_pose,q34,project,limited,Stable
from .sensors import IO
from .config import CONFIG
from .stream import TACTILE_POLICY

def check_stop():
    if (ROOT/'runs/STOP').exists():raise KeyboardInterrupt

def ready(io,timeout=10):
    end=time.monotonic()+timeout;last='No feedback'
    while time.monotonic()<end:
        check_stop()
        try:return project(io.check(),io.limits,feedback=True)
        except ValueError as e:last=str(e)
        time.sleep(.03)
    raise TimeoutError(last)

def aligned_snapshot(io,timeout=5):
    end=time.monotonic()+timeout
    while True:
        check_stop()
        try:return io.store.snapshot()
        except ValueError:
            if time.monotonic()>end:raise
            time.sleep(.01)

def reset(args,io):
    target=q34(reset_pose());project(target,io.limits)
    current=ready(io);emit('reset_reference',source=reset_pose()['source'],target_rad=target.tolist(),actual_rad=current.tolist(),error_rad=(current-target).tolist())
    if not args.execute:return
    io.enable();previous=current.copy();stage=0;stagger_until=None
    arm_target=current.copy();arm_target[:7]=target[:7];arm_target[17:24]=target[17:24]
    stable=Stable(arm_target,.5);end=time.monotonic()+args.reset_timeout
    while time.monotonic()<end:
        check_stop();actual=project(io.check(prepared=True),io.limits,feedback=True);now=time.monotonic()
        desired=arm_target if stage<2 else target
        previous=limited(desired,previous,io.limits);io.publish(previous)
        if stage==0 and stable.update(actual,now):stage=1;stagger_until=now+1.;emit('reset_arm_arrived')
        if stage==1 and now>=stagger_until:stage=2;stable=Stable(target,4.);emit('reset_hand_stage')
        if stage==2 and io.hands_acked() and stable.update(actual,now):
            emit('reset_complete',actual_rad=actual.tolist(),error_rad=(actual-target).tolist(),stationary_seconds=4.,hand_commands_acknowledged=True,arm_position_verified=True,arm_command_acknowledged=None);return
        time.sleep(1/FPS)
    raise TimeoutError('Reset did not converge with fresh position feedback and current hand acknowledgements')

class Workers:
    def __init__(self,io,current):
        from openpi.fastslow.buffer import ActionBuffer
        self.io=io;self.stop=threading.Event();self.calibrated=threading.Event();self.ready=threading.Event();self.error=None
        self.sequence=0;self.fed=-math.inf;self.updates=0;self.discarded=0;self.threads=[]
        self.last_timing=None
        self.session=rpc('/reset',{'anchors':io.store.anchors})['session_id']
        step=np.tile(np.r_[np.full(7,.02),np.full(10,.025)],2)
        self.buffer=ActionBuffer(34,step,current)
    def fail(self,e):self.error=str(e);self.stop.set()
    def discard(self,stamp,timing):
        self.discarded+=1
        if self.discarded<=3 or self.discarded%10==0:emit('policy_result_discarded',reason='Eight-frame context age exceeded',discarded=self.discarded,observation_age_ms=(time.monotonic()-stamp)*1000,**timing)
    def feed(self):
        try:
            while not self.stop.is_set():
                rows=self.io.store.after(self.sequence)[:512]
                if not rows:self.stop.wait(.005);continue
                r=rpc('/feed',dict(session_id=self.session,frames=rows))
                self.sequence=rows[-1]['sequence'];self.fed=max(self.fed,max(r['timestamp'] for r in rows))
                if r['calibrated']:self.calibrated.set()
        except Exception as e:
            if not self.stop.is_set():self.fail(e)
    def feed_aligned_snapshot(self,last,timeout):
        # Calibration can finish while feed is still draining the four-second
        # reset-stability history. Retain a fresh candidate while feed catches it,
        # then replace it if it ages out; never infer on the expired startup frame.
        started=None;candidate=None
        while not self.stop.is_set():
            now=time.monotonic()
            if started is not None and now-started>=timeout:
                lag=(stamp-self.fed)*1000 if math.isfinite(self.fed) else None
                raise TimeoutError('Tactile feed is behind current camera anchor: '+json.dumps(dict(feed_lag_ms=lag,uploaded_sequence=self.sequence,wait_ms=(now-started)*1000)))
            if candidate is None or now-candidate[2]>CONFIG['camera_max_age_s']:
                candidate=None
                try:images,state,stamp=self.io.store.snapshot()
                except ValueError:
                    self.stop.wait(.01);continue
                if stamp<=last:self.stop.wait(.005);continue
                candidate=(images,state,stamp)
            images,state,stamp=candidate
            now=time.monotonic()
            if started is None:started=now
            if self.fed>=stamp:return images,state,stamp,(now-started)*1000
            # A paused source cannot advance past the camera anchor. Once all
            # locally received packets are ACKed, allow the same causal
            # hold as the server instead of waiting for a nonexistent new packet.
            if self.calibrated.is_set() and math.isfinite(self.fed) and self.fed<=now:
                with self.io.store.lock:uploaded_all=self.sequence>=self.io.store.sequence
                if uploaded_all:
                    self.io.tactile_health()
                    return images,state,stamp,(now-started)*1000
            self.stop.wait(.003)
        return None
    def model(self):
        from openpi.fastslow.buffer import ActionUpdate
        try:
            if not self.calibrated.wait(5):raise TimeoutError('First16 calibrated tactile stream missing')
            last=-math.inf
            while not self.stop.is_set():
                snapshot=self.feed_aligned_snapshot(last,5. if self.updates==0 else .1)
                if snapshot is None:break
                images,state,stamp,feed_wait_ms=snapshot
                selected=time.monotonic()
                request_started=time.monotonic()
                slow=rpc('/slow',body=pack(session=np.asarray(self.session),state=state,timestamp=stamp,**images))
                now=time.monotonic()
                timing=dict(camera_age_at_selection_ms=(selected-stamp)*1000,feed_wait_ms=feed_wait_ms,slow_rpc_ms=(now-request_started)*1000,
                            chunk_id=slow['chunk_id'],slow_server_wall_ms=slow.get('server_wall_ms'),slow_server_queue_ms=slow.get('server_queue_ms'),
                            slow_handler_ms=slow.get('server_handler_ms'),slow_read_ms=slow.get('server_read_ms'),slow_decode_ms=slow.get('server_decode_ms'))
                self.last_timing=timing
                if now-stamp>8/FPS:
                    self.discard(stamp,timing);last=stamp;continue
                fast=rpc('/fast',dict(session_id=self.session,chunk_id=slow['chunk_id'],timestamp=now,executed_steps=0))
                timing.update(fast_rpc_ms=(time.monotonic()-now)*1000,fast_server_wall_ms=fast.get('server_wall_ms'),fast_server_queue_ms=fast.get('server_queue_ms'),
                              fast_handler_ms=fast.get('server_handler_ms'),fast_read_ms=fast.get('server_read_ms'),fast_decode_ms=fast.get('server_decode_ms'))
                if time.monotonic()-stamp>8/FPS:
                    self.discard(stamp,timing);last=stamp;continue
                actions=np.asarray(fast['actions'],float)
                if actions.shape!=(30,34) or not np.isfinite(actions).all():raise ValueError('Invalid model action chunk')
                for row in actions[fast['valid_from']:]:
                    # Saturate only finger predictions at the unchanged native hand limits.
                    for side,start in [('left',7),('right',24)]:
                        row[start:start+10]=np.clip(row[start:start+10],*self.io.limits[side]['hand'])
                    project(row,self.io.limits)
                fast['actions']=actions
                update=ActionUpdate(**{k:fast[k] for k in ActionUpdate.__dataclass_fields__})
                with self.buffer.lock:
                    if not self.buffer.apply(update,time.monotonic()):raise ValueError('Action buffer refused stale model update')
                self.updates+=1;last=stamp;self.ready.set()
                if self.updates==1 or self.updates%30==0:emit('policy_update',updates=self.updates,slow_ms=slow['slow_ms'],fast_ms=fast['fast_ms'],observation_age_ms=(time.monotonic()-stamp)*1000)
        except Exception as e:
            if not self.stop.is_set():self.fail(e)
    def start(self):
        for fn in (self.feed,self.model):
            thread=threading.Thread(target=fn,daemon=True);self.threads.append(thread);thread.start()
    def close(self):
        self.stop.set()
        for t in self.threads:t.join(timeout=3)

def infer(args,io):
    status=rpc('/status')
    if (status.get('schema'),status.get('state_dim'),status.get('physical_action_dim'),status.get('model_action_dim'))!=('sandisk100_dual_o10_v1',46,34,48):raise ValueError('Wrong remote model contract')
    if not status.get('ready') or args.execute and not status.get('live_budget_ok'):raise ValueError('Model warmup did not pass the live latency budget')
    remote_tactile=status.get('tactile_policy',{})
    if any(remote_tactile.get(k)!=TACTILE_POLICY[k] for k in ('sampling','max_sample_age_s','stream_timeout_s','fallback_after_s')):
        raise ValueError('Client/server tactile policy differs; configure both endpoints consistently')
    current=ready(io,CONFIG['startup_timeout_s']);stable=Stable(q34(reset_pose()),4.);end=time.monotonic()+CONFIG['startup_timeout_s']
    while (args.execute and not stable.update(current,time.monotonic())) or len(io.store.anchors)<16:
        check_stop()
        if time.monotonic()>end:raise ValueError('Need first16 camera anchors and (for execution) a stable saved collection reset pose')
        time.sleep(1/FPS);current=project(io.check(),io.limits,feedback=True)
    if not args.execute:emit('shadow_inference',physical_outputs=False,reset_pose_required=False)
    aligned_snapshot(io)
    import gc
    gc.collect();gc.freeze()
    workers=Workers(io,current);workers.start()
    try:
        end=time.monotonic()+7
        while not workers.ready.wait(.03):
            check_stop()
            if workers.error:raise RuntimeError(workers.error)
            if time.monotonic()>end:raise TimeoutError('First inference result missing')
        if args.execute:io.enable()
        start=last_report=time.monotonic();previous=current.copy();sent=0
        while args.duration<=0 or time.monotonic()-start<args.duration:
            check_stop();project(io.check(prepared=args.execute),io.limits,feedback=True);io.tactile_health()
            io.conflicts()
            if workers.error:raise RuntimeError(workers.error)
            with workers.buffer.lock:
                now=time.monotonic()
                if workers.buffer.actions is not None and now>=workers.buffer.observation_time+30/FPS:
                    raise TimeoutError('Model action horizon exhausted: '+json.dumps(dict(updates=workers.updates,discarded=workers.discarded,
                        last_observation_age_ms=(now-workers.buffer.observation_time)*1000,last_timing=workers.last_timing)))
                action=workers.buffer.next_action(now)
            if action is not None:
                previous=limited(action[2],previous,io.limits)
                if args.execute:io.publish(previous)
                sent+=1
            if now-last_report>=1:
                emit('inference_running',execute=args.execute,actions=sent,updates=workers.updates);last_report=now
            time.sleep(1/FPS)
        emit('inference_complete',execute=args.execute,actions=sent,updates=workers.updates,discarded=workers.discarded,elapsed_seconds=time.monotonic()-start)
    finally:
        io.stop();workers.close()

def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['observe','reset','infer'])
    p.add_argument('--execute',action='store_true');p.add_argument('--confirm-motion',action='store_true')
    p.add_argument('--duration',type=float,default=0);p.add_argument('--reset-timeout',type=float,default=60)
    a=p.parse_args();io=None
    if a.execute and (not a.confirm_motion or a.mode=='observe'):p.error('Physical execution requires --execute --confirm-motion on reset/infer')
    if not math.isfinite(a.duration) or a.duration<0 or not math.isfinite(a.reset_timeout) or a.reset_timeout<=0:p.error('Invalid duration')
    import fcntl
    (ROOT/'runs').mkdir(exist_ok=True);lease=(ROOT/'runs/controller.lock').open('w')
    try:fcntl.flock(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise SystemExit('Another controller owns this deployment')
    (ROOT/'runs/STOP').unlink(missing_ok=True)
    signal.signal(signal.SIGTERM,lambda *_:(ROOT/'runs/STOP').touch())
    try:
        io=IO()
        ready(io,CONFIG['startup_timeout_s']);io.conflicts();emit('controller_start',mode=a.mode,execute=a.execute,motion_publishers=False)
        if a.mode=='reset':reset(a,io)
        elif a.mode=='infer':infer(a,io)
        else:
            aligned_snapshot(io)
            end=time.monotonic()+(a.duration or 5)
            while time.monotonic()<end:
                check_stop();q=io.check();images,state,stamp=aligned_snapshot(io,timeout=1)
                emit('observation_ready',state_dim=len(state),q34=q.tolist(),camera_age_ms=(time.monotonic()-stamp)*1000,tactile_events=io.store.sequence);time.sleep(.5)
        return 0
    except KeyboardInterrupt:emit('controller_stopped');return 130
    except Exception as e:emit('controller_blocked',reason=str(e));return 2
    finally:
        if io:io.close()
        lease.close()
if __name__=='__main__':raise SystemExit(main())
