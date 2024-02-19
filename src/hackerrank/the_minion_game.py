

def minion_game(string):
    k_score = 0; s_score = 0
    for i in range(len(string)):
        if c[i].lower() in ('a', 'e', 'i', 'o', 'u'):
            k_score += len(string) - i
        else:
            s_score += len(string) - i
        # for j in range(0, len(string)-i):
        #     c = string[j:j+i+1]
        
    if k_score > s_score:
        print(f'Kevin {k_score}')
    elif k_score < s_score:
        print(f'Stuart {s_score}')
    else:
        print('Draw')
        
if __name__ == '__main__':
    s = input()
    minion_game(s)