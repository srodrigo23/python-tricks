
"""
Design door mat
link: https://www.hackerrank.com/challenges/designer-door-mat/problem?isFullScreen=false&h_r=next-challenge&h_v=zen
"""

def get_row_string(num_col, pos_mid, num_adds):
    row = ['-']*num_col
    row[pos_mid] = '|' ; row[pos_mid + 1] = '.' ; row[pos_mid - 1 ] = '.'
    cont = 0; left = pos_mid - 3; right = pos_mid + 3  
    while cont < num_adds:
        row[left] = '|'; row[left-1] = '.'; row[left+1]='.'
        row[right] = '|'; row[right-1] = '.'; row[right+1]='.'
        left= left - 3; right = right + 3
        cont += 1
    return ''.join(row)

def get_mid_welcome(num_col, pos_mid):    
    row = ['-']*num_col
    row[pos_mid] = 'C'
    row[pos_mid+1] = 'O'; row[pos_mid+2] = 'M'; row[pos_mid+3] = 'E'
    row[pos_mid-1] = 'L'; row[pos_mid-2] = 'E'; row[pos_mid-3] = 'W'
    return ''.join(row)

def get_mid_string_door(nrows, ncols, is_up):
    row = ""
    if is_up:    
        for i in range(0, nrows):
            row = row + get_row_string(ncols, ncols//2, i) + '\n'
    else:
        for i in range(nrows-1, -1, -1):
            row = row + get_row_string(ncols, ncols//2, i) + '\n'
    return row

def get_ans(N, M):
    ans =''
    ans = ans + get_mid_string_door(N//2, M, True)
    ans = ans + get_mid_welcome(M, M//2) + '\n'
    ans = ans + get_mid_string_door(N//2, M, False)
    return ans

if __name__ == "__main__":
    N, M = input().split()
    print(get_ans(int(N), int(M)))