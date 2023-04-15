# todo:  Даны три переменные: X, Y, Z. Их значения числа.
# Из данных произвольных чисел выбрать наибольшее.

# Пример:
# X = 5
# Y = 10
# Z = 3
# Ответ: Наибольшее число 10.
#
# X = 10
# Y = 12
# Z = -7
# Ответ: Наибольшее число 12.
vals = {"X":0,"Y":0,"Z":0}

for key in vals.keys():
    inp = ""
    while not inp.isdecimal():
        print("Input " + key)
        inp = input()
    vals[key] = float(inp)

print("Max = " + str(max(vals.values())))