from collections import Counter
import re



def word_counter(sentence):
    if len(sentence) < 1:
        raise ValueError("Please write a sentence or word")

    sentence = re.sub('[^A-Za-z0-9]+', ' ', sentence.lower())
    
    sentence = str(sentence.lower()).split(' ')
    
    sentence = dict(Counter(sentence))

    return sentence




if __name__ == '__main__':

    sentence = input("Please insert a sentence:  ")
    output = word_counter(sentence)
    print(output)