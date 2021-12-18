##
## csc609/507-221 (sept 2021-dec 2021)
##
## test program for project 5
##
## burton rosenberg
## university of miami
## last-update:
##    16 nov 2021
##
##

from proj5_modn import ModN
from proj5_ec import EC, EC_ElGamal

def basic_tests(): 

	def list_primes(low, high, trials=100):
		pr_a = []
		for j in range(low,high):
			if ModN.miller_rabin(j,trials)[0]:
				pr_a += [j]
		print(pr_a)
		return pr_a


	def test_miller_rabin():
		p104087_104729 = [104087, 104089, 104107, 104113, 104119, 104123, 104147, 104149, 104161, 104173, 104179, 104183, 104207, 104231, 104233, 104239, 104243, 104281, 104287, 104297, 104309, 104311, 104323, 104327, 104347, 104369, 104381, 104383, 104393, 104399, 104417, 104459, 104471, 104473, 104479, 104491, 104513, 104527, 104537, 104543, 104549, 104551, 104561, 104579, 104593, 104597, 104623, 104639, 104651, 104659, 104677, 104681, 104683, 104693, 104701, 104707, 104711, 104717, 104723, 104729]
		carmichael_numbers = [561, 41041, 825265, 321197185, 5394826801, 232250619601, 9746347772161, 1436697831295441, 60977817398996785, 7156857700403137441, 1791562810662585767521, 87674969936234821377601, 6553130926752006031481761, 1590231231043178376951698401]
		super_carmichael_numbers = [41041, 62745, 63973, 75361, 101101, 126217, 172081, 188461, 278545, 340561, 449065, 552721, 656601, 658801, 670033, 748657, 838201, 852841, 997633, 1033669, 1082809, 1569457, 1773289, 2100901, 2113921, 2433601, 2455921]

		t = list_primes(104087,104730)
		if t!=p104087_104729: return False
		for pr in carmichael_numbers:
			if ModN.miller_rabin(pr)[0]:
				return False
		for pr in super_carmichael_numbers:
			if ModN.miller_rabin(pr)[0]:
				return False

		return True


	def example_8_69_ed2():
		"""
		example 8.69 in 2nd edition Katz and Lindal
		"""
		ec = EC(7,3,3)
		p1 = (1,0,1)
		p2 = (4,3,1)
		q2 = p2
		p3 = ec.add(p1,p2)
		p4 = ec.add(p3,q2)
		p3p = ec.add(p2,q2)
		p4p = ec.add(p1,p3p)
		return p3==(3,5,1) and p4==(4,4,1) and p3p==(3,2,1) and p4p==(4,4,1)


	test_ec = [ (EC(7,0,2),9), (EC(7,3,3),6), (EC(23,1,0),24), (EC(79,1,1),86), (EC(79,3,1),81), (EC(79,37,23),72), (EC(79,2,5),71)	 ]

	def test_ec_orders():
		for ec in test_ec:
			#print(ec.profile_orbits())
			if ec[0].group_order()!=ec[1]:
				return False
			return True


	def test_encryption():
		ec = EC(79,2,5)
		eg = EC_ElGamal(ec)


		# create generators automatically
		eg.get_generator()
		# create secret key and public key
		eg.gen_keys()

		# encrypt a message
		m = 3
		c = eg.encrypt(m,verbose=True)
		# not every message can be encrypted
		assert c!= None

		m_o = eg.decrypt(c)

		return m_o==m


# -----------------
	
	passed_all = True
	#"""
	if test_miller_rabin():
		print('passes test_miller_rabin')
	else:
		passed_all = False
		print('fails test_miller_rabin')

	if example_8_69_ed2():
		print('passes example_8_69_ed2')
	else:
		passed_all = False
		print('fails example_8_69_ed2')
	#"""
	if test_ec_orders():
		print('passes test_ec_orders')
	else:
		passed_all = False
		print('fails test_ec_orders')

	if test_encryption():
		print('passes test_encryption')
	else:
		passed_all = False
		print('fails ttest_encryption')

	if not passed_all:
		print('not all tests passed')
	return passed_all

basic_tests()
