from collections import Counter

dictionary = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
number = "0123456789"

key2 = "як"
key3 = "моя"
key4 = "мова"
key5 = "точно"
key10 = "русалочкая"
key11 = "русалочкати"
key12 = "глубинахморс"
key13 = "вглубинахморс"
key14 = "прекраснымголо"
key15 = "прекраснымголос"
key16 = "прекраснымголосо"
key17 = "прекраснымголосом"
key18 = "умиротворитьсамыег"
key19 = "умиротворитьсамыеги"
key20 = "умиротворитьсамыегрр"


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


f = open('text_1v.txt', encoding="utf8")  # 1 варіант
text1 = f.read().replace('\n', '')

my_text = open("text.txt", "r+", encoding='utf-8')  # текст
text_ = my_text.read()
text = edit_text(text_, dictionary)
my_text.close()


def Vigenere_decrypt(text, key):
    key_len = len(key)
    res = ''
    for i in range(len(text)):
        if text[i].isalpha():
            shift = dictionary.index(key[i % key_len])
            res += dictionary[(dictionary.index(text[i]) - shift) % 32]
        else:
            res += text[i]
    return res


def Vigenere_encrypt(text, key):
    key_len = len(key)
    res = ''
    for i in range(len(text)):
        if text[i].isalpha():
            shift = dictionary.index(key[i % key_len])
            res += dictionary[(dictionary.index(text[i]) + shift) % 32]
        else:
            res += text[i]
    return res


t2 = Vigenere_encrypt(text1, key2)
t3 = Vigenere_encrypt(text1, key3)
t4 = Vigenere_encrypt(text1, key4)
t5 = Vigenere_encrypt(text1, key5)
t10 = Vigenere_encrypt(text1, key10)
t11 = Vigenere_encrypt(text1, key11)
t12 = Vigenere_encrypt(text1, key12)
t13 = Vigenere_encrypt(text1, key13)
t14 = Vigenere_encrypt(text1, key14)
t15 = Vigenere_encrypt(text1, key15)
t16 = Vigenere_encrypt(text1, key16)
t17 = Vigenere_encrypt(text1, key17)
t18 = Vigenere_encrypt(text1, key18)
t19 = Vigenere_encrypt(text1, key19)
t20 = Vigenere_encrypt(text1, key20)


def Index_coinsidence(text):
    n = len(text)
    I = 0
    N = dict(Counter(text))

    for t in N:
        I += N[t]*(N[t]-1) / (n * (n - 1))

    return I


print(Index_coinsidence(text1))
"""
print("відповідність по ключам:")
print(Index_coinsidence(t2))
print(Index_coinsidence(t3))
print(Index_coinsidence(t4))
print(Index_coinsidence(t5))
print(Index_coinsidence(t10))
print(Index_coinsidence(t11))
print(Index_coinsidence(t12))
print(Index_coinsidence(t13))
print(Index_coinsidence(t14))
print(Index_coinsidence(t15))
print(Index_coinsidence(t16))
print(Index_coinsidence(t17))
print(Index_coinsidence(t18))
print(Index_coinsidence(t19))
print(Index_coinsidence(t20))
print("індекс відповідності вт:")
print(Index_coinsidence(text1))

"""


def Blocks(text, key_length):
    block = ['' for i in range(key_length)]
    for i in range(len(text)):
        block[i % key_length] += text[i]
    return block


def Key_lenght(text1):
    key_len = {}
    for k in range(2, 31):
        i = 0
        blocks = Blocks(text1, k)
        for b in blocks:
            i += Index_coinsidence(b)
        i = i / len(blocks)
        key_len[k] = i
    print(key_len)
    max_key_len = max(key_len, key=key_len.get)
    print("Maximum key length:", max_key_len, key_len[max_key_len])


print("key length:")
key = Key_lenght(text1)
print(key)


def Key_freq_letter(text, block_length):
    blocks = Blocks(text, block_length)
    keys = []
    for k in range(len(blocks)):
        count_let = {}
        for l in blocks[k]:
            if l in count_let:
                count_let[l] += 1
            else:
                count_let[l] = 1

        max_count = 0
        max_letter = ''
        for letter, count in count_let.items():
            if count > max_count:
                max_count = count
                max_letter = letter

        key = (dictionary.index(max_letter) - 14) % 32
        keys.append(dictionary[key])

        print(
            f"Block {k+1}: letter with highest frequency is '{max_letter}', key is '{dictionary[key]}'")

    return ''.join(keys)


print("result key:")
print(Key_freq_letter(text1, 12))


def Key_M(text, key_len):
    key = ""
    p = [0.0801, 0.0159, 0.0454, 0.0165, 0.0298, 0.0845, 0.0899, 0.0254, 0.0716, 0.0007, 0.0186, 0.0523, 0.0312, 0.0670, 0.1097, 0.0281,
         0.0473, 0.0547, 0.0626, 0.0262, 0.0026, 0.0097, 0.0048, 0.0144, 0.0073, 0.0062, 0.0457, 0.0310, 0.0739, 0.0201, 0.0010, 0.0047]

    blocks = Blocks(text, key_len)

    for num in range(len(blocks)):
        N = {}
        for l in blocks[num]:
            if l in N:
                N[l] += 1
            else:
                N[l] = 1
        ListKey = dict()
        for g in range(32):
            M = 0
            for t in range(32):
                t_g = dictionary[(t + g) % 32]
                if t_g in N:
                    val1 = N[t_g]
                else:
                    val1 = 0
                val2 = p[t]
                M += val1 * val2
                ListKey[dictionary[g]] = M

        count1 = ''
        count2 = 0

        for ch in ListKey:
            if ListKey[ch] > count2:
                count1 = ch
                count2 = ListKey[ch]

        key += count1

    return key, ListKey


print(Key_M(text1, 12))


key_1 = "вшебспирбуря"
key_2 = "вшекспирбуря"

print("--------------------")
print(Vigenere_decrypt(text1, key_1))
print(Vigenere_decrypt(text1, key_2))
