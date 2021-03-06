# Python 3 program to build Bloom Filter
# Install mmh3 and bitarray 3rd party module first
# pip install mmh3
# pip install bitarray
from __future__ import absolute_import
import math
import mmh3
from bitarray import bitarray
from random import shuffle
import numpy
import datetime
import math
import hashlib
#from pybloom.utils import range_fn, is_string_io, running_python_3
from struct import unpack, pack, calcsize
import time

 
class Node:
	def __init__(self,k):

		self.bit=bitarray(k)
		#to implement delete functionality. Count is present for each bit.
		self.count=[bitarray(4) for i in range(k)]

		self.bit.setall(0)

	def display(self):
		print(self.bit)
		print(self.count)
		print(len(self.bit))

class BloomFilter:

	def __init__(self, items_count,fb):
		self.fp_prob = fb
 
		# Size of bit array to use
		self.size = self.get_size(items_count,self.fp_prob)
 
		# number of hash functions to use
		self.hash_count = self.get_hash_count(self.size,items_count)

		#size of each partition
		self.k=self.size/self.hash_count
 
		# List of bit arrays to partition the data
		self.bit_array = [Node(self.k) for x in range(self.hash_count)]

	
	def get_size(self,n,p):
		'''
		Return the size of bit array(m) to used using
		following formula
		m = -(n * lg(p)) / (lg(2)^2)
		n : int
			number of items expected to be stored in filter
		p : float
			False Positive probability in decimal
		'''
		m = -(n * math.log(p))/(math.log(2)**2)
		return int(m)
 
	

	def get_hash_count(self, m, n):
		'''
		Return the hash function(k) to be used using
		following formula
		k = (m/n) * lg(2)
 
		m : int
			size of bit array
		n : int
			number of items expected to be stored in filter
		
		'''
		
		k = (m/n) * math.log(2)
		return int(k)

	def display(self):
		for i in range(self.hash_count):
			print(self.bit_array[i].display())

#function to search for element
	def Query(self,x):
		
		for i in range(0,self.hash_count):
			index=mmh3.hash(x,i) % self.k
			if self.bit_array[i].bit[index]==0:
				return False
		return True

	def add(self,x):
	
			for j in range(self.hash_count):
				index=mmh3.hash(x,j) %self.k 

				if self.bit_array[j].bit[index]==1:
					self.bit_array[j].count[index]+=1
				else:
					self.bit_array[j].bit[index]=1
					self.bit_array[j].count[index]=1

	def delete(self,x):
		if self.Query(x)==False:
			print("Element does not exist")
			return
		else:
			for j in range(self.hash_count):
				index=mmh3.hash(x,j)%self.k

				if self.bit_array[j].bit[index]==1:
					self.bit_array[j].count[index]-=1
				if self.bit_array[j].count[index]==0:
					self.bit_array[j].bit[index]=0
				else:
					print("Element does not exist")
					return
		print("Element successully deleted!")

#SCALABLE DEFINITION
class ScalableBloomFilter:

	def __init__(self, initial_capacity=200, error_rate=0.001):
		
		if not error_rate or error_rate < 0:
			raise ValueError("Error_Rate must be a decimal less than 0.")
		self.filters =  bitarray(initial_capacity)
		self.initial_capacity = initial_capacity
		self.error_rate = error_rate
		self.count=0
		self.hash_count = self.get_hash_count(self.initial_capacity,20)

		#size of each partition
		self.k=self.initial_capacity//self.hash_count
		self.capacity=self.initial_capacity

	def get_size(self,n,p):
 
		m = -(n * math.log(p))/(math.log(2)**2)
		return int(m)
 
 
	def get_hash_count(self, m, n):
		'''
		Return the hash function(k) to be used using
		following formula
		k = (m/n) * lg(2)
 
		m : int
			size of bit array
		n : int
			number of items expected to be stored in filter
		'''
		k = (m/n) * math.log(2)
		return int(k)
	
	def add(self, key):
		"""Adds a key to this bloom filter.
		If the key already exists in this filter it will return True.
		Otherwise False.
		"""

		self.count+=1
		print(self.count)
		if self.count>self.initial_capacity:
			filters=bitarray(self.initial_capacity)
			self.capacity+=self.initial_capacity

		self.filters.append(filter)
		for i in range(self.hash_count):
			# create digest for given item.
			# i work as seed to mmh3.hash() function
			# With different seed, digest created is different
			digest = mmh3.hash(key,i) % self.capacity
			#print(digest)
			#print(len(self.filters))
			self.filters[digest] = 1


