from socket import *
from random import randrange
import binascii
import struct
import sys
#Cant get this to work
def xor(s1,s2):
	return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
def repeat(key, length):
	return (key * (int(length/len(key))+1))[:length]
#Important connection information
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM )
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
#Diffie-Hellman dataset
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
#we are expecting 3 ints when we recive our initial packet which needs to be translated
unpacker = struct.Struct('I I I')
print ("The server has launched")
while 1:
	connectionSocket, addr = serverSocket.accept() #open conn
	try:
		# grabbing 3 ints
		handshakeStart = connectionSocket.recv(unpacker.size)
		#pulling apart the string recived
		unpacked_data = unpacker.unpack(handshakeStart)
		#assuming that the ints are stored this way
		dhUpperA = unpacked_data[0]
		dhP = unpacked_data[1]
		dhG = unpacked_data[2]
		#debug
		#print dhUpperA
		#print dhP
		#print dhG
		#make sever secret
		dhB = primes[randrange(len(primes))]
		#prep responding a single int
		outbound = struct.Struct('I')
		#make server Pubkey
		dhUpperB = pow(dhG, dhB, dhP)
		#debug
		#print dhUpperB
		#pack pubkey
		packed_data = outbound.pack(dhUpperB)
		#send server pubkey
		connectionSocket.sendall(packed_data)
		#common Secret
		secret = pow(dhUpperA, dhB, dhP)
		message = connectionSocket.recv(1024).decode()
		print "Ciphered", message
		print "Deciphered", (xor(message, repeat(str(secret), len(message))))
		ack = xor("Acknowledged", repeat(str(secret), len("Acknowledged")))
		connectionSocket.send(ack.encode())
	finally:
		connectionSocket.close()
