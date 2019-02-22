import random
p = 2**513 + 83049
g = 2
n = 513

def genkeys(n=n,p=p,g=g):
    sk = random.getrandbits(n)
    pk = pow(g,sk,p)
    return sk, pk

def sign(sk,msg,p=p,g=g):
    return pow(g, (msg - sk) % (p-1), p)

def verify(pk,sig,msg,p=p,g=g):
    return ((sig*pk) % p) == pow(g, msg, p)