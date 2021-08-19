#! /Users/sergiorodrigo/Documents/tesis/test/examples/.env/bin/python

def is_palindrome(word: str) -> bool:
    i = 0 
    j = len(word) - 1
    while i < j:
        if word[i] != word[j]:
            return False
        i += 1
        j -= 1
    return True

print(f"apple: {is_palindrome('apple')}")
print(f"apple: {is_palindrome('aaaabbaaaa')}")