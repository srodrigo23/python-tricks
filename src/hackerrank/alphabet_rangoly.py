# https://www.hackerrank.com/challenges/alphabet-rangoli/problem?isFullScreen=true

def print_rangoli(size):
    letter = 97 + (size-1)
    for i in range(0, size):
        row = ['-']*(4 * size -3)
        mid = len(row)//2
        aux_letter = letter
        row[mid] = chr(aux_letter)
        l = mid; r = mid
        inter_aux_letter = aux_letter
        for j in range(i+1):
            row[l-(2*j)] = chr(inter_aux_letter)
            row[r+(2*j)] = chr(inter_aux_letter)
            inter_aux_letter+=1
        letter -=1
        print(''.join(row))
    letter+=2
    for i in range(size-1, 0, -1):
        row = ['-']*(4 * size -3)
        mid = len(row)//2
        aux_letter = letter
        row[mid] = chr(aux_letter)
        l = mid; r = mid
        inter_aux_letter = aux_letter
        for j in range(i):
            row[l-(2*j)] = chr(inter_aux_letter)
            row[r+(2*j)] = chr(inter_aux_letter)
            inter_aux_letter+=1
        letter +=1
        print(''.join(row))
        
if __name__ == '__main__':
    n = int(input())
    print_rangoli(n)