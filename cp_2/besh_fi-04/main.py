from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


#Словник
aplhabet='абвгдежзийклмнопрстуфхцчшщъыьэюя'


#Редагування тексту
first_text="first text.txt"

encode_text_1=''
with open(first_text,encoding="utf8") as file :
    encode_text_1=file.read()
encode_text_1=encode_text_1.lower()
encode_text_1=encode_text_1.replace('ъ','ь').replace('ё','е').replace("\n", " ")

clear_encode_text_1=''
for letter in range(len(encode_text_1)):
    if encode_text_1[letter] in aplhabet: clear_encode_text_1+=encode_text_1[letter]

output_text_1 = "2 clear_text.txt"
with open(output_text_1 ,'w',encoding="utf8") as file: 
    file.write(clear_encode_text_1)



#Ключі
key1 = "мы"
key2 = "они"
key3 = "моих"
key4 = "всеми"
key5 = "невидящеео"
key6 = "невидящееок"
key7 = "невидящееоко"
key8 = "невидящееокос"
key9 = "невидящееокосл"
key10 = "невидящееокоследит"



# Зашифрування тексту шифром Віженера
def vigener_cipher_encrypt(text, key, alphabet):
    len_key = len(key)
    encode_text_1 = ''  
    for letter in range(len(text)):
        if text[letter].isalpha():
            index_text = alphabet.index(text[letter])
            index_key = alphabet.index(key[letter % len_key])
            encoded_char = alphabet[(index_text + index_key) % len(alphabet)]
            encode_text_1 += encoded_char
        else:
            encode_text_1 += text[letter]    
    return encode_text_1


# Дешифрування тексту шифром Віженера
def vigener_cipher_decrypt(text, key, alphabet):
    len_key = len(key)
    decode_text_1 = ''  
    for letter in range(len(text)):
        if text[letter].isalpha():
            index_text = alphabet.index(text[letter])
            index_key = alphabet.index(key[letter % len_key])
            decoded_char = alphabet[(index_text - index_key) % len(alphabet)] 
            decode_text_1 += decoded_char
        else:
            decode_text_1 += text[letter]    
    return decode_text_1



# Результат шифрування з ключем 1
Vigenere_text_encrypt_1 = vigener_cipher_encrypt(clear_encode_text_1, key1, aplhabet)
#print(Vigenere_text_encrypt_1)
print("---------------------------------------------------------------------\n")
# Результат дешифрування з ключем 2
Vigenere_text_decrypt = vigener_cipher_decrypt(Vigenere_text_encrypt_1, key1, aplhabet)
#print(Vigenere_text_decrypt)
Vigenere_text_encrypt_2 = vigener_cipher_encrypt(clear_encode_text_1, key2, aplhabet)
Vigenere_text_encrypt_3 = vigener_cipher_encrypt(clear_encode_text_1, key3, aplhabet)
Vigenere_text_encrypt_4 = vigener_cipher_encrypt(clear_encode_text_1, key4, aplhabet)
Vigenere_text_encrypt_5 = vigener_cipher_encrypt(clear_encode_text_1, key5, aplhabet)
Vigenere_text_encrypt_6 = vigener_cipher_encrypt(clear_encode_text_1, key6, aplhabet)
Vigenere_text_encrypt_7 = vigener_cipher_encrypt(clear_encode_text_1, key7, aplhabet)
Vigenere_text_encrypt_8 = vigener_cipher_encrypt(clear_encode_text_1, key8, aplhabet)
Vigenere_text_encrypt_9 = vigener_cipher_encrypt(clear_encode_text_1, key9, aplhabet)
Vigenere_text_encrypt_10 = vigener_cipher_encrypt(clear_encode_text_1, key10, aplhabet)




#Знаходимо індекси відповідності 
def Find_index(clear_text):
    I_text=0
    N_text=Counter(clear_text)
    #print(N_text,"\n")
    for letter in N_text:
        I_text+=(1/(len(clear_text)*(len(clear_text)-1)))*N_text[letter]*(N_text[letter]-1)
        #Array_of_index.append(I_text)
    return I_text

