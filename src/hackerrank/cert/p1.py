def missingCharacters(s):
    ans = ''
    for i in range(10):
        if str(i) not in s:
            ans = ans + str(i)
    for i in range(97, 123, 1):
        if chr(i) not in s:
            ans = ans + chr(i)
    return ans

print(missingCharacters('8hypotheticall024y6wxz'))