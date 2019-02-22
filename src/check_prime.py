# Python program to check if the input number is prime or not
import random



def check(p):
	if p > 1:
		return miller_rabin(p, 40)
	else:
		return False

def find_prime(bits, start=1, end=20):
	q = 2**bits
	for i in range(2**start+1, 2**end, 2):
		n = q - i
		if check(n):
			if check_safe(n):
				print(i, "found prime")
				return n
			else:
				print(i, "unsafe prime")

	return None

def find_next_safe_prime(start, s=1, e=20):
	for i in range(0, 2**e, 2):
		p = start + i
		if check(p):
			if check(2*p + 1):
				print(i, "safe")
				return p
			else:
				print(i, "unsafe")
	return None

def check_safe(p):
	n = (p-1)/2
	return check(n)

def miller_rabin(n, k):
	# Primality test courtesy of Ayrx on Github:
	# https://gist.github.com/Ayrx/5884790
	# Implementation uses the Miller-Rabin Primality Test
	# The optimal number of rounds for this test is 40
	# See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
	# for justification

	# If number is even, it's a composite number

	if n == 2:
		return True

	if n % 2 == 0:
		return False

	r, s = 0, n - 1
	while s % 2 == 0:
		r += 1
		s //= 2
	for _ in range(k):
		a = random.randrange(2, n - 1)
		x = pow(a, s, n)
		if x == 1 or x == n - 1:
			continue
		for _ in range(r - 1):
			x = pow(x, 2, n)
			if x == n - 1:
				break
		else:
			return False
	return True

q = 2**513 - 1
#qq = find_next_safe_prime(q)

#print(check(qq))
#print(check(2*qq + 1))
qq = 2**513 + 83049
print(check(qq))
print(check(2*qq+1))
