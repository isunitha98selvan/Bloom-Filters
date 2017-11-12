# Python 3 program to build Bloom Filter
# Install mmh3 and bitarray 3rd party module first
# pip install mmh3
# pip install bitarray
import math
import mmh3
from bitarray import bitarray
from random import shuffle
 
class Node:
	def __init__(self,k):

		self.bit=bitarray(k)
		#to implement delete functionality. Count is present for each bit.
		self.count=[0 for i in range(k)]

		self.bit.setall(0)

	def display(self):
		print(self.bit)
		print(self.count)
		print(len(self.bit))

class BloomFilter:

	def __init__(self, items_count,fp_prob):
		self.fp_prob = fp_prob
 
		# Size of bit array to use
		self.size = self.get_size(items_count,fp_prob)
 
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


	#instead of import mmh3 ,add user defined hash functions.
	def add(self,x):
	
			for j in range(self.hash_count):
				index=mmh3.hash(x,j) %self.k #doesnt generate different hash function eevry time. check this.
				#print(j,index)

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

def main():  
	n = 20 #no of items to add
	p = 0.05 #false positive probability
 
	bloomf = BloomFilter(n,p)
	
	print("Implementing an accurate counting bloom filter")
	print("Size of bit array:{}".format(bloomf.size))
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
 
	test_words = word_present[:10] + word_absent
	shuffle(test_words)
	for word in test_words:
		if bloomf.Query(word)==False:
			print("'{}' is not present".format(word))
		else:
			print("'{}' is probably present!".format(word))

	print("*****************************************************************")

	'''Bloom filter application to check for already used usernames and weak passwords'''
	'''Bloom filter data structure partition sizes and no of bits in each partition need to be changed to handle large
	file sizes. Check how t partition more efficiently. Also calculate the runtime of the below application and space complexity''
	'''
	t=BloomFilter(2000000,p) #replace 2000 with number of words in username.txt
	with open('usernames.txt','r') as f:
		for line in f:
			for word in line.split():
				t.add(word)
	flag=1
	while flag==1:
		user=raw_input("Enter Username ")
		if t.Query(user)==True:
			print("Username already in use!")
			break
		else:
			flag=0
			break

	'''p=BloomFilter(20000,p) #replace 2000 with number of words in password.txt
	with open('passlist.txt','r') as f:
		for line in f:
			for word in line.split():
				t.add(word)
	flag=0
	while flag==0:
		passwd=raw_input("Enter password")
		if p.Query(passwd)==True:
			print("Weak password!")
		else:
			flag=1
			print("Strong password")
'''
if __name__=='__main__':
	main()