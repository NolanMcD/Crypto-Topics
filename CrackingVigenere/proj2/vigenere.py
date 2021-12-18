import string
import sys
import os
import argparse

#
# vigenere.py
#
# last update:
#     aug 2019 -bjr: template 
#     31 aug 2021 -bjr: solution
#

def vigenere_encipher(p,k):
	c = ""
	i = 0
	for pi in p:
		ki = ord(k[i]) - ord('a')
		pi = ord(pi) - ord('a')
		pi = (ki+pi)%26
		c += chr(ord('A')+pi)
		i += 1
		if i>=len(k):
			i = 0
	return c ;

def vigenere_decipher(c,k):
	p = ""
	i = 0
	for ci in c:
		ki = ord(k[i]) - ord('a')
		ci = ord(ci) - ord('A')
		ci = (ci-ki+26)%26
		p += chr(ord('a')+ci)
		i += 1
		if i>=len(k):
			i = 0
	return p ;

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
