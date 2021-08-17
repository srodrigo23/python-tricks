# 1.- Hallar la sumatoria de los num del 1 al 10
def ej1():
    print(sum(range(1, 10)))

#2.- Factorial de un numero entero positivo
def ef2():
    num = int(input("Ingrese un numero :")) #python3 doesn't evaluate type input
    print(factorial(num))

def factorial(n):
    if n == 1: 
        return 1
    else:
        return n * factorial(n-1)

#3.- Hallar la suma de los primeros 20 primeros pares
def ej3():
    print(sum(range(2, 2*10 + 1, 2)))

#4.- Suma de los primeros 10 multiplos de 5
def ej4():
    print(sum([x*5 for x in range(1,11)]))

#5.-Multiplos del 7 en el intervalo del 100 al 200
def ej5():
    print([x for x in range(100, 201) if x%7==0])

#6.- El cuadrado de un numero dado por el metodo : n=4 -> 1+3+5+7=16
def ej6():
    n = int(input("Ingrese un numero para mostra el cuadrado : "))
    print(cuadrado(n))

def cuadrado(n):
    imp = 1
    sum = 0
    for i in range(n):
        sum = sum  + imp
        imp = imp + 2
    return sum

#7.- Calcular pi mediante la serie de Gregory pi/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - 1/11 + ...
# Determinar la cantidad de numeros de la serie
def pi_serie(n):
    den = 1
    sig = 1
    sum = 0
    for i in range(n):
        sum = sum + (sig*(1/den))
        sig = sig * -1
        den = den + 2
    return sum

def ej7():
    n = int(input("Ingrese la cantidad de elementos de la serie de gregory : "))
    print(pi_serie(n) * 4 )

#8.- Hallar la suma de la sig. serie : 1, 1/2, 1/3, 1/4, ... , 1/10
def ej8():
    print(sum(list(map(lambda x: 1/x, range(1, 11)))))

#9.- Hallar la suma de la sig serie : 1/2, 3/4, 5/8, 7/16, 9/32, 11/64, ... , 19/1024
#def ej9():
    # print(sum(list(map(lambda x, y: x/y, range(1, 20, 2), range(2, 1025, )))))