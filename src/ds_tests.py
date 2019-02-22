from keys import *
import hashlib
import time

def main():
    unit1()
    unit2()
    unit3()

def unit1():
    start = time.time()
    m = hashlib.sha256()
    m.update(b"Here is my message!")
    pk, sk = genkeys()
    m = int(m.hexdigest(), 16)
    sig = sign(sk, m)
    print(verify(pk, sig, m))
    end = time.time()
    print(end - start, 'seconds')


def unit2():
    start = time.time()
    for i in range(1000):
        genkeys()

    end = time.time()
    print(end - start, 'seconds')

def unit3():
    pk, sk = genkeys()
    m = random.getrandbits(8000)
    start = time.time()
    for i in range(1000):
        sig = sign(sk, m)
        verify(pk, sig, m)
    end = time.time()
    print(end - start, 'seconds')


main()
