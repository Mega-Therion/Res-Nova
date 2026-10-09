import numpy as np
rng=np.random.default_rng(11)
def run(k, N=6000, nper=10, dt=2.5e-4, emax=0.9, every=800):
    e=np.minimum(np.sqrt(rng.random(N)),emax); M=rng.random(N)*2*np.pi; E=M.copy()
    for _ in range(40): E-=(E-e*np.sin(E)-M)/(1-e*np.cos(E))
    den=1-e*np.cos(E)
    pos=np.stack([np.cos(E)-e,np.sqrt(1-e**2)*np.sin(E),0*E],-1)
    vel=np.stack([-np.sin(E)/den,np.sqrt(1-e**2)*np.cos(E)/den,0*E],-1)
    q=rng.normal(size=(N,4)); q/=np.linalg.norm(q,axis=1)[:,None]; w,x,y,z=q.T
    R=np.stack([np.stack([1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y)],-1),
                np.stack([2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x)],-1),
                np.stack([2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)],-1)],1)
    r=np.einsum('nij,nj->ni',R,pos); v=np.einsum('nij,nj->ni',R,vel)
    def phi(r):
        rr=np.linalg.norm(r,axis=1); return -(1/rr)*(1+(k/2)*(r[:,0]**2+r[:,1]**2)/rr**2)
    def acc(r):
        rr=np.linalg.norm(r,axis=1)[:,None]; xy2=(r[:,0]**2+r[:,1]**2)[:,None]
        return -r/rr**3 + (k/2)*(np.concatenate([2*r[:,:2],0*r[:,2:]],1)/rr**3 - 3*xy2*r/rr**5)
    E0=0.5*np.sum(v*v,1)+phi(r); drift=np.zeros(N); rmin=np.full(N,9.)
    nsteps=int(nper*2*np.pi/dt); burn=int(2*2*np.pi/dt)
    a=acc(r); RO=[];VO=[]
    for i in range(nsteps):
        v+=0.5*dt*a; r+=dt*v; a=acc(r); v+=0.5*dt*a
        if i%every==0:
            En=0.5*np.sum(v*v,1)+phi(r); drift=np.maximum(drift,np.abs(En/E0-1))
            if i>burn: RO.append(r.copy()); VO.append(v.copy())
    good=drift<1e-2
    return np.stack(RO,1)[good], np.stack(VO,1)[good], good.mean()
for k in (0.0,-0.1878):
    R3,V3,fg=run(k); No,Ns=R3.shape[:2]
    r=R3.reshape(-1,3); v=V3.reshape(-1,3); n=len(r)
    rr=np.linalg.norm(r,axis=1); cth=np.abs(r[:,2])/rr; v2r=np.sum(v*v,1)*rr
    al=cth>0.8; pe=cth<0.2
    nh=rng.normal(size=(n,3)); nh/=np.linalg.norm(nh,axis=1)[:,None]
    rs=r-np.sum(r*nh,1)[:,None]*nh; vs=v-np.sum(v*nh,1)[:,None]*nh; gs=np.array([0,0,1.0])-nh[:,2:3]*nh
    s=np.linalg.norm(rs,axis=1); vt=np.linalg.norm(vs,axis=1)*np.sqrt(s)
    cpsi=np.abs(np.sum(rs*gs,1))/(s*np.linalg.norm(gs,axis=1)+1e-30)
    A=cpsi>np.sqrt(0.5)
    print(f"k={k:+.4f} kept orbits {fg*100:.1f}% ({No}), snapshots {n}")
    print(f"  3D: median v^2 r ratio |cos th|>0.8 vs <0.2 = {np.median(v2r[al])/np.median(v2r[pe]):.4f}; mean ratio = {v2r[al].mean()/v2r[pe].mean():.4f}  (ergodic 1/(1+k/2) = {1/(1+k/2):.4f})")
    print(f"  sky, all snapshots: median v~ aligned/perp - 1 = {np.median(vt[A])/np.median(vt[~A])-1:+.4f}  (|cos psi| split at 1/sqrt2)")
    # independent: one snapshot per orbit, many observer draws -> bootstrap over orbits for the error of the effect
    eff=[]
    for b in range(200):
        idx=rng.integers(0,No,No); j=rng.integers(0,Ns,No)
        rb=R3[idx,j]; vb=V3[idx,j]
        nb=rng.normal(size=(No,3)); nb/=np.linalg.norm(nb,axis=1)[:,None]
        rsb=rb-np.sum(rb*nb,1)[:,None]*nb; vsb=vb-np.sum(vb*nb,1)[:,None]*nb; gsb=np.array([0,0,1.0])-nb[:,2:3]*nb
        sb=np.linalg.norm(rsb,axis=1); vtb=np.linalg.norm(vsb,axis=1)*np.sqrt(sb)
        cb=np.abs(np.sum(rsb*gsb,1))/(sb*np.linalg.norm(gsb,axis=1)+1e-30); Ab=cb>np.sqrt(0.5)
        eff.append(np.median(vtb[Ab])/np.median(vtb[~Ab])-1)
    print(f"  sky, 1 snapshot/orbit bootstrap: effect {np.mean(eff):+.4f} +- {np.std(eff):.4f} (N={No} orbits)")
