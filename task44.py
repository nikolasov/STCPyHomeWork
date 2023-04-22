#todo: Напишите программу, в которой используется две функции. В одной программа «спит» 2 секунды, в другой – 3 секунды. Пусть каждая функция возвращает время, которое она «проспала».
# Главная программа запускает цикл от 0 до 10, если число четное, то запускает функцию с 2 секундами, если нечетное, то функцию с 3 секундами. Накапливает сон обеих функций отдельно и печатает две суммы. 
import time


def func_sleep_2():
    time.sleep(2)
    return 2


def func_sleep_3():
    time.sleep(3)
    return 3


funcs = [func_sleep_2, func_sleep_3]
sleep_sum = [0, 0]
for i in range(11):  
    i_d = 0 if i % 2 == 0 else 1
    print("Start func ....")
    sleep_sum[i_d] = sleep_sum[i_d] + funcs[i_d]()

print(f"func_sleep_2 = {sleep_sum[0]}, func_sleep_3 = {sleep_sum[1]}")