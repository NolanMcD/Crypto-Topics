import string
import sys
import os
import argparse
import random

from bohzu_aes import AES

#
# padding oracle for project 4,
# csc609/507-201
# csc609/507-221
#
# author: burt
# date: 21 oct 2019
# last update: 
#		21 oct 2019 -bjr: created
#		10 oct 2021 -bjr: key is required, -R is for the IV only
#		15 oct 2021 -bjr: added get_block_size method
#

# this mostly should be good, with no major changes needed.
# you can change things but I was thinking that most of your
# work would be in the padding-attack.py file

class Padding_Oracle:

	BlockSize = 16

	def __init__(self,key,zero_padding=False,norandomness=False):

		# combination pad or truncate
		self.key = (bytes(key,encoding="utf-8")
				+bytes(self.BlockSize))[:self.BlockSize]  
		self.aes = AES(self.key)
		self.zero_padding = zero_padding
		self.norandomness = norandomness

	def print_key(self):
		print(self.key)

	@staticmethod
	def print_bytearray(ba):
		print(''.join('{:02x} '.format(x) for x in ba))
		
	def get_block_size(self):
		return self.BlockSize

	# ENCRYPTION

	def get_initial_vector(self):
		iv = bytearray(self.BlockSize)
		if self.norandomness:
			return iv
		for i in range(self.BlockSize):
			iv[i] = random.randint(0,255)
		return iv

	def encrypt_xor(self,ciphertext,plaintext,location):
		buf = bytearray(self.BlockSize)
		for i in range(self.BlockSize):
			buf[i] = plaintext[location+i] ^ ciphertext[location+i]
		return buf

	def encrypt(self,intext_ba):
		assert isinstance(intext_ba,bytearray),"encrypt parameter not a bytearray"

		# pad up
		pad_len = self.BlockSize - (len(intext_ba)%self.BlockSize)
		if not self.zero_padding:
			p = bytes([pad_len]*pad_len)
		else:
			p = bytes(pad_len)
		intext_ba += p
		assert (len(intext_ba)%self.BlockSize) == 0

		# initialize
		outtext_ba = bytearray(len(intext_ba)+self.BlockSize)
		location = 0
		outtext_ba[0:self.BlockSize] = self.get_initial_vector()

		for i in range(len(intext_ba)//self.BlockSize):

			buf = self.encrypt_xor(outtext_ba,intext_ba,location)
			buf = self.aes.encrypt_block(buf)
			location += self.BlockSize
			outtext_ba[location:location+self.BlockSize] = buf

		return outtext_ba


	# DECRYPTION

	def remove_padding(self,ba):
		i = int.from_bytes(ba[-1:],byteorder='big')
		if i<=0 or i>self.BlockSize:
			return ba
		return ba[:-i]

	def decrypt_xor(self,plaintext,ciphertext,buf,location):
		for i in range(self.BlockSize):
			plaintext[location+i] = buf[i] ^ ciphertext[location+i]

	def decrypt_only(self,intext_ba):
	
		assert isinstance(intext_ba,bytearray),"decrypt parameter not a bytearray"
		assert (len(intext_ba)%self.BlockSize and self.BlockSize>0) == 0, "decrypt text wrong length"

		# initialize
		outtext_ba = bytearray(len(intext_ba)-self.BlockSize)
		location = 0

		for i in range(len(outtext_ba)//self.BlockSize):

			buf = intext_ba[location+self.BlockSize:location+2*self.BlockSize]
			buf = self.aes.decrypt_block(buf)
			self.decrypt_xor(outtext_ba,intext_ba,buf,location)
			location += self.BlockSize
			
		return outtext_ba

	def decrypt(self,intext_ba):
		outtext_ba = self.decrypt_only(intext_ba)
		if not self.zero_padding:
			return self.remove_padding(outtext_ba)
		return outtext_ba


	# PADDING ORACLE

	def padding_oracle(self,intext_ba, verbose=False):
		ba = self.decrypt_only(intext_ba)
		if verbose:
			self.print_bytearray(ba)
		i = int.from_bytes(ba[-1:],byteorder='big')
		if i<=0 or i>self.BlockSize:
			return False
		return ba[-i:]==bytes([i]*i)

# end class
