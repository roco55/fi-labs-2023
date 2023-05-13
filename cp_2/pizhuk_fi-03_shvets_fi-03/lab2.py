from text import cyph

CHARSET_RU = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
FREQ_RU = {
    'О': 10.97, 'Е': 8.49, 'А': 8.01, 'И': 7.35, 'Н': 6.7, 'Т': 6.26, 'С': 5.47, 'Р': 4.73, 'В': 4.54, 'Л': 4.40,
    'К': 3.49, 'М': 3.21, 'Д': 2.98, 'П': 2.81, 'У': 2.62, 'Я': 2.01, 'Ы': 1.90, 'Ь': 1.74, 'Г': 1.7, 'З': 1.65,
    'Б': 1.59, 'Ч': 1.44, 'Й': 1.21, 'Х': 0.97, 'Ж': 0.94, 'Ш': 0.73, 'Ю': 0.64, 'Ц': 0.48, 'Щ': 0.36, 'Э': 0.32,
    'Ф': 0.26, 'Ъ': 0.04}


def vigenere_encode(text: str, key: str, charset: str = CHARSET_RU) -> str:
    key = key.upper()
    text = text.upper()
    result = ''
    for i in range(len(text)):
        key_index = charset.index(key[i % len(key)])
        text_index = charset.index(text[i])
        result += charset[(text_index + key_index) % len(charset)]
    return result


def vigenere_decode(text: str, key: str, charset: str = CHARSET_RU) -> str:
    key = key.upper()
    text = text.upper()
    result = ''
    for i in range(len(text)):
        key_index = charset.index(key[i % len(key)])
        text_index = charset.index(text[i])
        result += charset[(text_index - key_index) % len(charset)]
    return result


def N_t(text: str, char: str):
    return text.count(char)


def M_i(block: str, g: int, charset: str = CHARSET_RU):
    summ = 0
    for i in range(len(CHARSET_RU)):
        summ += FREQ_RU[charset[i]] * N_t(block, charset[(i + g) % len(charset)])
    return summ


def I(text: str, charset: str = CHARSET_RU):
    summ = 0
    for char in charset:
        summ += N_t(text, char) * (N_t(text, char) - 1)
    return summ / (len(text) * (len(text) - 1))


def get_r(text, start=1, end=30):
    match = {}
    for r in range(start, end + 1):
        blocks = ['' for i in range(r)]
        for i in range(len(text)):
            blocks[i % r] += text[i]
        result = [I(block) for block in blocks]
        match[r] = sum(result) / len(result)
    return match


open_text = 'НояживуневидядняВомракебесконечнойночиИнетнадеждыуменяВгробусмыкаюсвоиочиНояживуневидядняВомракебесконечнойночиИнетнадеждыуменяВгробусмыкаюсвоиочиНояживуневидядняВомракебесконечнойночиИнетнадеждыуменяВгробусмыкаюсвоиочи'.upper()
key0 = 'ШП'
key1 = 'КОТ'
key2 = 'ЖАБА'
key3 = 'ПОТЕЦ'
key4 = 'скрывшисьотпогони'.upper()

enc0 = vigenere_encode(open_text, key0)
enc1 = vigenere_encode(open_text, key1)
enc2 = vigenere_encode(open_text, key2)
enc3 = vigenere_encode(open_text, key3)
enc4 = vigenere_encode(open_text, key4)

open_r = get_r(open_text)
r0 = get_r(enc0)
r1 = get_r(enc1)
r2 = get_r(enc2)
r3 = get_r(enc3)
r4 = get_r(enc4)

Iopen = I(open_text, CHARSET_RU)
I0 = I(enc0, CHARSET_RU)
I1 = I(enc1, CHARSET_RU)
I2 = I(enc2, CHARSET_RU)
I3 = I(enc3, CHARSET_RU)
I4 = I(enc4, CHARSET_RU)

print('Ir open:')
print(open_r)
print('Ir 1:')
print(r0)
print('Ir 2:')
print(r1)
print('Ir 3:')
print(r2)
print('Ir 4:')
print(r3)
print('Ir 5:')
print(r4)

a = cyph.upper()

match_dict = get_r(a)
match_list = []
for key in match_dict:
    match_list.append((key, match_dict[key]))
match_list = sorted(match_list, key=lambda x: abs(x[1] - 0.055))
print('for encoded text')
print(match_dict)
print(match_list)
best_fit = match_list[0][0]

blocks = ['' for i in range(best_fit)]
for i in range(len(a)):
    blocks[i % best_fit] += a[i]

keys = []
for most_possible in ('О', 'Е', 'А'):
    key = ''
    for i in range(best_fit):
        val = {char: N_t(blocks[i], char) for char in CHARSET_RU}
        max_key = max(val, key=val.get)
        k = (CHARSET_RU.index(max_key) - CHARSET_RU.index(most_possible)) % 32
        key += CHARSET_RU[k]
    keys.append(key)

print(keys)
# РЕЫИНТУЕЗРАЗЛЪЧЯЯ
# ЩОДСЦЫЬОРЩЙРФГАИИ -> РОДИНАБЕЗРАЗЛИЧИЯ
# ЮУЙЦЫАБУХЮОХЩИЕНН

key_m = ''
for block in blocks:
    val = {CHARSET_RU[g]: M_i(block, g) for g in range(len(CHARSET_RU))}
    max_key = max(val, key=val.get)
    key_m += max_key

print(key_m)
print(a)
print(vigenere_decode(a, 'РОДИНАБЕЗРАЗЛИЧИЯ'))
