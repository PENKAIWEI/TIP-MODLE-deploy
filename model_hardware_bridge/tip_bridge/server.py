import argparse,gc,io,json,os,signal,threading,time
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from .common import ROOT,CHECKPOINT,FPS,CAMERAS,token,emit
from .stream import DualStream,TACTILE_POLICY,TACTILE_STREAM_TIMEOUT_S

def main():
    p=argparse.ArgumentParser();p.add_argument('--host',default='0.0.0.0');p.add_argument('--port',type=int,default=18774);a=p.parse_args()
    token()  # Fail before model loading if authentication is not configured.
    import jax
    jax.config.update('jax_compilation_cache_dir',str(ROOT/'jax_cache'))
    from openpi.fastslow.policy import FastSlowPolicy
    from openpi.policies.policy_config import create_trained_policy
    from openpi.training.config import get_config
    from .runtime import install_annotation_check
    install_annotation_check()
    class Policy(FastSlowPolicy):
        def reset(self,targets=None):
            sid=super().reset();self.stream=DualStream(targets);return sid
        def feed(self,sid,frames):
            with self.sensor_lock:
                self._session(sid)
                for f in frames:self.stream.update(f['patch'],f['raw'],f['timestamp'],f.get('valid',True))
        def _touch(self,stamp):
            with self.sensor_lock:return self.stream.snapshot(stamp)
    cfg=get_config('vtla_sandisk100_direct_full')
    metadata=json.loads((__import__('pathlib').Path(CHECKPOINT)/'assets/fastslow.json').read_text())
    if metadata['action_dim']!=48 or metadata['loss_action_dims']!=list(range(34)) or metadata['tactile_layout']!='dualhand_430':raise ValueError('Wrong checkpoint contract')
    # _touch above replaces the generic stream's age check. The only remaining
    # touch timeout is the independent whole-hand stream heartbeat.
    policy=Policy(create_trained_policy(cfg,CHECKPOINT,default_prompt='Pour water.'),fps=FPS,max_delay_frames=8,max_sensor_age_s=TACTILE_STREAM_TIMEOUT_S,seed=43)
    inference=ThreadPoolExecutor(max_workers=1,thread_name_prefix='policy')
    def invoke(function,*args,**kwargs):
        def run():
            start=time.monotonic();value=function(*args,**kwargs)
            value['server_wall_ms']=(time.monotonic()-start)*1000
            return value
        return inference.submit(run).result()
    fixture=dict(np.load(ROOT/'data/replay.npz',allow_pickle=False))
    if not fixture['sample_valid'][:,-1].any():raise ValueError('Warmup fixture has no fresh current tactile patches')
    gc.collect();gc.freeze()
    targets=100.+np.arange(16)/FPS;sid=policy.reset(targets.tolist())
    for j,t in enumerate(targets):
        frames=[]
        for patch,(h,w) in enumerate(__import__('tip_bridge.common',fromlist=['SHAPES']).SHAPES):
            frames.append(dict(patch=patch,raw=fixture['calibration'][j,patch,:h,:w].tolist(),timestamp=float(t),valid=bool(fixture['calibration_valid'][j,patch])))
        policy.feed(sid,frames)
    warm=[]
    for i in range(5):
        anchor=101.+i
        for j in range(16):
            t=anchor+(j-15)/FPS
            if t<=targets[-1] and i==0:continue
            policy.feed(sid,[dict(patch=k,raw=fixture['touch'][k,j,:h,:w].tolist(),timestamp=float(t),valid=bool(fixture['sample_valid'][k,j])) for k,(h,w) in enumerate(__import__('tip_bridge.common',fromlist=['SHAPES']).SHAPES)])
        start=time.monotonic()
        slow=invoke(policy.slow,sid,dict(images={c:fixture['images'][k] for k,c in enumerate(CAMERAS)},state=fixture['state'],camera_valid=np.ones(3,bool),prompt='Pour water.'),anchor)
        fast=invoke(policy.fast,sid,slow['chunk_id'],anchor,0)
        actions=np.asarray(fast['actions']);assert actions.shape==(30,34) and np.isfinite(actions).all()
        row=dict(slow_ms=slow['slow_ms'],fast_ms=fast['fast_ms'],total_ms=(time.monotonic()-start)*1000);warm.append(row);emit('warmup',**row)
        if i==0:gc.collect();gc.freeze()
    policy.reset();gc.collect();gc.freeze()
    status=dict(ready=True,schema='sandisk100_dual_o10_v1',checkpoint=CHECKPOINT,state_dim=46,physical_action_dim=34,model_action_dim=48,
        tactile_layout='dualhand_430',slow_steps=6,fast_steps=4,fps=FPS,max_delay_frames=8,prompt='Pour water.',pid=os.getpid(),warmup=warm,
        tactile_policy=TACTILE_POLICY,live_budget_ok=all(r['total_ms']<8/FPS*1000-15 for r in warm[2:]),robot_control=False)
    (ROOT/'runs/model').mkdir(parents=True,exist_ok=True);(ROOT/'runs/model/status.json').write_text(json.dumps(status,indent=2))
    class Handler(BaseHTTPRequestHandler):
        protocol_version='HTTP/1.1'
        disable_nagle_algorithm=True
        def log_message(self,*args):pass
        def reply(self,code,value):
            body=json.dumps(value,allow_nan=False).encode();self.send_response(code);self.send_header('Content-Length',str(len(body)));self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(body)
        def authorized(self):return self.headers.get('Authorization')=='Bearer '+token()
        def do_GET(self):
            if not self.authorized():return self.reply(401,{'error':'Unauthorized'})
            self.reply(200,status) if self.path=='/status' else self.reply(404,{})
        def do_POST(self):
            if not self.authorized():return self.reply(401,{'error':'Unauthorized'})
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<8*1024*1024:raise ValueError('Invalid request size')
                body=self.rfile.read(size)
                if self.path=='/slow':
                    with np.load(io.BytesIO(body),allow_pickle=False) as f:
                        from PIL import Image
                        images={}
                        for c in CAMERAS:
                            image=f[c]
                            if image.ndim==1 and image.dtype==np.uint8:
                                with Image.open(io.BytesIO(image.tobytes())) as decoded:image=np.asarray(decoded.convert('RGB'))
                            if image.shape!=(224,224,3) or image.dtype!=np.uint8:raise ValueError('Expected three 224 RGB images')
                            images[c]=image
                        value=invoke(policy.slow,str(f['session'].item()),dict(images=images,state=f['state'],camera_valid=np.ones(3,bool),prompt='Pour water.'),float(f['timestamp']))
                else:
                    d=json.loads(body)
                    if self.path=='/reset':
                        with policy.infer_lock,policy.sensor_lock:value={'session_id':policy.reset(d['anchors'])}
                    elif self.path=='/feed':
                        if len(d['frames'])>1024:raise ValueError('Too many frames')
                        policy.feed(d['session_id'],d['frames']);value={'accepted':len(d['frames']),'calibrated':policy.stream.baseline is not None}
                    elif self.path=='/fast':value=invoke(policy.fast,d['session_id'],d['chunk_id'],d['timestamp'],d.get('executed_steps',0))
                    else:raise ValueError('Unknown route')
                self.reply(200,value)
            except Exception as exc:self.reply(400,{'error':type(exc).__name__+': '+str(exc)})
    server=ThreadingHTTPServer((a.host,a.port),Handler);server.daemon_threads=True
    def stop(*_):threading.Thread(target=server.shutdown,daemon=True).start()
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    emit('model_ready',**status)
    try:server.serve_forever(.2)
    finally:server.server_close();inference.shutdown(wait=True)

if __name__=='__main__':main()
