import math
from collections import Counter


my_text = open("my_text.txt", "r+", encoding='utf-8')
text = my_text.read()
my_text.close()

dictionary = "абвгдежзийклмнопрстуфхцчшщыьэюя"  # without space
dictionary1 = "абвгдежзийклмнопрстуфхцчшщыьэюя "  # with space
number = "0123456789"


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


# print("Edited text without space", edit_text(
    # text, dictionary))  # without space
# print("Edited text with space", edit_text(text, dictionary1))  # with space


def FrequencyLetter(text):
    c = Counter(text)
    freq_letter = dict(c)
    for i in freq_letter:
        freq_letter[i] = round((freq_letter[i]/len(text)), 6)
    return dict(sorted(freq_letter.items()))


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


def FrequencyBigram1(text):  # with cross
    cross_freq_bigram = {}

    for i in range(0, len(text) - 1, 2):
        bigram = text[i: i+2]
        cross_freq_bigram[bigram] = cross_freq_bigram.get(bigram, 0) + 1

    bigrams = list(cross_freq_bigram.keys())

    for b in bigrams:
        cross_freq_bigram[b] = round(
            (cross_freq_bigram[b] / (len(text) // 2)), 6)

    return cross_freq_bigram


def EntropyBigram(frequency):
    n = 2
    entropy = 0
    for i in frequency:
        frequency[i] += frequency[i]*math.log2(frequency[i])

        entropy += frequency[i]
    res = round(entropy/n, 6)
    return -res


def EntropyLetter(frequency):
    entropy = 0
    for i in frequency:
        entropy += frequency[i]*math.log2(frequency[i])
    return round(-entropy/1, 6)


def RedundancyWithSpace(entropy):  # i=32 with space and 31 - without
    redundancy = round(1 - (entropy/math.log2(32)), 6)
    return redundancy


def RedundancyWithoutSpace(entropy):
    redundancy = round(1 - (entropy/math.log2(31)), 6)
    return redundancy


# Frequency
freql1 = FrequencyLetter(edit_text(text, dictionary1))
freql2 = FrequencyLetter(edit_text(text, dictionary))

print("\nFrequency monogram with space", freql1)
print("\nFrequency monogram without space", freql1)

freqb1 = sorted(FrequencyBigram(edit_text(text, dictionary1)).items())
print("\nFrequency bigram with space", freqb1)
freqb2 = sorted(FrequencyBigram1(edit_text(text, dictionary1)).items())
print("\nFrequency bigram with space and with a cross", freqb2)

freqb3 = sorted(FrequencyBigram(edit_text(text, dictionary)).items())
freqb4 = sorted(FrequencyBigram1(edit_text(text, dictionary)).items())

print("\nFrequency bigram without space", freqb3)
print("\nFrequency bigram without space and with a cross", freqb4)


# Entropy
entrm1 = EntropyLetter(FrequencyLetter(edit_text(text, dictionary1)))
entrm2 = EntropyLetter(FrequencyLetter(edit_text(text, dictionary)))

entrb1 = EntropyBigram(FrequencyBigram(edit_text(text, dictionary1)))
entrb2 = EntropyBigram(FrequencyBigram1(edit_text(text, dictionary1)))
entrb3 = EntropyBigram(FrequencyBigram(edit_text(text, dictionary)))
entrb4 = EntropyBigram(FrequencyBigram1(edit_text(text, dictionary)))


# print("\nEntropy monogram with space", entrm1)
# print("\nEntropy monogram without space", entrm2)

print("\nEntropy bigram with space", entrb1)
print("\nEntropy bigram with space and with cross", entrb2)
print("\nEntropy bigram without space", entrb3)
print("\nEntropy bigram without space and with cross", entrb4)

"""
# Redundancy
print("\nRedundancy monogram with space", RedundancyWithSpace(
    EntropyLetter(FrequencyLetter(edit_text(text, dictionary1)))))
print("\nRedundancy monogram without space", RedundancyWithoutSpace(
    EntropyLetter(FrequencyLetter(edit_text(text, dictionary)))))

print("\nRedundancy bigram with space", -RedundancyWithSpace(
    EntropyLetter(FrequencyBigram(edit_text(text, dictionary1)))))
print("\nRedundancy bigram with space and with a cross", -RedundancyWithSpace(
    EntropyLetter(FrequencyBigram1(edit_text(text, dictionary1)))))
print("\nRedundancy bigram without space", -RedundancyWithoutSpace(
    EntropyLetter(FrequencyBigram(edit_text(text, dictionary)))))
print("\nRedundancy bigram without space and with cross", -RedundancyWithoutSpace(
    EntropyLetter(FrequencyBigram1(edit_text(text, dictionary)))))


with open('output3.txt', 'w') as f:

    f.write('Frequency bigram with space:\n')
    for bigram, frequency in freqb1:
        f.write(f'{bigram:<10}{frequency:.6f}\n')

    f.write('Frequency bigram with space and with a cros:\n')
    for bigram, frequency in freqb2:
        f.write(f'{bigram:<10}{frequency:.6f}\n')

    f.write('Frequency bigram without space:\n')
    for bigram, frequency in freqb3:
        f.write(f'{bigram:<10}{frequency:.6f}\n')

    f.write('Frequency bigram without space and with a cross:\n')
    for bigram, frequency in freqb4:
        f.write(f'{bigram:<10}{frequency:.6f}\n')
"""
