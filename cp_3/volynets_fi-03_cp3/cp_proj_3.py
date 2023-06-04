from pprint import pprint
import math
import itertools
import heapq
from operator import itemgetter

import lab_constants as constants


def gcd(a: int, b: int) -> int:
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Error: only integer values are allowed")
    
    if a < 0 or b < 0:
        raise ValueError("Error: only positive values are allowed")
    
    if a == 0:
        return b
    
    if b == 0:
        return a

    if a == 1 or b == 1:
        return 1
    
    if a == b:
        return a
    
    r_1, r_2 = max(a, b), min(a, b)

    r_3 = r_1 % r_2
    # print(f"r_3 = {r_3}")
    r_1 = r_2
    r_2 = r_3

    while r_3 != 0:
        r_3 = r_1 % r_2
        # print(f"r_3 = {r_3}")
        r_1 = r_2
        r_2 = r_3
    
    return r_1

def reverse(a: int, M: int) -> int:
    if not isinstance(a, int) or not isinstance(M, int):
        raise ValueError("Error: only integer values are allowed")
    
    while a < 0:
        a += M

    if a >= M:
        a = a % M

    if a == 0:
        raise ValueError("Error: zero has no reverse element")

    if a == 1:
        return 1

    q_vals = []
    r_1 = M
    r_2 = a
    r_3 = 1
    while r_3 != 0:
        q_vals.append(int(r_1 / r_2))
        r_3 = r_1 % r_2

        r_1 = r_2
        r_2 = r_3
    
    if r_1 != 1:
        raise ValueError(f"Error: number must have no comon divisors with module while have: {r_1}")
    
    q_vals.pop()
    
    u_vals = [1, 0]
    v_vals = [0, 1]
    for q in q_vals:
        u_vals.append(u_vals[-2] - u_vals[-1] * q)
        v_vals.append(v_vals[-2] - v_vals[-1] * q)
    
    # print(f"q_vals: {q_vals}")
    # print(f"u_vals: {u_vals}")
    # print(f"v_vals: {v_vals}")
    
    if v_vals[-1] >= 0:
        return v_vals[-1]
    
    return v_vals[-1] + M

def solve_dif_system(a_1: int, mod_1: int, a_2: int, mod_2: int) -> int:
    d = gcd(mod_1, mod_2)

    if d != 1:
        return

    N = mod_1 * mod_2

    N_1 = mod_2
    N_2 = mod_1

    M_1 = reverse(a=N_1, M=mod_1)
    M_2 = reverse(a=N_2, M=mod_2)

    print(f"answ = ({a_1} * {N_1} * {M_1} + {a_2} * {N_2} * {M_2}) % {N}")

    X_0 = (a_1 * N_1 * M_1 + a_2 * N_2 * M_2) % N

    return X_0

def count_bi_gram(text: str) -> dict: 
    bi_gram_counter = dict()

    for key in itertools.product(constants.__RU_ALPHABET__, repeat=2):
        s_key = key[0] + key[1]
        reps = text.count(s_key)
        if reps != 0:
            bi_gram_counter[s_key] = reps

    return bi_gram_counter

