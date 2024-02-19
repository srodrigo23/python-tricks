
from itertools import permutations

if __name__ == '__main__':
    ins = input().split()
    string, c = ins[0], int(ins[1])
    p = list(permutations(string, c))
    p.sort()
    for per in p:
        print(''.join(per))
    