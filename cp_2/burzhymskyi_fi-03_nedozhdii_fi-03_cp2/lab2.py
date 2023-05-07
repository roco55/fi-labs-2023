import numpy as np

import numpy as np
alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

def redact_text():
    text = ""
    with open('balobol.txt', 'r', encoding="utf8") as f:
        line = f.read()
        line = line.lower()
        new_line = ""
        for letter in line:
            if letter >= 'а' and letter <= 'я':
                new_line += letter
        text += new_line
    with open('balobol_clean.txt', 'w', encoding="utf8") as f:
        f.write(text)

def encode(text, key):
    code = ""
    for i in range(len(text)):
        letter = alphabet[(alphabet.index(text[i]) + alphabet.index(key[i % (len(key))])) % len(alphabet)]
        code += letter
    return code

def decode(code,key):
    text = ""
    for i in range(len(code)):
        letter = alphabet[(alphabet.index(code[i]) - alphabet.index(key[i % (len(key))])) % len(alphabet)]
        text += letter
    return text

def N(Y,t):
    k = 0
    for i in Y:
        if i == t:
            k += 1
    return k

def IoC(Y):
    k = 0
    n = len(Y)
    for t in alphabet:
        tmp = N(Y,t)
        k += (tmp * (tmp - 1))
    k = float(k / (n * (n - 1)))
    return k

def lenKey(Y):
    n = len(Y)
    D = []
    deltaD = []
    for r in range(6, 31):
        D.append(0)
        for i in range(0, n-r):
            if(Y[i] == Y[i+r]):
                D[r-6] += 1

    deltaD.append(abs(D[0] - D[1]))
    for r in range(7,30):
        deltaD.append(max((D[r - 6] - D[r - 6 - 1]), (D[r - 6] - D[r - 6 + 1])))
    deltaD.append(abs(D[30 - 6] - D[30 - 6 - 1]))

    return D.index(max(D))+6

def splitCodeOnFragments(code, r):
    Y = np.full(r, "", dtype='object')
    j = 0
    for i in range(0,r):
        Y[i] = ""

    for i in range(0, len(code)):
        if i % r == 0:
            j += r
        Y[i-j] += code[i]
    return Y


def frequencyInFragment(Y):
    p = {'а': 0, 'б': 0, 'в': 0, 'г': 0, 'д': 0, 'е': 0,
     'ж': 0, 'з': 0, 'и': 0, 'й': 0, 'к': 0, 'л': 0,
     'м': 0, 'н': 0, 'о': 0, 'п': 0, 'р': 0, 'с': 0,
     'т': 0, 'у': 0, 'ф': 0, 'х': 0, 'ц': 0, 'ч': 0,
     'ш': 0, 'щ': 0, 'ъ': 0, 'ы': 0, 'ь': 0, 'э': 0,
     'ю': 0, 'я': 0}
    for letter in Y:
        p[letter] += 1
    return dict(sorted(p.items(), key=lambda item: item[1], reverse=True))

def findPossibleKey(blocks, p):
    p = dict(sorted(p.items(), key=lambda item: item[1], reverse=True))
    keys = []
    result = ""
    for i in range(len(blocks)):
        block = frequencyInFragment(blocks[i])
        key = ""
        for j in range(len(blocks)):
            key += (alphabet[(alphabet.index(list(block)[0]) - alphabet.index(list(p)[j])) % len(alphabet)])
        keys.append(key)
        result += keys[i][0]
    return result

def splitCodeOnBlocks(code, r):
    Y = np.full(r, "", dtype='object')
    j = 0
    for i in range(0, len(code)):
        if i % r == 0:
            j += r
        Y[i-j] += code[i]
    return Y.tolist()

def M_i(Y, g, p):
    k = 0
    for t in range(0,len(alphabet)):
        pr = p[alphabet[t]]
        nt = N(Y, alphabet[(t + g) % len(alphabet)])
        k += ( pr*nt )
    return k

def key(code, r, p):
    Y = splitCodeOnBlocks(code,r)
    key = ""
    for y_i in Y:
        maxF = 0
        maxG = 0
        for g in range(0,len(alphabet)):
            tmp = M_i(y_i, g, p)
            if tmp > maxF:
                maxF = tmp
                maxG = g
        key += alphabet[maxG]
    return key


with open('balobol_clean.txt', 'r', encoding="utf8") as f:
    our_text = f.read()

key_2 = "ру"
key_3 = "чвк"
key_4 = "груз"
key_5 = "гойда"
key_12 = "генацидрусни"

print(IoC(our_text))
print(IoC(encode(our_text,key_2)))
print(IoC(encode(our_text,key_3)))
print(IoC(encode(our_text,key_4)))
print(IoC(encode(our_text,key_5)))
print(IoC(encode(our_text,key_12)))


with open('labtext_encoded', 'r', encoding="utf8") as f:
    text = f.read()

r = lenKey(text)

p = {'а': 0.0837222, 'б': 0.0168792, 'в': 0.0439467, 'г': 0.0181161, 'д': 0.031353, 'е': 0.0863102,
     'ж': 0.0122626, 'з': 0.0159467, 'и': 0.0609324, 'й': 0.0106413, 'к': 0.0358363, 'л': 0.0479277,
     'м': 0.0321066, 'н': 0.0644872, 'о': 0.11294, 'п': 0.0280266, 'р': 0.0425652, 'с': 0.0526736,
     'т': 0.063589, 'у': 0.0280076, 'ф': 0.00373739, 'х': 0.00672502, 'ц': 0.00317793, 'ч': 0.0152578,
     'ш': 0.0076803, 'щ': 0.00312845, 'ъ': 0.000216936, 'ы': 0.0175642, 'ь': 0.0208754, 'э': 0.00356613,
     'ю': 0.00785918, 'я': 0.021941}


keyword = key(text, r, p)
print(keyword)

Yi = splitCodeOnFragments(text, r)
result = findPossibleKey(Yi, p)
print(result)

realkey = "экомаятникфуко"

print(decode(text, keyword))
print(decode(text, result))
print(decode(text, realkey))

print(IoC(text))
print(IoC(decode(text, realkey)))

