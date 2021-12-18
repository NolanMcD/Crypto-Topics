##
## csc609/507-221 (sept 2021-dec 2021)
##
## implements class EC and EC_ElGamal for project 5
## 
## student name: Nolan McDermott
## last-update:
##    16 nov 2021: template files
##
##


import random 
from proj5_modn import ModN

class EC:
	
	def __init__(self,p,A,B):
		self.A = A
		self.B = B
		self.p = p

		assert p>=5
		assert p%4==3, 'do not make square roots difficult'
		assert (4*A**3+27*B**2)%p != 0	 # non-degenerate


	def zero(self):
		return (0,1,0)


	def is_zero(self,x):
		return x==self.zero()
	
	def is_point(self,x):
		if type(x)!=tuple or len(x)!=3:
			return False
		if x[2]!=0 and x[2]!=1:
			return False
		y2 = self.eval_poly_aux(x[0])
		if x==(0,1,0):
			return True
		return (x[1]*x[1]%self.p)==y2	 


	def is_quad_residue(self,a):
		return ModN.exp_mod(a,(self.p-1)//2,self.p)==1


	def sqroot_3mod4(self,x):
		if self.is_quad_residue(x):
## implement the square root for primes 3 mod 4
                        if (x % 4) == 3:
                                sqrtx = x**((x+1)/4) % self.p
                                return sqrtx
                        else:
                                return None
			

		return None


	def eval_poly_aux(self,x):
		y2 = (x*x+self.A)%self.p
		return (x*y2+self.B)%self.p
		
	def eval_poly(self,x):
		x = x%self.p
		y2 = self.eval_poly_aux(x)
		if y2==0:
			return (0,0)
		y = self.sqroot_3mod4(y2)
		if y!=None:
			return (y,-y%self.p)
		return None


	def add(self,p1,p2):
		assert self.is_point(p1) and self.is_point(p2)
		print("point1: ", p1)
		print("point2: ", p2)
		res = self.zero()
		X, Y, Z = 0, 1, 2
		m = ( (p2[Y] - p1[Y]) / (p2[X] - p1[X]) ) % self.p
		if p1[X] != p2[X]:
			x3 = (m**2 - p1[X] - p2[X] % self.p)
			y3 = (m * (p1[X] - x3) - p1[Y] % self.p)
		if p1[X] == p2[X] and p1[Y] != p2[Y]:
			return res
		if p1 == p2 and p1[Y] == 0:
			return res
		if p1 == p2 and p1[Y] != 0:
			m = ( ((3 * p1[X])**2 + self.A) / (2 * p1[Y])) # + A?
			x3 = (m**2 - 2 * p1[X] % self.p)
			y3 = (m * (p1[X] - x3) - p1[Y] % self.p)
		newpoint = (x3, y3, 1)
                ## implement add, see textbook for formulas
		print(newpoint)
		assert self.is_point(newpoint)
		return newpoint


	def negative(self,pt):
		X, Y, Z = 0, 1, 2
		print("pt: ", pt)
		

## implement point -pt from pt 

		return self.zero()


	def gen_all_points(self):
		points = [(0,1,0)]
		for x in range(self.p):
			y = self.eval_poly(x)
			if y!=None:
				if y[0]==0:
					points += [(x,0,1)]
				else:
					points += [(x,y[0],1),(x,y[1],1)]
					
		assert all(map((lambda x: self.is_point), points))
		return points
	
	def group_order(self):
		return len(self.gen_all_points())
	def gen_orbit(self,p):
		p_tot = self.zero()
		i = 0
		orb = []
		while True:
			## implement adding p successively to p_tot
			#p_tot = self.zero()
			p_list = list(p_tot)
			p_list.append(p)
			p_tot = tuple(p_list)
			orb += [p_tot]
			if self.is_zero(p_tot):
				break
		return orb
	def profile_orbits(self):
		orb = {}
		pts =self.gen_all_points()
		for p in pts:
			o = self.gen_orbit(p)
			if len(o) in orb:
				orb[len(o)] += [p]
			else:
				orb[len(o)] = [p]
		return orb

	def n_add(self,n,pt):
		if self.is_zero(pt) or n==0:
			return self.zero()
		if n<0:
                        n = -n
                        pt = self.negative(pt)
		if n>0:
			return n * pt
                ## calculate n * pt (n>0)
		return self.zero()



class EC_ElGamal:
	
	miller_rabin_trials = 100

	def __init__(self,elliptic_curve, generator=None):
		self.ec = elliptic_curve
		self.g = generator
		self.n = None
		self.ec_n = None
		self.s = None
		self.public = None


	def set_generator(self,generator, group_size):
		self.g = generator
		self.n = group_size


	def get_generator(self):
		if self.g==None:
			(self.g, self.n) = self.suggest_generator()
		return (self.g, self.n)		  


	def get_order_group(self):
		if self.ec_n == None:
			self.ec_n = len(self.ec.gen_all_points())
		return self.ec_n


	def get_order_subgroup(self):
		(g,n) = self.get_generator()
		return n


	def get_public_key(self):
		self.get_secret_key()
		return self.public


	def get_secret_key(self):
		if self.s==None:
			self.gen_keys()
		return self.s


	def suggest_generator(self, verbose=False):
		orbits = self.ec.profile_orbits()
		gen = self.ec.zero()
		grp_size = 0

## implement: find the largest key in the orbits dictionary
## that is prime, and take the first element for the value associated
## with that key as the generator; also set grp_size

		self.g = gen
		self.n = grp_size
		max = 0
		for i in orbits:
			if i > max and modn.miller_rabin(i):
				gen = i
				grp_size += 1
		return(gen,grp_size)


	def gen_keys(self):
		self.get_generator()
		self.s = random.randint(2,self.n-2)
		self.public = self.ec.n_add(self.s,self.g)


	def encode(self, an_integer):
		m = an_integer%self.ec.p
		p = self.ec.eval_poly(m)
		if p==None:
			# don't really worry about failed encodings.
			# some messages just won't be
			return None
		return (m,p[0],1)


	def decode(self, a_point):
		return a_point[0]


	def encrypt(self,m, verbose=False):
		assert self.public
		p = self.encode(m)
		if p==None:
			return None
		E = self.ec
		p = self.ec.p
		# choose k randomly like s
		s = self.s
		P = self.public
		#E[s](m) = (P, s + m)
		#return (E[P], E[s + m])
		kp = n_add(k * P)
		sp = n_add(s * P)
		c = n_add(k * sp)
		return (kp, add(p, c))

## write the encryption code

		return (self.ec.zero(), self.ec.zero())


	def decrypt(self,c,verbose=False):
		assert self.public
		D = self.ec
		p = self.ec.p
		s = self.s
		P = self.public
		
		

## write the decryption code

		return self.ex.zero()

class PH:
	def __init__(self,elliptic_curve, p, n, fact):
		self.ec = elliptic_curve
		self.p = p
		self.n = n
		self.fact = fact
	
	def ph_solve(Q):
		rem = []
		return None

	def ph_solve_plus(Q):
		return None 


## end of file
