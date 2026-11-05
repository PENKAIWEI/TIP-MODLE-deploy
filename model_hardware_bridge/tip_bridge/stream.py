from collections import deque
import math
import numpy as np
from .common import FPS,SHAPES
from .config import CONFIG

TACTILE_FRESH_S = CONFIG['tactile_fallback_after_s']
TACTILE_STREAM_TIMEOUT_S = None if CONFIG['tactile_mode']=='hold' else CONFIG['tactile_strict_timeout_s']
TACTILE_MAX_SAMPLE_AGE_S = None if CONFIG['tactile_mode']=='hold' else CONFIG['tactile_strict_sample_age_s']
TACTILE_POLICY = dict(sampling='latest_causal_packet',max_sample_age_s=TACTILE_MAX_SAMPLE_AGE_S,
                      stream_timeout_s=TACTILE_STREAM_TIMEOUT_S,
                      fallback='hold_last_causal_packet' if CONFIG['tactile_mode']=='hold' else 'stop',fallback_after_s=TACTILE_FRESH_S)

class DualStream:
    """Causal histories that hold the last packet across tactile stream outages."""
    def __init__(self,targets=None):
        self.rows=[deque(maxlen=1000) for _ in range(14)];self.targets=None;self.baseline=None;self.calibration_time=None
        self.hand_age_s=();self.reused_hands=()
        if targets is not None:
            a=np.asarray(targets,float)
            if a.shape!=(16,) or not np.isfinite(a).all() or np.any(np.diff(a)<=0):raise ValueError('Need 16 increasing camera anchors')
            self.targets=a
    def reset(self):self.__init__()
    def update(self,patch,raw,stamp,valid=True):
        if type(patch) is not int or not 0<=patch<14:raise ValueError('Invalid patch')
        raw=np.asarray(raw);stamp=float(stamp)
        if raw.shape!=SHAPES[patch] or not np.isfinite(raw).all() or np.any(raw<0) or np.any(raw>255) or np.any(raw!=np.floor(raw)):raise ValueError('Invalid native mono8 patch')
        rows=self.rows[patch]
        if not math.isfinite(stamp) or rows and stamp<=rows[-1][0]:raise ValueError('Nonincreasing tactile source clock')
        if type(valid) is not bool:raise ValueError('Packet validity must be boolean')
        rows.append((stamp,raw.astype(np.float32).copy(),valid))
        if self.baseline is None and self.targets is not None and all(r and r[-1][0]>=self.targets[-1] for r in self.rows):
            from openpi.vtla.pressure import calibrate_dualhand
            values,valid,_=self.sample(self.targets)
            self.baseline,self.scale,self.baseline_valid=calibrate_dualhand(values.transpose(1,0,2,3),valid.T)
            self.calibration_time=float(self.targets[-1])
    def sample(self,targets):
        values=np.zeros((14,len(targets),14,15),np.float32);valid=np.zeros((14,len(targets)),bool);latest=[]
        # Keep every retained packet. Only the temporary query view is narrowed:
        # one predecessor of the earliest target plus all following packets can
        # answer every causal search, including unsorted/duplicate targets.
        earliest=None
        if len(targets):
            target_array=np.asarray(targets)
            if target_array.ndim==1 and np.isfinite(target_array).all():earliest=min(targets)+1e-9
        for i,rows in enumerate(self.rows):
            query=rows
            if earliest is not None:
                suffix=[]
                for row in reversed(rows):
                    suffix.append(row)
                    if row[0]<=earliest:break
                suffix.reverse();query=suffix
            times=np.asarray([r[0] for r in query]);h,w=SHAPES[i]
            if not len(times):continue
            for j,t in enumerate(targets):
                k=int(np.searchsorted(times,t+1e-9,side='right'))-1
                if k>=0 and query[k][2] and t-times[k]>=-1e-9 and (TACTILE_MAX_SAMPLE_AGE_S is None or t-times[k]<=TACTILE_MAX_SAMPLE_AGE_S+1e-9):
                    values[i,j,:h,:w]=query[k][1];valid[i,j]=True
                    if j==len(targets)-1:latest.append(float(times[k]))
        return values,valid,max(latest) if latest else -math.inf
    def snapshot(self,stamp):
        from openpi.vtla.pressure import dualhand_contact_fields
        stamp=float(stamp)
        if not math.isfinite(stamp) or self.baseline is None or stamp<self.calibration_time-1e-9:raise ValueError('First16 tactile calibration not ready')
        raw,valid,latest=self.sample(stamp+np.arange(-15,1)/FPS)
        fields=dualhand_contact_fields(raw,valid,self.baseline,self.scale,self.baseline_valid)
        causal=[]
        for side in range(2):
            times=[]
            for rows in self.rows[side*7:(side+1)*7]:
                for t,_,_ in reversed(rows):
                    if t<=stamp+1e-9:
                        times.append(t);break
            if not times:raise ValueError('Dual-hand tactile stream has no causal history')
            causal.append(max(times))
        # sample() already repeats the latest causal packet while a hand is
        # silent. Keep its original timestamp and invalid masks without an age
        # cutoff; receiving a new packet naturally ends the hold.
        self.hand_age_s=tuple(stamp-t for t in causal)
        if TACTILE_STREAM_TIMEOUT_S is not None and max(self.hand_age_s)>TACTILE_STREAM_TIMEOUT_S:
            raise ValueError('Tactile stream timed out under strict policy')
        self.reused_hands=tuple(side for side,age in zip(('left','right'),self.hand_age_s) if age>TACTILE_FRESH_S)
        # Invalid packets still establish the stream heartbeat, exactly as in
        # the full-history query, while sample() leaves their values masked.
        return fields,max(causal)
