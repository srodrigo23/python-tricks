

def merge_the_tools(string, k):
    c = ""
    i=0
    for ch in string:
        if (i % k) == 0 and i>0:
            print(c)
            c = ""
        if ch not in c:
            c += ch
        i+=1
    print(c)

if __name__ == '__main__':
    string, k = input(), int(input())
    merge_the_tools(string, k)