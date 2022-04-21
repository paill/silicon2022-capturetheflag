
import sys

KEY = "91HcwAhvxh"

def xor(data, key):
	l = len(key)
	output_str = ""

	for i in range(len(data)):
		current = data[i]
		current_key = key[i%len(key)]
		output_str += chr(ord(current) ^ ord(current_key))
	
	return output_str

def printC(ciphertext):
	print('{ 0x' + ', 0x'.join(hex(ord(x))[2:] for x in ciphertext) + ' };')

if not sys.argv[1]:
	print('Need something to encrypt!')
	sys.exit()

plaintext=sys.argv[1]+'\0'


ciphertext = xor(plaintext, KEY)

printC(ciphertext)
