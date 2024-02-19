from collections import Counter

if __name__ =='__main__':
    number_shoes = int(input())
    shoes = Counter(input().split())
    amount = 0
    for _ in range(int(input())):
        shop = input().split()
        if shop[0] in shoes.keys() and shoes[shop[0]] > 0:
            shoes[shop[0]]-=1
            amount += int(shop[1])
    print(amount)
                
    