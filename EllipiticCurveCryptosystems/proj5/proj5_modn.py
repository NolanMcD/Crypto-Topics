##
## csc609/507-221 (sept 2021-dec 2021)
##
## implements class ModN for project 5
## 
## student name: Nolan McDermott
## last-update: 11/17/21
##    16 nov 2021: template files
##
##


import random
import math

class ModN:

	@staticmethod
	def extended_gcd(a,b):
		"""
		extended GCD algorithm. recursive.
		returns (d,s,t) where d = s*a+t*b 
		and d = gcd(a,b)
		"""
		assert(
			a>=0 and b>=0 )
		if b==0:
			return (a,1,0)
		(q,r) = divmod(a,b)
		(d,s,t) = ModN.extended_gcd(b,r)
		# gcd(a, b) == gcd(b, r) == s*b + t*r == s*b + t*(a - q*b)
		return (d,t,s-q*t)


	@staticmethod
	def gcd(a,b):
		(d,s,t) = ModN.extended_gcd(a,b)
		return d


	@staticmethod
	def invert(a,n):
		"""
		returns a inverse mod n
		"""
		(d,t,s) = ModN.extended_gcd(a,n)
		assert 1==d
		return t%n


	def isPP(n):
		wrange = math.log(n)/math.log(2)
		wrange = int(wrange)
		result = []
		for i in range(n):
			if(i<=1):
				continue
			exponent = (int)(math.log(n)/math.log(i))
			for j in [exponent-1, exponent, exponent+1]:
				if i ** j == n:
					result.append([i,j])
		return result

	@staticmethod
	def exp_mod(a,b,n):
		"""
		returns a**b mod n
		"""
		
		a = a%n
		if a==0: return 0
		if a==1: return 1
		if b==0: return 1
		if b==1: return a
		assert b>1

		if b%2==1:
			return a * ModN.exp_mod(a,b-1,n)%n
		t = ModN.exp_mod(a,b//2,n)
		return (t*t)%n


	@staticmethod
	def miller_rabin(n,trials=100):
		#print(n)
		
		def st_rep(x):
			s = 0
			t = x
			while t%2==0:
				s += 1
				t //= 2
			return (s,t)
		
		def is_little_fermat(a,p):
                        #return False
			#fix this (add if x | n)
			#print(p)
			if ModN.exp_mod(a,p,p) == a:
				print("p is prime: " , p)
				return False
			if ModN.exp_mod(a,p-1,p) == 1:
				print("p is prime: " , p)
				return False
			return True
                
		def witness_factoring(w,n):
			(f1,s,t) = ModN.extended_gcd(w+1,n)
			(f2,s,t) = ModN.extended_gcd(w-1,n)
			return (f1,f2)

		if n==1:
			print("n is one")
			return (False,(1,1))
		if (n % 2) == 0:
			#print("n is even")
			return (False,(2,n))
		if len(ModN.isPP(n)) > 0:
			print("n is perfect power") 
			return (False, ModN.isPP(n))

		
		s,t = st_rep(n)
		d = n - 1
		counter = 0
		while d % 2 == 0:
			d = d / 2
			counter += 1
		r = counter
		u = d
		for trial in range(trials):
			w = random.randint(2,n-2)
			if not is_little_fermat(w,n):
				if ModN.exp_mod(w,u,n) != 1 and ModN.exp_mod(w,u,n) != -1:
					for i in range(1, r-1): 
						if ModN.exp_mod(w,2 * i * u, n) != -1:
							print("n is miller-rabin")
							return (False, (w,1))
			else:
				return (False, (w,1))
 
			## implement the core of the miller-rabin algorithm
		print("n is prime") 
		return (True,None)


## end of file
