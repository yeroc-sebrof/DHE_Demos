from socket import *
from random import randrange #To get a int from 0 to arg - randrange(a)
import binascii
import struct
import sys
#Cant get this to work
def xor(s1,s2):
	return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
def repeat(key, length):
	return (key * (int(length/len(key))+1))[:length]

#Could point this about but not needed for example
IP = 'localhost'
PORT = 12000

#In an attempt to follow real standards by using primes
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]

#creates the conn
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((IP , PORT))
sentence = raw_input('Input sentence to send\n') # sentence will send after the handshake

#secret key
dhA = primes[randrange(len(primes))]

dhG = primes[randrange(len(primes))]
dhP = primes[randrange(5, len(primes))]
#g is the base int and p is the modulo (dont want P to be too small for the purpose of the example)

#pub key
dhUpperA = pow(dhG, dhA, dhP) #A = g^a mod p

#package
outbound = struct.Struct('I I I')

#Send Pub keys
packed_data = outbound.pack(dhUpperA, dhP, dhG)

clientSocket.sendall(packed_data)

unpacker = struct.Struct('I')

response = clientSocket.recv(unpacker.size)
#pulling apart the string recived

dhUpperB = unpacker.unpack(response)
#debug
#print dhUpperB[0]
secret = pow(dhUpperB[0],dhA,dhP)
send = xor(sentence, repeat(str(secret), len(sentence)))
clientSocket.send(send.encode())
ack = clientSocket.recv(1024).decode()
decodedAck = xor(ack, repeat(str(secret), len(ack)))
print ('From Server: ' + decodedAck)
clientSocket.close()
