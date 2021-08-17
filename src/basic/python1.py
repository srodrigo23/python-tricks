import math
def esPrimo(n):
    nd = 0
    for i in range(2,int(math.sqrt(n))+1):
        if(n % i == 0):
            nd = nd + 1
    return nd == 0

l = int(input("Ingrese la cantidad de numeros primos a mostrar : "))
c = 0
n = 2
while (c < l):
    if(esPrimo(n)):
        print(n)
        c = c + 1
    n = n + 1