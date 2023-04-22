#todo:
# Создайте функцию-генератор, которая создает последовательность числовых
# палиндромов: 1 2 3 4 5 6 7 8 9 11 22 33 44 55 66 77 88 99 101 111 121 131 141 151 161 171 181 191 202 212 …
from math import pow


#Функция генерирует все числовые полиндромы состоящие из n чисел
def gen_pol_for_deg(n):
    if n <= 0:
        return []
    if n == 1:
        return [i for i in range(1, 10)]
    if n == 2:
        return [i*10+i for i in range(1, 10)]
    val = gen_pol_for_deg(n-2)
    return [int(i*pow(10, n-1) + j*10 + i) for i in range(1, 10) for j in [0] + val]


#Интерфейсный метод генерирует список числовых полиндромов с заданым числом цифр
# d - максимальное число цифр в полиндромах
# all_before_d - флаг для дополнительного вывода всех полнидром с числом цифр <d
def gen_pol_for_depth(d, all_be_d=False):
    if all_be_d:
        if d == 1:
            return gen_pol_for_deg(d)
        return gen_pol_for_depth(d-1, all_be_d) + gen_pol_for_deg(d)
    
    return gen_pol_for_deg(d)


print(gen_pol_for_depth(3, True))
