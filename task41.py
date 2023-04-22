#todo:
# В Python существуют ключевые слова, которые нельзя использовать для названия переменных, функций и классов. Для получения списка всех ключевых слов можно воспользоваться атрибутом kwlist из модуля keyword. Приведенный ниже код:
# import keyword
# print(keyword.kwlist)
# выводит: ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
# Напишите программу, которая принимает строку текста и заменяет в ней все ключевые слова на <kw>.
import keyword
kw = keyword.kwlist

print("Введите строку")
inp_str = input()


def check_word(word): 
    i_d = word.find(",")
    kw_ = "<kw>," if i_d >= 0 else "<kw>"
    if word.replace(",", "") in kw:
        return kw_
    return word


print(" ".join([check_word(i) for i in inp_str.split(" ")]))
