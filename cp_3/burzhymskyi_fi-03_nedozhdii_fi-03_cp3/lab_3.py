def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        (d, x, y) = extended_gcd(b, a % b)
        return d, y, x - int(a / b) * y


def solve_linear_mod_equations(a, b, n):
    res = []
    (d, x, y) = extended_gcd(a, n)
    if d == 1:
        res.append((x * b) % n)
    else:
        if b % d == 0:
            (a, b, n) = (a / d, b / d, n / d)
            (_, x, y) = extended_gcd(a, n)
            x_0 = (x * b) % n
            for i in range(d):
                res.append(int(x_0 + i * n))
    return res


alph1 = "абвгдежзийклмнопрстуфхцчшщыьэюя"
alph2 = "абвгдежзийклмнопрстуфхцчшщьыэюя"

M_bi = ["ен", "на", "то", "но", "ст"]
C_var = ["кд", "щю", "во", "рб", "тд"]

def cb(bigram, alphabet):
    n = len(alphabet)
    number = alphabet.index(bigram[0]) * n + alphabet.index(bigram[1])
    return number


def splitOnPairs(list1, list2, alph):
    listOfPairs = []
    for indexX1 in range(len(list1)):
        for indexY1 in range(len(list2)):
            for indexX2 in range(len(list1)):
                for indexY2 in range(len(list2)):
                    if indexX1 != indexX2 and indexY1 != indexY2 and indexX2 < indexX1:
                        listOfPairs.append(
                            [cb(list1[indexX1], alph), cb(list2[indexY1], alph), cb(list1[indexX2], alph),
                             cb(list2[indexY2], alph)])
    return listOfPairs


def solve_system(x1, y1, x2, y2, mod):
    (_, r, _) = extended_gcd(x1 - x2, mod)
    a = (r * (y1 - y2)) % mod
    b = (y1 - a * x1) % mod
    return a, b


def keys(pairs):
    key = []
    mod = len(alph1) ** 2
    for p in pairs:
        key.append(solve_system(p[0], p[1], p[2], p[3], mod))
    return key


def decode(code, a, b, alph):
    text = ""
    m = len(alph)
    (d, a, _) = extended_gcd(a, m**2)
    if d != 1:
        return text
    i = 0
    while i < len(code) - 1:
        x = a*(cb(code[i]+code[i+1], alph) - b) % m**2
        x2 = x % m
        x1 = int((x-x2)/m)
        text += alph[x1]+alph[x2]
        i += 2
    return text


def N(Y,t):
    k = 0
    for i in Y:
        if i == t:
            k += 1
    return k


def IoC(Y, alphabet):
    k = 0
    n = len(Y)
    for t in alphabet:
        tmp = N(Y,t)
        k += (tmp * (tmp - 1))
    k = float(k / (n * (n - 1)))
    return k


def searchThroughKeys(text, keys, alphabet):
    texts = []
    I_normal = 0.059
    for k in keys:
        texts.append(decode(text, k[0], k[1], alphabet))
    j = 0
    for text in texts:
        if text != '':
            index = IoC(text, alphabet)
            if abs(index - I_normal) < 0.001:
                print(keys[j][0], keys[j][1])
                print(index)
                print(text)
        j += 1


varpairs1 = splitOnPairs(M_bi, C_var, alph1)
varpairs2 = splitOnPairs(M_bi, C_var, alph2)

vark1 = keys(varpairs1)
vark2 = keys(varpairs2)

with open('03.txt', 'r', encoding="utf8") as f:
    vartext = f.read()
vartext = vartext.replace('\n', '')

searchThroughKeys(vartext, vark1, alph1)
searchThroughKeys(vartext, vark2, alph2)