index_0=Find_index(clear_encode_text_1)
index_1=Find_index(Vigenere_text_encrypt_1)
index_2=Find_index(Vigenere_text_encrypt_2)
index_3=Find_index(Vigenere_text_encrypt_3)
index_4=Find_index(Vigenere_text_encrypt_4)
index_5=Find_index(Vigenere_text_encrypt_5)
index_6=Find_index(Vigenere_text_encrypt_6)
index_7=Find_index(Vigenere_text_encrypt_7)
index_8=Find_index(Vigenere_text_encrypt_8)
index_9=Find_index(Vigenere_text_encrypt_9)
index_10=Find_index(Vigenere_text_encrypt_10)


Array_of_index=[]
Array_of_index.extend([index_0,
                       index_1,
                       index_2,
                       index_3,
                       index_4,
                       index_5,
                       index_6,
                       index_7,
                       index_8,
                       index_9,
                       index_10])
print(Array_of_index)



#Візуалізація індексів 
data = Array_of_index
plt.title('Столбчата діаграма')
labels = ['ВТ', '2літ', '3літ', '4літ', '5літ', '10літ', '11літ', '12літ', '13літ', '14літ', '18літ']
plt.bar(labels, data)
plt.show()



#Розшифрування відредактованого вже тексту variants3_clear_text.txt
#Редагування тексту 
first_text_2="text.txt"
encode_text_2=''
with open(first_text_2,encoding="utf8") as file :
    encode_text_2=file.read()
encode_text_2=encode_text_2.lower()
encode_text_2=encode_text_2.replace('ё','е').replace("\n", " ")

clear_encode_text_2=''
for letter in range(len(encode_text_2)):
    if encode_text_2[letter] in aplhabet: clear_encode_text_2+=encode_text_2[letter]
output_text_2 = "variant3_clear_text.txt"
with open(output_text_2 ,'w',encoding="utf8") as file: 
    file.write(clear_encode_text_2)




#Знаходимо довжину ключа 
Average_index_encode_text = []
Key_lengths = []

for i in range(2, 36):
    result = 0
    for j in range(0, i):
        count = 0
        block = clear_encode_text_2[j::i]
        counter_index = Counter(block)
        for letter in counter_index.values():
            count = count + (letter * (letter - 1))
        sum = count / ((len(block) * (len(block) - 1)))
        result += sum
    
    average_result = result / i
    
    Key_lengths.append(i)
    Average_index_encode_text.append(average_result)

plt.title("Індекси відповідності")
plt.bar(Key_lengths,Average_index_encode_text,color='blue')
plt.show()




#Результат довжина ключа 14 символів
print("Довжина ключа = 14")
real_key_len=14
often_letters = ['а', 'е', 'о','и']

for i in range(len(often_letters)):
    possible_keys = []
    for j in range(real_key_len):
        block_text = clear_encode_text_2[j::14]
        count_text = Counter(block_text)
        max_letter = max(count_text.values())
        for n in count_text.keys():
            if count_text[n] == max_letter:
                res = (aplhabet.find(n) - aplhabet.find(often_letters[i])) % 32
        possible_keys.append(aplhabet[res])
    print(f"Key{i}: {possible_keys}")


#Отриманий ключ
key_о=['э', 'б', 'о', 'м', 'ч', 'ц', 'т', 'н', 'и', 'к', 'ф', 'у', 'ь', 'о']
#Деякі штучні перетворення 
key_a_str='экомаятникфуко'
#Дешифрування варіанта 3
Vigenere_encode_text_decrypt=vigener_cipher_decrypt(clear_encode_text_2, key_a_str, aplhabet)
print(Vigenere_encode_text_decrypt)



encode_text_variant3='encode_text_variant3'
with open(encode_text_variant3,'w',encoding='utf-8') as file:
    encode_text_variant3=file.write(Vigenere_encode_text_decrypt)


    










