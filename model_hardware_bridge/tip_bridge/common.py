import http.client,io,json,os,threading,time
from pathlib import Path
from urllib.parse import urlsplit
import numpy as np
from .config import ROOT, CONFIG

URL=CONFIG['model_url']
CAMERAS=('top','left_wrist','right_wrist')
PATCHES=('back','palm','thumb/distal','index/distal','middle/distal','ring/distal','pinky/distal')
SHAPES=((11,12),(14,15),(8,2),(9,2),(9,2),(9,2),(9,2))*2
CHECKPOINT=CONFIG['checkpoint']
FPS=29.994
_rpc_local=threading.local()

def emit(event,**fields):print(json.dumps(dict(event=event,monotonic=time.monotonic(),**fields),allow_nan=False),flush=True)
def token():
    path=Path(os.environ.get('TIP_MODEL_TOKEN_FILE',str(ROOT/CONFIG['token_file'])))
    value=path.read_text(encoding='utf-8').strip()
    if not value:raise ValueError('Empty model token file')
    return value
def rpc(route,data=None,body=None,timeout=3):
    headers={'Authorization':'Bearer '+token()}
    if data is not None:body=json.dumps(data,allow_nan=False).encode();headers['Content-Type']='application/json'
    address=urlsplit(URL);key=(address.scheme,address.hostname,address.port)
    connection=getattr(_rpc_local,'connection',None)
    if connection is None or getattr(_rpc_local,'key',None)!=key:
        if connection is not None:connection.close()
        factory=http.client.HTTPSConnection if address.scheme=='https' else http.client.HTTPConnection
        connection=factory(address.hostname,address.port,timeout=timeout)
        _rpc_local.connection=connection;_rpc_local.key=key
    connection.timeout=timeout
    if connection.sock is not None:connection.sock.settimeout(timeout)
    try:
        connection.request('GET' if body is None else 'POST',address.path.rstrip('/')+route,body=body,headers=headers)
        response=connection.getresponse();payload=response.read()
        if response.status!=200:raise RuntimeError(payload.decode())
        return json.loads(payload)
    except Exception as exc:
        connection.close();_rpc_local.connection=None
        # Never replay a possibly accepted POST after an ambiguous connection loss.
        raise RuntimeError(route+': '+str(exc)) from exc
def pack(**fields):
    # Live images already carry the training JPEG encoding; avoid recompressing RGB.
    out=io.BytesIO();np.savez(out,**fields);return out.getvalue()
def reset_pose():return json.loads((ROOT/CONFIG['reset_file']).read_text(encoding='utf-8'))
def q34(pose):
    return np.r_[np.deg2rad(pose['arm_deg']['left']),0.,pose['hand_rad']['left'],
                 np.deg2rad(pose['arm_deg']['right']),0.,pose['hand_rad']['right']]
def vector(value,n):
    a=np.asarray(value,np.float64)
    if a.shape!=(n,) or not np.isfinite(a).all():raise ValueError(f'Expected finite {n}-vector')
    return a

def project(q,limits,*,feedback=False):
    q=vector(q,34).copy()
    if np.max(np.abs(q[[6,23]]))>1e-4:raise ValueError('RM65 padding dimensions must remain zero')
    q[[6,23]]=0.
    for side,start in [('left',0),('right',17)]:
        arm=q[start:start+6];lo,hi=limits[side]['arm']
        tolerance=1e-4 if feedback else 0.
        if np.any(arm<np.asarray(lo)-tolerance) or np.any(arm>np.asarray(hi)+tolerance):raise ValueError(side+' arm joint limit')
        hand=q[start+7:start+17];lo,hi=map(np.asarray,limits[side]['hand'])
        tolerance=.03 if feedback else 0.
        if np.any(hand<lo-tolerance) or np.any(hand>hi+tolerance):raise ValueError(side+' O10 joint limit')
    return q

def limited(target,previous,limits):
    target=project(target,limits);previous=project(previous,limits,feedback=True)
    step=np.tile(np.r_[np.full(6,.02),0.,np.full(10,.025)],2)
    result=previous+np.clip(target-previous,-step,step)
    for side,start in [('left',7),('right',24)]:result[start:start+10]=np.clip(result[start:start+10],*limits[side]['hand'])
    return project(result,limits)

class Stable:
    def __init__(self,target,duration=4.):self.target=vector(target,34);self.duration=duration;self.rows=[]
    def update(self,q,stamp):
        q=vector(q,34)
        if np.max(np.abs(q-self.target))>.05:self.rows=[];return False
        if self.rows and stamp-self.rows[-1][0]>.15:self.rows=[]
        self.rows.append((stamp,q.copy()))
        while len(self.rows)>1 and stamp-self.rows[1][0]>=self.duration:self.rows.pop(0)
        return len(self.rows)>1 and stamp-self.rows[0][0]>=self.duration and np.ptp(np.stack([r[1] for r in self.rows]),axis=0).max()<.01
