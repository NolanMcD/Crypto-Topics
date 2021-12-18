#
# template author: bjr
# template date: 9 sept 2019


# please enter name and date:
# student name: Nolan McDermott
# date (last update): 10/5/2021

import argparse
import sys
import random

### Encipherment and key generator functions

def cycle_enigma_encipher(p,k):
        """
	k is a list giving the permutation, e.g. [0,2,1]
	p is plaintext over an alphabet a, b, c, .. up to len(k) characters
	c is ciphertext over same alphabet but capital letters, A, B, C, ...

	"""
        if args_g.verbose:
                print("cycle_enigma_encipher:")
                print("\tplaintext:",p)
                print("\tkey:",k)
        c = ''
        for i in range(len(p)):
                pi = ord(p[i]) - ord('a')
                ki = k[i%len(k)]
                cn = (pi + ki) % len(k) + ord('A')
                c += chr(cn)
        return c ;

def gen_key(n):
#
#	generate a random key and return
#
	return [i for i in range(n)]  # a boring non-random key

def encode_alpha_key(k):
	return 	[ ord(kc)-ord('a') for kc in k ]

### Adversary functions

def gen_bit():
	return random.choice([0,1])


def adversary_challenge():
	# adversary chooses a message pair
	#
# replace next line
	m0 = 'helloworld'
# replace next line
	m1 = 'aaaaa'
	#
	return (m0,m1)


def adversary_decision(m0,m1,c):
	# adversary takes the encryption c of
	# either m0 or m1 and returns a best
	# guess of which message was encrypted
	#
	# This code is highly dependent on the
	# cipher used. It is the heart of the crack.
	#
        guess = 0
        #print("C is " + c)
        if len(c) == len(m0):
                guess = 0
        elif len(m1) == len(c):
                guess = 1
        return guess


def adversary_start():
	# adversary chooses a message pair
	return adversary_challenge()


def adversary_sample(m):
	# the adversarial indistinguishability experiment
	# a bit is chosen at random
# replace next line
	b = gen_bit()
	#
	# a cipher key is chosen at random
# replace next line
	k = gen_key(10)
	#
	# the cipher is queried with key k and message m[b]
# replace next line
	c = cycle_enigma_encipher(m[b],k)
	#
	# the adversary makes its guess
# replace next line
	guess = adversary_decision(m[0],m[1],c)
	#
	return b==guess


def adversary_advantage(trials):

	if args_g.verbose:
		print("number trials:", trials)

	m = adversary_start()
	count = 0 
	for i in range(trials):
		if adversary_sample(m):
			count += 1
	return (count+0.0)/(trials+0.0)

# main

def parse_args():
	parser = argparse.ArgumentParser(description="The adversary protocol game for a enigma-type cipher.")
	parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
	parser.add_argument("-k", "--keyword", help="set keyword and trigger encryption mode")
	parser.add_argument("argument", help="depening on mode, either number of trials or the plaintext to encrypt ")
	
	return parser.parse_args()

#
# the keyword given in the -k argument is a list of lower letter characters, for instance bcdefgha,
# with the following rules: 
#    1. A letter appears at most once
#    2. The letter a appears
#    3. If two letters appear then all the letters between those two letters in the alphabet apear.
#    4. If a letter does not appear in the keyword it must not appear in the plaintext
#
# turn the keyword into a list of numbers and this becomes the lookup array for the permutation (also called the key
# to the encryption). read the code of encode_alpha_key to make this clear.

def main(argv):
	global args_g
	args_g = parse_args()

	if args_g.keyword == None:
		print (adversary_advantage(int(args_g.argument)))
	else:
		print (cycle_enigma_encipher(args_g.argument, encode_alpha_key(args_g.keyword)))



if __name__ == "__main__":
	main(sys.argv)