class AffineCryptographer:
    def __init__(self, alphabet: str, leters_probability: list) -> None:
        self.leters_probability = leters_probability.copy()
        self.set_alphabet(alphabet=alphabet)

    def set_alphabet(self, alphabet: str) -> None:
        # self.most_frequent_leter = "о"

        self.alphabet = alphabet
        self.size = len(alphabet)

        self.__id_to_letter = dict()
        for id, leter in zip(range(len(alphabet)), alphabet):
            self.__id_to_letter[id] = leter

        self.__letter_to_id = dict()
        for id, leter in zip(range(len(alphabet)), alphabet):
            self.__letter_to_id[leter] = id

    def get_id(self, leter: str):
        """
        Retruns:
            int: index of leter in alphabet, starting from 0
        """
        return self.__letter_to_id[leter]

    def get_id_bi(self, bi_gram: str):
        return self.__letter_to_id[bi_gram[0]] * self.size + self.__letter_to_id[bi_gram[1]]

    def get_leter_bi(self, id: int):
        return self.get_leter(int(id / self.size)) + self.get_leter(id % self.size)

    def get_leter(self, leter_id: int):
        """
        Retruns:
            str: char in alphabet at given index
        """
        while leter_id >= self.size:
            leter_id -= self.size
        
        while leter_id < 0:
            leter_id += self.size

        return self.__id_to_letter[leter_id]

    def encrypt(self, open_text: str, key: list) -> str:
        encrypted_text = ""
        for c in open_text:
            encrypted_text += self.get_leter(leter_id=(key[0] * self.get_id(c) + key[1]))
        
        return encrypted_text
    
    def decrypt_with_key(self, encrypted_text: str, key: str) -> str:
        decrypted_text = ""
        for c in encrypted_text:
            id = reverse(a=key[0], M=self.size) * (self.get_id(c) - key[1])
            decrypted_text += self.get_leter(leter_id=id)
        
        return decrypted_text
    
    def get_bi_text(self, text: str) -> list:
        if len(text) % 2 == 1:
            raise ValueError(f"Error with text size that must be even but {len(text)} was gieven")
        
        bi_text = []

        for i in range(0, len(text), 2):
            bigr = text[i] + text[i+1]
            bi_text.append(bigr)
        
        return bi_text
    
    def encrypt_bi(self, open_text: str, key: list) -> str:
        encrypted_text = ""
        if len(open_text) % 2 == 1:
            raise ValueError("Error: problem with open text size")
        
        bi_text = self.get_bi_text(text=open_text)

        # encryption
        for bigr in bi_text:
            encrypted_id = self.get_id_bi(bigr) * key[0] + key[1]
            encrypted_text += self.get_leter_bi(encrypted_id)
        
        return encrypted_text
    
    def decrypt_with_key_bi(self, encrypted_text: str, key: str) -> str:
        decrypted_text = ""

        bi_text = self.get_bi_text(text=encrypted_text)

        for bigr in bi_text:
            decrypted_id = reverse(a=key[0], M=self.size * self.size) * (self.get_id_bi(bigr) - key[1])
            decrypted_text += self.get_leter_bi(id=decrypted_id)
        
        return decrypted_text
    
    def get_key(self, encrypted_bi_1, encrypted_bi_2, decrypted_bi_1, decrypted_bi_2):
        mod = pow(self.size, 2)

        x_1 = self.get_id_bi(decrypted_bi_1)
        x_2 = self.get_id_bi(decrypted_bi_2)
        y_1 = self.get_id_bi(encrypted_bi_1)
        y_2 = self.get_id_bi(encrypted_bi_2)

        # y = ax mod 
        x = x_1 - x_2
        y = y_1 - y_2
        
        if x < 0:
            x += mod

        d = gcd(a=x, b=mod)

        if d == 1:
            r = reverse(a=x, M=mod)
            a = (y * r) % mod
            b = (y_1 - a * x_1) % mod
        
            return [(a, b)] # the only solution
        
        if y % d != 0:
            return []  # no solution
        
        x = int(x / d)
        y = int(y / d)
        mod = int(mod / d)

        r = reverse(a=x, M=mod)
        a = (y * r) % mod
        b = (y_1 - a * x_1) % mod

        rez = []

        for i in range(d):
            rez.append((a, b))
            a += mod
            b += mod
        
        return rez

    def count_occurrences(self, text: str) -> dict:
        occurrences = dict()
        for c in self.alphabet:
            occurrences[c] = 0

        for c in text:
            occurrences[c] += 1
        
        return occurrences

    def accordance_index(self, text: str) -> float:
        index = 0

        occurrences = self.count_occurrences(text=text)
        for key in occurrences:
            index += occurrences[key] * (occurrences[key] - 1)

        n = len(text)
        index = (index / n) / (n-1)

        return index

    def check_if_is_meaningful(self, text) -> bool:
        I = self.accordance_index(text=text)
        I_def = 0.0591

        if abs(I - I_def) < 0.01:
            return True
        
        return False
    
    def check_key(self, encrypted_text, key):
        decrypted_text = ""
        try:
            decrypted_text = self.decrypt_with_key_bi(encrypted_text=encrypted_text, key=key)
        except ValueError as e:
            return False
        
        if self.check_if_is_meaningful(text=decrypted_text):
            print(f"text: {decrypted_text}")
            print(f"key: {key}")
            
            return True

        return False
    
    def decrypt_bi(self, encrypted_text: str) -> str:
        mf = self.find_the_most_frequent_bi_gramm(text=encrypted_text, n=5)
        mf_def = ["ст", "но", "то", "на", "ен"]

        print("In progress...")
        for p1 in itertools.permutations([0, 1, 2, 3, 4], 2):
            # print(f"p1: {p1}")
            print(f"Still in progress...")
            for p2 in itertools.permutations([0, 1, 2, 3, 4], 2):
                # print(f"p2: {p2}")
                keys = self.get_key(decrypted_bi_1=mf_def[p1[0]],
                                   decrypted_bi_2=mf_def[p1[1]],
                                   encrypted_bi_1=mf[p2[0]],
                                   encrypted_bi_2=mf[p2[1]])
                
                for key in keys:
                    if self.check_key(encrypted_text=encrypted_text, key=key):
                        # return
                        pass
                    

    def find_the_most_frequent_bi_gramm(self, text: str, n: int=5) -> dict:
        bi_gram = count_bi_gram(text=text)
        max_four = dict(heapq.nlargest(n=n, iterable=bi_gram.items(), key=itemgetter(1)))

        return list(max_four.keys())

