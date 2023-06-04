from text import cyph


def gcd_ext(x, y):
    if x == 0:
        return y, 0, 1
    _gcd, x1, y1 = gcd_ext(y % x, x)
    x = y1 - (y // x) * x1
    return _gcd, x, x1


def gcd(x, y):
    return gcd_ext(x, y)[0]


def inversed(x, mod):
    return gcd_ext(x, mod)[1]


# ax === b (mod m)
def solve_mod_eq(a, b, m):
    M = m
    d = gcd(a, m)
    if b % d:
        return None
    a /= d
    b /= d
    m /= d
    x = (inversed(a, m) * b) % m
    roots = {int(x)}
    while True:
        x = (x - m) % M
        if x in roots:
            break
        roots.add(int(x))
    return roots


def count_bigrams(text: list) -> dict:
    frequencies = {}
    for bigram in text:
        if bigram in frequencies:
            frequencies[bigram] += 1
        else:
            frequencies[bigram] = 1
    return frequencies


def get_probability(text: list) -> dict:
    frequencies = count_bigrams(text)
    probs = {}
    for ngram in frequencies:
        probs[ngram] = frequencies[ngram] / sum(frequencies.values())
    return probs


def linear_decode(text: list, a, b, charset):
    mod = len(charset) ** 2
    result = ''
    for y in text:
        x = (inversed(a, mod) * (y - b)) % mod
        first = x // len(charset)
        second = x % len(charset)
        first = charset[first]
        second = charset[second]
        result += first + second
    return result


def convert_to_bigrams(text: str, charset: str):
    arr = []
    mod = len(charset)
    for i in range(0, len(text) - 1, 2):
        first = charset.index(text[i])
        second = charset.index(text[i + 1])
        ind = first * mod + second
        arr.append(ind)
        if ind == 20:
            print('stop')
    return arr


CHARSET1 = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ'
CHARSET2 = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЭЮЯ'

open_most_frequent = 'СТНОТОНАЕН'
impossible_bigrams = ('ЫЫ', 'ЬЬ', 'ЙЙ', 'ШШ', 'ЩЩ', 'ЭЭ')

for charset in (CHARSET1, CHARSET2):
    bigr_open_most_freq = convert_to_bigrams(open_most_frequent, charset)
    bigr_cyph = convert_to_bigrams(cyph, charset)
    cyph_bigrams = get_probability(bigr_cyph)
    cyph_most_frequent = sorted(cyph_bigrams, key=cyph_bigrams.get, reverse=True)[:5]

    to_solve = set()
    combinations_x = tuple(((x1, x2) for x1 in bigr_open_most_freq for x2 in bigr_open_most_freq if x1 != x2))
    combinations_y = tuple(((y1, y2) for y1 in cyph_most_frequent for y2 in cyph_most_frequent if y1 != y2))
    for x1, x2 in combinations_x:
        for y1, y2 in combinations_y:
            mod = len(charset) ** 2
            to_solve.add(((x1 - x2) % mod, (y1 - y2) % mod, x1, y1, mod))

    keys = set()
    for equation in to_solve:
        a = solve_mod_eq(equation[0], equation[1], equation[4])
        if not a:
            continue
        for root in a:
            b = (equation[3] - (equation[2] * root)) % equation[4]
            keys.add((root, b))

    decoded = []
    for key in keys:
        dec = linear_decode(bigr_cyph, key[0], key[1], charset)
        decoded.append(dec)

    for imp in impossible_bigrams:
        decoded = list(filter(lambda x: imp not in x, decoded))

    filtered = []
    for dec in decoded:
        dec_bigr = convert_to_bigrams(dec, charset)
        dec_freq = get_probability(dec_bigr)
        dec_most_frequent = sorted(dec_freq, key=dec_freq.get, reverse=True)[:15]
        if len(set(dec_most_frequent).intersection(set(bigr_open_most_freq))) > 3:
            filtered.append(dec)

    print(filtered)
