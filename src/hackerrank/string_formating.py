"""
String Formatting
link: https://www.hackerrank.com/challenges/python-string-formatting/problem?h_r=next-challenge&h_v=zen&isFullScreen=false
"""

def print_formatted(number):    
    l = len(bin(number)) - 2
    for i in range(1, number + 1):
        f = ""
        for c in "doXb":
            if f:
                f += " "
            f += "{:>" + str(l) + c + "}"
        print(f.format(i, i, i, i))

if __name__ == '__main__':
    n = int(input())
    print_formatted(n)
    
# def to_binary(num):
#     b = ''
#     while num >= 1:
#         b = str(num % 2) + b
#         num=num//2
#     return b
    
# def to_octal(num):
#     o = ''
#     while num >= 1:
#         o = str(num % 8) + o
#         num=num//8
#     return o

# def to_hexa(num):
#     h = ''; r = ''
#     while num >= 1:
#         res = num % 16
#         if res == 10:
#             r = 'A'
#         elif res == 11:
#             r = 'B'
#         elif res == 12:
#             r = 'C'
#         elif res == 13:
#             r = 'D'
#         elif res == 14:
#             r = 'E'
#         elif res == 15:
#             r = 'F'
#         else:
#             r = str(res)
#         h = r + h
#         num=num//16
#     return h