def transformSentence(sentence):
    words = sentence.split()
    for word in words:
        sentence = sentence.replace(word, change_word(word))
    return sentence
    

def change_word(word):
    if len(word) == 1:
        return word
    else:
        ans = word[0]
        for i in range(1, len(word)):
            if word[i-1].lower() < word[i].lower():
                ans = ans + (word[i].upper())
            elif word[i-1].lower() > word[i].lower():
                ans = ans + (word[i].lower())
            else:
                ans = ans + word[i]
        return ans
print(transformSentence('coOL dog'))
print(transformSentence('a Blue MOON'))