"""ARKS Sharks sonic logo: drone -> riser -> impact + 3-note motif (A-E-A) + shimmer tail. Usage: sting.py OUT TOTAL HIT"""
import sys, numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve
SR=44100; rng=np.random.default_rng(11); out, TOTAL, HIT = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
N=int(TOTAL*SR); L=np.zeros(N); R=np.zeros(N)
lp=lambda x,f: sosfilt(butter(2,f,'low',fs=SR,output='sos'),x); bp=lambda x,a,b: sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
def put(s,t,gl=1,gr=None):
    i=int(t*SR); s=s[:max(0,N-i)]; L[i:i+len(s)]+=s*gl; R[i:i+len(s)]+=s*(gl if gr is None else gr)
def saw(f,n,d=0): t=np.arange(n)/SR; return 2*((f*(1+d)*t+rng.random())%1)-1
note=lambda m: 440*2**((m-69)/12)
t=np.arange(int(HIT*SR))/SR
drone=lp(saw(55,len(t))+saw(55,len(t),.005)+.6*saw(82.4,len(t),-.003),300)*(t/HIT)**1.5*.25
put(drone,0)
rl=min(2.2, max(0.3, HIT-0.05)); n=int(rl*SR); tt=np.arange(n)/SR; nz=rng.normal(0,1,n); r=np.zeros(n)
for i,(a,b) in enumerate(np.linspace([250,800],[2500,8000],8)): s=slice(i*n//8,(i+1)*n//8); r[s]=bp(nz,a,b)[s]
riser=(r*.3+np.sin(2*np.pi*np.cumsum(180*2**(3.2*tt/rl))/SR)*.12)*(tt/rl)**2.2
put(riser,HIT-rl,.8,1)
# impact
n=int(3.2*SR); tt=np.arange(n)/SR; f=30+45*np.exp(-tt/.07)
sub=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt/1.0)
crash=lp(rng.normal(0,1,n),3500)*np.exp(-tt/.4)*.35
put(sub*.95+crash,HIT)
# motif: A3 E4 A4, bright detuned-saw "brass" stabs with octave, 1/8 apart, last one held
for k,(m,ln) in enumerate([(57,.22),(64,.22),(69,1.9)]):
    n=int((ln+.6)*SR); tt=np.arange(n)/SR; e=np.minimum(1,tt/.012)*np.exp(-tt/(0.18 if ln<1 else 0.9))
    s=sum(saw(note(m+o),n,d) for o in (0,12) for d in (-.006,.006))/4
    s=lp(s,3200)*e*.32
    put(s,HIT+.04+k*.25,.85 if k!=1 else 1,1 if k!=1 else .85)
# shimmer tail
n=int(2.5*SR); tt=np.arange(n)/SR; sh=sum(np.sin(2*np.pi*note(m)*tt+rng.random()*6) for m in (81,88,93))*np.minimum(1,tt/.3)*np.exp(-tt/.9)*.035
put(sh,HIT+.5,1,.7); put(sh,HIT+.62,.7,1)
ir=lp(rng.normal(0,1,int(1.8*SR)),5000)*np.exp(-np.arange(int(1.8*SR))/SR/.5)*.035
L=L+fftconvolve(L,ir)[:N]; R=R+fftconvolve(R,ir[::-1].copy())[:N]
fo=np.ones(N); k=int((TOTAL-.8)*SR); fo[k:]=np.linspace(1,0,N-k); L*=fo; R*=fo
st=np.stack([L,R],1); st/=np.abs(st).max()/.89
with wave.open(out,'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
print("sting:",out)
