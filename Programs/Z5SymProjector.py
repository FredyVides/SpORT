"""
Created on Fri Jul 15 20:40:07 2022
K4-symmetric projector
@author: doctor
"""

def Z5SymProjector(data,solver,L,S,ss,tp,nz,g1,G1,tol,delta):
    from numpy import reshape, identity, kron, diag, zeros
    from scipy.linalg import svd
    from RCDataGen import RCDataGen
    from spsolver import spsolver
    
    s = data.shape
    sL = s[0]*L
    R = s[1]-L+1
    
    D,r = RCDataGen(data,L,S,ss,tp)
    D0 = D[:,:-1]
    D1 = D[:sL,1:]
    
    ri = r.T@diag(1/diag(r@r.T))
    K = r@G1@ri
    n = (sL,D.shape[0])
    m = n[0]*n[1]
    n1 = (sL,D0.shape[1])
    m1 = n1[0]*n1[1]
    E = identity(m)
    K = kron(K,g1)-E
    K = K.T@K
    u,rk,_ = svd(K,full_matrices=0)
    rk = sum(rk>1e-10)
    u = u[:,rk:]
    us = u.shape[1]
    W0 = zeros((m1,us))
    for j in range(us):
        w0 = reshape(u[:,j],(n[1],n[0])).T
        w0 = w0@D0
        W0[:,j] = reshape(w0, (m1))
    W1 = reshape(D1, (m1,1))
    c = spsolver(W0,W1,R,solver,nz,tol,delta)
    wr = reshape(u@c,(n[1],n[0])).T
    return wr,D,r