def main():  
	n = 20 #no of items to add
	fp=0.08
	bloomf = BloomFilter(n,fp)


	print("Implementing an accurate counting bloom filter")
	print("Size of bit array:{}".format(bloomf.k))
	print("False positive Probability:{}".format(bloomf.fp_prob))
	print("Number of hash functions:{}".format(bloomf.hash_count))
 
# words to be added
	word_present = ['abound','abounds','abundance','abundant','accessable',
				'bloom','blossom','bolster','bonny','bonus','bonuses',
				'coherent','cohesive','colorful','comely','comfort',
				'gems','generosity','generous','generously','genial']
 
# word not added
	word_absent = ['bluff','cheater','hate','war','humanity',
			   'racism','hurt','nuke','gloomy','facebook',
			   'geeksforgeeks','twitter']
 
	for item in word_present:
		bloomf.add(item)
 
	shuffle(word_present)
	shuffle(word_absent)
	runtimes=0
	test_words = word_present[:10] + word_absent
	shuffle(test_words)
	for word in test_words:
		start = datetime.datetime.now()
		if bloomf.Query(word)==False:
			print("'{}' is not present".format(word))
		else:
			print("'{}' is probably present!".format(word))
		finish = datetime.datetime.now()
		print('Runtime: ',(finish-start).microseconds,"microseconds")
		print("\n")

		runtimes+=(finish-start).microseconds
	avg=runtimes/n
	print("Average Runtime:",avg, "microseconds")

	print("\n")
	print("\n")
	time.sleep(10)
	print("*****************************************************************")

	'''Bloom filter application to check for already used usernames and weak passwords'''
	'''Bloom filter data structure partition sizes and no of bits in each partition need to be changed to handle large
	file sizes. Check how t partition more efficiently. Also calculate the runtime of the below application and space complexity''
	'''
	 #replace 2000 with number of words in username.txt
	print("Checking for used usernames and weak passwords")
	
	print("*****************************************************************")

	#print("Number of hash functions:{}".format(bloomf.hash_count))
	i = 0
	f = open("usernames.txt", "r")
	for i, line in enumerate(f):
		  pass
	f.close()

	t=BloomFilter(i,fp)
	print("Size of bit array:{}".format(t.k))
	print("False positive Probability:{}".format(t.fp_prob))

	with open('usernames.txt','r') as f:
		for line in f:
			for word in line.split():
				t.add(word)

	flag=1
	while True:
		user=raw_input("Enter Username ")
		if t.Query(user)==True:
			print("Username already in use!")
		else:
			print("Username accepted")
			flag=0
			break

	i = 0
	f = open("passwords.txt", "r")
	for i, line in enumerate(f):
		  pass
	f.close()

	p=BloomFilter(i,fp)
	with open('passwords.txt','r') as f:
		for line in f:
			for word in line.split():
				p.add(word)
	if flag==0:
		while True:
			passwd=raw_input("Enter password ")
			if p.Query(passwd)==True:
				print("Please use another password! It is a common password!")
			else:
				flag=1
				print("Password accepted")
				break

	t=ScalableBloomFilter()

	f = open("passwords.txt", "r")
	for i, line in enumerate(f):
		  pass
	f.close()
	time.sleep(10)
	print("****************************************************************")
	print("Scalable Bloom filter Implementation")
	print("Dispaying weak passwords using SBF")
	p=ScalableBloomFilter()
	with open('passwords.txt','r') as f:
		for line in f:
			for word in line.split():
				p.add(word)
				print(word)

if __name__=='__main__':
	main()