def prepare_text(text: str) -> str:
    final_text = ""
    
    for c in text:
        if c.lower() in constants.__RU_ALPHABET__:
            final_text += c.lower()
    
    return final_text

def main():
    # print(find_the_most_frequent_bi_gramm(text=constants.__VARIANT_TEXT__))
    # {'еш': 68, 'шя': 52, 'еы': 50, 'до': 49, 'зо': 48}
    # print(find_the_most_frequent_bi_gramm(text=constants.__FOR_TEST__))
    # {'щь': 119, 'ьв': 92, 'ез': 88, 'ди': 80, 'ий': 75}

    John = AffineCryptographer(leters_probability=constants.__RU_ALPHABET_LETERS_PROBABILITY__,
                               alphabet=constants.__RU_ALPHABET__)

    text = """Автомобиль, без преувеличения, можно назвать самым популярным транспортным средством на нашей планете. Он есть практически в каждом доме, а некоторые семьи имеют даже несколько машин.
    Безусловно, автомобили во многом упрощают жизнь человека. С их помощью можно легко и быстро добраться из одной точки города в другую, а также перевезти тяжёлые вещи. Машина — это отличное средство для путешествий в пределах родной страны или заграницу.
    Но к сожалению, с большой распространённостью автомобилей в мире связано множество экологических проблем. Главная из них — это загрязнение воздуха выхлопными газами. Оно вредит здоровью людей и приводит к ухудшению состояния атмосферы.
    Последнее влечёт за собой явление под названием парниковый эффект. Выхлопные газы, скапливаясь в атмосфере, препятствуют отдаче тепла земли в космос. В результате воздух над поверхностью нашей планеты сильно нагревается, что приводит ещё к целому ряду осложнений, таких как повышение уровня мирового океана, глобальное таяние ледников, нарушение климата и так далее.
    Одним словом, цена, которую люди платят за использование автомобилей, несмотря на всё их удобство, довольно высока. Поэтому я не могу назвать эти транспортные средства исключительно друзьями человека.
    Машины действительно сильно вредят людям, поэтому в будущем, если мы хотим продолжить пользоваться ими, ситуация должна измениться. Уже сейчас начался активный поиск альтернативных источников энергии, способных заменить собой бензиновые двигатели.
    В связи с этим успешно были введены в эксплуатацию электромобили. Надеюсь, в будущем транспорт также сможет стать не только безвредным, но и совершенно бесшумным. Лишь тогда люди смогут массово передвигаться на автомобилях без вреда для своего здоровья и для планет."""

    text = prepare_text(text)
    # print(f"text: {text}")
    # print(">><><>><><><><><><><<<><><><")
    
    encrypted_text = John.encrypt_bi(open_text=text, key=(7, 7))
    # print(f"encrypted_text: {encrypted_text}")
    
    # encrypted_text = constants.__FOR_TEST__
    encrypted_text = constants.__VARIANT_TEXT__
    decrypted_text = John.decrypt_bi(encrypted_text=encrypted_text)
    # print(f"decrypted_text: {decrypted_text}")


if __name__ == "__main__":
    main()
