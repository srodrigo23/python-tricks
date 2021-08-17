#!/usr/bin/python

num = input("Ingrese un numero" + "\n")

#numero espejo
def espejo(n):
	return True if (n == invertir(n)) else False
def invertir(n):
	nn = 0
	while n > 0 :
		nn = (nn * 10) + (n % 10)
		n = n / 10	
	return nn

#numero perfecto
import math
def perfecto(n):
	sd = 1
	for i in range(2, (n / 2)+1):
		if (n % i == 0):
			sd = sd + i
	return n == sd

#numeros primos
def primos(n):
	for i in range(2, n+1):
		if esPrimo (i) :
			print i
		
def esPrimo(num):
	for i in range(2, int(math.sqrt(num))+1):
		if (num % i == 0):
			return False
	return True

print("Espejo : " + str(espejo(num)))
print("Perfecto : " + str(perfecto(num)))
primos(num)