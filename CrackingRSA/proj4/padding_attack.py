import string
import sys
import os
import argparse

from padding_oracle import Padding_Oracle

#
# padding-attack.py
#
# author: Nolan McDermott
# date: 10/27/21
# last update:
#               04 nov 2021 -nim: attacked
#		22 oct 2019 -bjr: csc507-201
#		10 oct 2021 -bjr: updated for csc507-221
#		15 oct 2021 -bjr: added a comment
#		

# this is where most of your work should go.
# changing padding_oracle, if needed, is not wrong, but my
# intent was you would implement the attack inside the attack_mode
# def, or with added def's here in this file (just to things simple
# for me, when grading)


args_g = 0  # args are global

def attack_mode(oracle,intext):
        #print(oracle.padding_oracle(intext))
        print("Intext is: ")
        sys.stdout.buffer.write(intext)
        print('\n')
        block_size = oracle.get_block_size()
        print("Block size is: " + str(block_size))
        outtext = []
        for back in range(block_size, 0, -1):
                for x in range(256):
                        intext[back] = x
                        if oracle.padding_oracle(intext) == False:
                                print("Padding is incorrect")
                        else:
                                print("Padding is correct")
                                print("x is " + str(x))
                                outtext.append(x)
        
        #read the wiki
        print('\n')
        for x in intext:
                if x != 255:
                        print(x)
        print(outtext)
        print("ATTACK FINISHED")
        
        

def encrypt_mode(oracle,intext):
	outtext = oracle.encrypt(intext)
	sys.stdout.buffer.write(outtext)
	
def decrypt_mode(oracle,intext):
	outtext = oracle.decrypt(intext)
	sys.stdout.buffer.write(outtext)


# first one on the list is the default
modes = ["encrypt","decrypt","attack"]
# callout table
modes_f = { "encrypt":encrypt_mode, "decrypt":decrypt_mode, "attack":attack_mode}


def parse_args():
	parser = argparse.ArgumentParser(description="Padding attack against ciphertext from stdin. ")
	parser.add_argument("key", help="encipherment key")
	parser.add_argument("-m", "--mode", help="mode either encrypt, decrypt, or attack")	
	parser.add_argument("-R", "--norandomness", action="store_true", help="set IV to zero")	
	parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
	parser.add_argument("-z", "--zero", action="store_true", help="use zeros padding on encrypt, do not remove padding on decrypt")	
	return parser.parse_args()

def main(argv):

	global args_g
	args_g = parse_args()
	if args_g.mode not in modes:
		args_g.mode = modes[0]
	
	padding_oracle = Padding_Oracle(args_g.key, zero_padding=args_g.zero, 
		norandomness=args_g.norandomness)
	bintext = bytearray(sys.stdin.buffer.read())
	modes_f[args_g.mode](padding_oracle,bintext)


main(sys.argv)
