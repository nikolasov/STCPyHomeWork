#todo:  Напишите программу, которая получает на вход строку, и определяет,
# является ли строка панграммой (т.е. содержатся ли в ней все 33 буквы русского алфавита).
#Абвгдеёжзийклмнопрстуфхцчшщъыьэюя

a = ord('а')
symb_map = {chr(i):0 for i in range(a,a+32)}
symb_map['ё'] = 0
print("Input word")
n = input().lower()
for key in n:
    if key in symb_map:
        if symb_map[key] == 0:
            symb_map[key]+=1
                
print("True" if sum(symb_map.values()) == len(symb_map) else "False")

