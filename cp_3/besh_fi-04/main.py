from typing import Dict
from collections import defaultdict
from collections import Counter
from prettytable import PrettyTable
import itertools
import math
from scipy.stats import entropy

#НСД
def gcd_only(a, b):
    if b == 0:
        return a
    else:
        return gcd_only(b, a % b)
    
#Розширений АЕ
def bezout_coefficients(a, b):
    if b == 0:
        return a , 1, 0
    else:
        gcd,u_1, v_1 = bezout_coefficients(b, a % b)

        u = v_1
        v = u_1 - (a // b) * v_1
        return gcd , u , v
# Приклад використання 
#n_1=35
#m_1=12
#print(f"НСД: {gcd_only(n,m)}")
#result=bezout_coefficients(n_1,m_1)
#print(result[2])
#print(f"НСД: {result[0]}, Коефіціенти Безу: U={result[1]}, V={result[2]}")



#Лінійне порінвняння
def linear_solve(a, b, n):
    results = []
    gcd_ab, u, v = bezout_coefficients(a, n)
    if gcd_ab == 1:
        results.append((u * b) % n)
        return results
    elif gcd_ab > 1:
        if  b % gcd_ab == 0:
            a = a // gcd_ab
            b = b // gcd_ab
            n = n // gcd_ab
            x = (linear_solve(a,b,n)[0])
            results.append(x)
            for i in range(1, gcd_ab):
                results.append(results[-1] + i*n)
            return results
        else:
            return results

  
#Словник
alphabet='абвгдежзийклмнопрстуфхцчшщьыэюя'


#Редагування тексту
text_test="04.txt"
text_test_1=''
with open(text_test,encoding="utf8") as file :
    text_test_1=file.read()

clear_test_text_1=''
for letter in range(len(text_test_1)):
    if text_test_1[letter] in alphabet: clear_test_text_1+=text_test_1[letter]


#Реалізація n-грам з 1 лаби
def count(text: str, ngram: int = 1, intersection: bool = False) -> Dict[str, int]:
    counter = defaultdict(int)
    step = 1 if intersection else ngram
    text_len = len(text)

    for i in range(0, text_len - ngram + 1, step):
        ngram_str = text[i: i + ngram]
        counter[ngram_str] += 1
    result = dict(counter)
    return result


def print_table(data: Dict[str, int]):
    table = PrettyTable()
    table.field_names = ["Bigram", "Count"]
    for bigram, count in data.items():
        table.add_row([bigram, count])
    print(table)


#Найчастіші біграми у шифротексті топ 10
def most_freq_bigram(text: str, n: int = 10):
    bigram_count = count(text, ngram=2, intersection=False)
    top_n_bigrams = dict(sorted(bigram_count.items(), key=lambda x: x[1], reverse=True)[:n])
    print_table(top_n_bigrams)


print(most_freq_bigram(clear_test_text_1))


#Індекс біграми 
def ind_bi(bigram):
    temp = [alphabet.index(bigram[0]), alphabet.index(bigram[1])]
    return temp[0] * len(alphabet) + temp[1]

#Обернений елемент
def find_inverse_a(a, b):
    return bezout_coefficients(a, b)[1]
    

#Дешифратор
def decrypt_affine_bigram(text, key):
    a = key[0]
    b = key[1]
    inverse_a = find_inverse_a(a, len(alphabet)**2)
    decode_bigrams = []

    for i in range(0, len(text), 2):
        x = (inverse_a * (ind_bi(text[i:i + 2]) - b)) % (len(alphabet) ** 2)
        decode_bigram = alphabet[x // len(alphabet)] + alphabet[x % len(alphabet)]
        decode_bigrams.append(decode_bigram)

    decoded_text = ''.join(decode_bigrams)
    return decoded_text



#Одержані та теоритичні біграми 
most_theor_bigram = ["ст", "но", "ен", "то", "на"]
most_bi = ["еш", "еы", "шя", "ск", "до"]


#Комбінування теоретичних і найчастыших біграм
def combination_of_bigrams(most_theor_bigram, most_bi ):
    bigrams = []
    combinations = []
    
    for i in most_theor_bigram:
        for j in most_bi :
            bigrams.append((i, j))
    for i_index, i in enumerate(bigrams):
        for j_index in range(i_index + 1, len(bigrams)):
            j = bigrams[j_index]
            if i == j or (j, i) in combinations:
                continue
            elif i[0] == j[0] or i[1] == j[1]:
                continue
            combinations.append((i, j)) 
    return combinations


#знаходження пар (a,b)
def find_pairs_ab(combinations, alphabet_size=31**2):
    ab = []
    x1, x2 = ind_bi(combinations[0][0]), ind_bi(combinations[1][0])
    y1, y2 = ind_bi(combinations[0][1]), ind_bi(combinations[1][1])

    a_values = linear_solve(x1 - x2, y1 - y2, alphabet_size)
    for i in a_values:
        if gcd_only(i, 31) != 1:
            continue
        b = (y1 - i * x1) % alphabet_size
        ab.append((i, b))
    
    return ab


print("--------------------------------------------------------\n")
combinations = combination_of_bigrams(most_theor_bigram, most_bi)

#пошук пар (a,b)
pair_ab = []
for pair in combinations:
    temp = find_pairs_ab(pair)
    if len(temp) != 0:
        for j in range(len(temp)):
            pair_ab.append(temp[j])
print(pair_ab)
print("--------------------------------------------------------\n")


#Пошук вірного ключа за допомогою ентропії
for key in pair_ab:
    keys = []
    decoded_text = decrypt_affine_bigram(clear_test_text_1, key)
    frequency = Counter(decoded_text)
    total_length = len(clear_test_text_1)
    prob = [count / total_length for count in frequency.values()] 
    entropy_value = entropy(prob, base=2)    
    if 4.4 < entropy_value < 4.5:
        keys.append(key)

print(keys)

   
#вивід ключа та розшифрованого тексту
print("--------------------------------------------------------\n")
print(f"Вірний ключ знайдено: {key} \n a={key[0]}, b={key[1]}")
print("--------------------------------------------------------\n")
open_txt = decrypt_affine_bigram(clear_test_text_1, [390, 10])
print(open_txt)



