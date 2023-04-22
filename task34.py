# todo:
#  Напишите рекурсивную функцию sumn(n), которая вычисляет и печатает сумму чисел от 0 до n.

def sumn(n):
    if n == 0:
        return 0
    return n+sumn(n-1)


print(sumn(5))
