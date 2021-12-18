import string
import sys
import os
import argparse
import math
import numpy as np

#
# letter-utils.py
#
# author:Nolan McDermott
# date: 9/8/21
# last update:
#     30 aug 2021 -bjr: created
#

def freq_count(text):
	# given a string text, all characters are in a-z, return
	# a vector of frequency counts.

        s = string.ascii_lowercase
        v = [0] * len(s)
        for letter in text:
                number = s.find(letter)
                if number == -1:
                        continue
                else:
                        v[number] += 1
        return v


def correlate_freqs(v1,v2,s):
	# return the mathematical correlation of v1 and a shifted version of v2.
	# for shift value s, v1_i is matched with v2_{(i+s)%n} where n is the length of
	# the vectors
	
	# the correlation is defined as the inner product of v1 and the shifted v2, 
	# divided by the length of each of the vectors. 
	
	# code here

        #shift v2 first
        v3 = v2.copy()
        #print(v2)
        for i in range(len(v2)):
                #print("i is %d", i)
                #print(str(v2[i]) + "-->" + str(v2[(i+s)%len(v2)]))
                #print((i+s) % len(v2))
                v2[i] = v3[ (i+s) % (len(v3)) ]
        #print(v2)


                
        #now find corr
        a = np.array(v1)
        b = np.array(v2)
        corr = (np.inner(v1,v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        #corr = np.corrcoef(a,b)[0][1]
        #for i in range(len(v1)):
        #        corr += (v1[i] * v2[i]) / (len(v1) * len(v2))
        
        return corr

def print_count(v, colw):
	the_max = max(v)
	scale = colw/the_max
	for x in v:
		print(x + ": " ,end="")
		for i in range(int(x*scale)):
			print('x',end="")
		print()

def parse_args():
	COLUMN_WIDTH_DEFAULT = 40
	
	parser = argparse.ArgumentParser(description="Calculate and compare letter frequencies")
	parser.add_argument("standard_text", help="file of standard text for fixed distribution")
	parser.add_argument("-s", "--letter_shift", type=int, default=-1, help="shift the distribution")
	parser.add_argument("-c","--column_width", type=int, default=COLUMN_WIDTH_DEFAULT, help="column width for histogram")
	parser.add_argument("-p", "--print_histogram", action="store_true", help="rint histogram")	
	parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
	return parser.parse_args()

def main(argv):
	args_g = parse_args()
	
	## gather test text 
	tt = ""
	for line in sys.stdin:
		for c in line:
			if c.isalpha():
				tt += c.lower()

	if args_g.verbose:
		print("file: " + args_g.standard_text)

	stf = open(args_g.standard_text,'r')
	st = stf.read()

	st_freq = freq_count(st)
	tt_freq = freq_count(tt)
	
	if args_g.print_histogram:
		print_count(tt_freq, colw)
	
	shifts = [args_g.letter_shift]
	if args_g.letter_shift<0 or args_g.letter_shift>=26:
		shifts = range(26)
	for i in shifts:
		c = correlate_freqs(st_freq,tt_freq,i)
		print("shift: %1d, correlation: %1.4f" % (i,c))

main(sys.argv)
