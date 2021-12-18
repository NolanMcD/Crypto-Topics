import string
import sys
import os
import argparse

#
# vigenere.py
#
# author: Nolan McDermott
# date: 8/28/21
# last update: 8/29/21
# template by: bjr aug 2019
#

def vigenere_encipher(p,k):
        
	# given a string p of all lowercase letters, 
	# and a key k of all lowercase letters,
	# return a string of all uppercase letters,
	# which is the vigenere encryption of p by key k.
	
        c = ""
        i = 0
        for i in range(len(p)):
                pi = ord(p[i]) - ord('a')
                ki = ord(k[i%len(k)]) - ord('a')
                cn = (pi + ki) % 26 + ord('A')
                c += chr(cn)
        return c

def vigenere_decipher(c,k):
	# given a string c of all uppercase letters, 
	# and a key k of all lowercase letters,
	# return a string of all lowercase letters,
	# which is the vigenere decryption of c by key k.

	p = ""
	i = 0
	for i in range(len(c)):
                ei = ord(c[i]) - ord('A')
                ki = ord(k[i%len(k)]) - ord('a')
                pn = (ei - ki + 26) % 26 + ord('a')
                p += chr(pn)
	return p

def parse_args():
	parser = argparse.ArgumentParser(description="Encrypt/decrypt stdin by a vigenere cipher. Ignores any character other than alphabetic.")
	parser.add_argument("key", help="encipherment key")
	parser.add_argument("-d", "--decrypt", action="store_true", help="decrypt, instead of encrypting")
	parser.add_argument("-g", "--word_group", type=int, default=5, help="characters per word group")
	parser.add_argument("-G", "--line_group", type=int, default=5, help="word groups per line")
	parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
	return parser.parse_args()

def main(argv):

	args_g = parse_args()

	## gather plain text and format
	t_in = ""
	for line in sys.stdin:
		for c in line:
			if c.isalpha():
				if not args_g.decrypt:
					c = c.lower()
				else:
					c = c.upper()
				t_in += c

	## encrypt/decrypt
	if args_g.decrypt:
		t_out = vigenere_decipher(t_in,args_g.key)
	else:
		t_out = vigenere_encipher(t_in,args_g.key)

	## pretty print ct
	i = 0
	s = ""
	r = args_g.word_group * args_g.line_group

	for c in t_out:
		s += c
		i += 1
		if i%args_g.word_group==0:
			s += ' '
		if i%r==0:
			s += '\n'
	print (s)
	

main(sys.argv)
