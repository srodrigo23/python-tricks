#!/usr/bin/python

print "Hola mundo"

# shebang, hashbang, sharpbang en el mundo unix
# raw_input()

c = "Hola\nmundo"
e = 3.5
d = "uno"
f = "dos "

print "====Cadenas en python===="
triple = """primera linea
y esto se vera en 
otra linea"""
print triple
print f * 3

print "====listas en python===="

l = [22, True, "una lista", [1,2]]

t = 1, 2, 3
print type(t)
print t

li = [2, 3, 5, 7, 9, 10, 22, 34, 56, 67]
print li[0::3]

print l[3][1]



print type(c)
print c
print e // 2
