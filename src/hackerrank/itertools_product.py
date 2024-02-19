from itertools import product

def my_product(A, B):
    print(*product(A, B))
    
if __name__ == '__main__':
    A, B = map(int, input().split()), map(int, input().split())
    my_product(A, B)