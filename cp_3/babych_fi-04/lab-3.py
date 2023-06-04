import itertools
import heapq
from collections import Counter
import math
import operator
import numpy as np
from functools import reduce
dictionary = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
number = "0123456789"

five_lang_freq_bigrams = ["ст", "но", "то", "на", "ен"][:4]
five_freq_bigrams = ['рн', 'ыч', 'нк', 'цз', 'тч'][:4]

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
letter_index = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7, 'и': 8, 'й': 9, 'к': 10, 'л': 11, 'м': 12, 'н': 13, 'о': 14,
                'п': 15, 'р': 16, 'с': 17, 'т': 18, 'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 'ч': 23, 'ш': 24, 'щ': 25, 'ь': 26, 'ы': 27, 'э': 28, 'ю': 29, 'я': 30}


def edit_text(text, dictionary1):
    for letter in text:
        text = text.lower()
        if letter == "ё":
            text = text.replace('ё', 'е')
        elif letter == "ъ":
            text = text.replace('ъ', 'ь')
        elif letter not in dictionary1 and not letter.isupper():
            text = text.replace(letter, '')
    new_text = open('clear_text1.txt', 'w')
    new_text.write(text)
    new_text.close()
    return text


my_text = open("text3.txt", "r+", encoding='utf-8')  # текст
text_ = my_text.read()
text = edit_text(text_, dictionary)
my_text.close()


def gcd(a, b):
    if (b == 0):
        return a
    else:
        d = gcd(b, a % b)
        return d


print(gcd(3, 26))


def ReverseElement(a, n):
    if n <= a:
        print("Module must be greater than a")
        return None

    if gcd(a, n) != 1:
        print("Inverse element doesn`t exist")
        return None

    u, v = 1, 0
    u1, v1 = 0, 1
    if n == 0:
        u, v = 1, 0
        return -1
    while n > 0:
        q = int(a/n)
        r = a % n

        a = n
        n = r

        temp = u1
        u1 = u - q * u1
        u = temp

        temp = v1
        v1 = v - q * v1
        v = temp

    #print("u:", u, "v:", v)
    return u


print(ReverseElement(3, 26))


def LinearCongruence(a, b, n):

    d = gcd(a, n)
    if d == 1:
        a_inv = ReverseElement(a, n)
        x = (a_inv*b) % n
        return [x]
    elif d > 1:
        if b % d != 0:
            print('The equasion has no solutions')
            return None
        if b % d == 0:
            a1, b1, n1 = int(a / d), int(b / d), int(n / d)
            d1 = gcd(a1, n1)
            a_1inv = ReverseElement(a1, n1)
            x_0 = (b1*a_1inv) % n1
            result = []
            for k in range(d):
                result.append(x_0 + k * n1)
            return result


print(LinearCongruence(7, 8, 13))


def FrequencyBigram(text):
    freq_bigram = {}
    for i in range(len(text)):
        bigram = text[i: i + 2]
        if bigram in freq_bigram:
            freq_bigram[bigram] += 1
        else:
            freq_bigram[bigram] = 1

    for i in freq_bigram:
        freq_bigram[i] = round(freq_bigram[i] / len(text), 6)

    return freq_bigram


def MostFrequentBigrams(freq_bigram):
    list_ = list(freq_bigram.items())
    sorted_list = dict(sorted(list_, key=operator.itemgetter(1)))
    sorted_list = dict(list(reversed(list(sorted_list.items()))))
    count_bigram = 0
    print("Five most frequent bigrams:")
    for bi, freq in sorted_list.items():
        print(f"{bi}: {freq} ")
        count_bigram += 1
        if count_bigram == 5:
            break


MostFrequentBigrams(FrequencyBigram(text))
most_freq = MostFrequentBigrams(FrequencyBigram(text))


def XY(text_bigram_pair, lang_bigram_pair):
    Y1 = reduce(lambda a, b: a * 31 +
                letter_index[b], text_bigram_pair[0], 0)
    Y2 = reduce(lambda a, b: a * 31 +
                letter_index[b], text_bigram_pair[1], 0)
    X1 = reduce(lambda a, b: a * 31 +
                letter_index[b], lang_bigram_pair[0], 0)
    X2 = reduce(lambda a, b: a * 31 +
                letter_index[b], lang_bigram_pair[1], 0)
    return X1, X2, Y1, Y2


def FindKeys(five_freq_bigrams, five_lang_freq_bigrams, alphabet):

    keys = []
    for i in itertools.combinations(five_lang_freq_bigrams, 2):
        for j in itertools.permutations(five_freq_bigrams, 2):
            x1, x2, y1, y2 = XY(j, i)
            a = LinearCongruence(x1 - x2, y1 - y2, (31*31))
            if a is None:
                continue
            b = [(y1 - a_ * x1) % (31*31) for a_ in a]
            key = [(a[k], b[k]) for k in range(len(a))]
            keys += key

    keys = sorted(list(dict.fromkeys(keys)))
    print("\nKeys:", keys)
    return keys


FindKeys(five_freq_bigrams, five_lang_freq_bigrams, alphabet)


print(letter_index)


def Decipher(a, b, text):
    x = ""
    for i in range(0, len(text), 2):
        y = BiToInt(text[i] + text[i+1], alphabet)
        a_inv = ReverseElement(a, (31*31))
        res = (a_inv * (y - b)) % (31*31)
        res = IntToBi(res, alphabet)
        x += res
    return x


def IntToBi(a, alphabet):
    b = alphabet[(a - (a % 31)) // 31]
    b += alphabet[a % 31]
    return b


def BiToInt(bigram, alphabet):
    result = alphabet.index(bigram[0]) * 31 + alphabet.index(bigram[1])
    return result


def Index_coinsidence(text):
    n = len(text)
    I = 0
    N = dict(Counter(text))

    for t in N:
        I += N[t]*(N[t]-1) / (n * (n - 1))

    return I


def RightKey():
    AB = FindKeys(five_freq_bigrams, five_lang_freq_bigrams, alphabet)

    for a, b in AB:
        dec_text = Decipher(a, b, text)
        i = Index_coinsidence(dec_text)
        if i >= 0.05:
            print("Rigth key: ", a, b)


print(RightKey())
#RightKey=(13, 151)
print(Decipher(13, 151, text))
