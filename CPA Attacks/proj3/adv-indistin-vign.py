#
# Adversarial Indistinguishability Experiment
# CSC507/609 Term 201
#
# Write an adversary with an advantage in the
# indistinguishability game for a vigenere cipher.
# The key is generated according to the distribution
# presented in problem 2.8 of the class text.
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

def vigenere_encipher(p,k):
        """
        p is plaintext over the alphabet a, b, c, ... , z
	c is ciphertext over the alphabet A, B, C, ... , Z
	k is a string over the alphabet, the keyword, e.g. "keyword"
	
        if args_g.verbose:
                print("cycle_enigma_encipher:")
                print("\tplaintext:",p)
                print("\tkey:",k)
        """
        c = ''
        
        ##This might be stupid
        if len(k) == 0:
                k = 'a'
        c = ""
        kord = [ ord(kc)-ord('a') for kc in k ]
        i = 0
        for i in range(len(p)):
                pi = ord(p[i]) - ord('a')
                ki = ord(k[i%len(k)]) - ord('a')
                cn = (pi + ki) % 26 + ord('A')
                c += chr(cn)
        return c

def gen_key(n):
	key_size = random.choice(range(n))
	# 
	# this is not a random key, although random length
	#
	return 'a'* key_size


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
        # replace next line
        if len(c) == len(m0):
                guess = 0
        elif len(c) == len(m1):
                guess = 1
        else:
                guess = 0
        return guess

def adversary_start():
	# adversary chooses a message pair
	return adversary_challenge()


def adversary_sample(m):
        
	# the adversarial indistinguishability experiment
	# a bit is chosen at random
        b = gen_bit()
	#
	# a cipher key is chosen at random
        k = gen_key(10)
	#
	# the cipher is queried with key k and message m[b]
        c = vigenere_encipher(m[b],k)
        # the adversary makes its guess
        #print("M0, m1, c")
        #print(m[0],m[1],c)
        guess = adversary_decision(m[0],m[1],c)
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
	parser = argparse.ArgumentParser(description="The adversary protocol game for a vigenre cipher.")
	parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
	parser.add_argument("-k", "--keyword", help="set keyword and trigger encryption mode")
	parser.add_argument("argument", help="depening on mode, either number of trials or the plaintext to encrypt ")
	
	return parser.parse_args()

def main(argv):
	global args_g
	args_g = parse_args()

	if args_g.keyword == None:
		print (adversary_advantage(int(args_g.argument)))
	else:
		print (vigenere_encipher(args_g.argument, args_g.keyword))


if __name__ == "__main__":
	main(sys.argv)




