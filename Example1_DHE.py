# Python 2.7
import sys  # unsure if entirely necessary
from random import randrange  # To get a int from 0 to arg - randrange(arg)
#Always useful to have some prime numbers, could've used a https://en.wikipedia.org/wiki/Primality_test to save some disk space
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
a = primes[randrange(len(primes))]  # priv key a
b = primes[randrange(len(primes))]  # priv key b

p = primes[randrange(5, len(primes))]  # pub value for modulo
g = primes[randrange(len(primes))]  # pub base value - should be a primi root if working to the wiki example

# creating pub key for Alice
A = pow(g,a,p)

# creating pub key for Bob
B = pow(g,b,p)

print 'Public/Shared Values'
print 'g == ', g
print 'p == ', p
print
print 'Private keys'
print 'a == ', a
print 'b == ', b
print
print 'Public keys'
print 'A == ', A, ' == g^a mod p == ', g, '^',a,' mod ', p
print 'B == ', B, ' == g^b mod p == ', g, '^',b,' mod ', p
print
print
secretA = pow(B,a,p)
secretB = pow(A,b,p)
print "Alice's secret generation == B^a mod p == ", B, '^',a,' mod ', p, " == ", secretA
print "Bob's secret generation   == A^b mod p == ", A, '^',b,' mod ', p, " == ", secretB
