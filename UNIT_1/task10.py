#Единицы массы пронумерованы следующим образом: 1 — килограмм, 2 — миллиграмм, 3 — грамм, 4 — тонна, 5 — центнер.
#Дан номер единицы массы и масса тела M в этих единицах (вещественное число). Вывести массу данного тела в килограммах.
# Данную задачу нужно решить с помощью конструкции  match  (Python v3.10)


# Пример:
# Введите единицу массы тела
#       1 - килограмм
#       2 — миллиграмм
#       3 — грамм
#       4 — тонна
#       5 — центнер
#>4

#Введите  массу тела
#>1

#Ответ: 1000 кг
'''
_dict = {
         "1": "килограмм",
         "2": "миллиграмм",
         "3": "грамм",
         "4": "тонна",
         "5": "центнер"   
         }
mul={
     "1":1,
     "2":1e-6,
     "3":1e-3,
     "4":1e3,
     "5":1e2
     }

print("введите код единицы измерения")
print(_dict)
key = input()
while not mul.get(key):
     print("неверный код ! повторите ввод")
     print(_dict)
     key = input()

print("введите массу, единцы = "+ _dict[key])
mass = input()
while not mass.isdecimal():
    print("значение массы некорректно повторите ввод")
    mass = input()

 
print("Масса = " + str(float(mass)*mul[key]) + " кг")
'''
# v2  with match
_dict = {
         "1": "килограмм",
         "2": "миллиграмм",
         "3": "грамм",
         "4": "тонна",
         "5": "центнер"   
         }

print("введите код единицы измерения")
print(_dict)
key = input()
print("введите массу, единцы = "+ _dict[key])
mass = input()
while not mass.isdecimal():
    print("значение массы некорректно повторите ввод")
    mass = input()

mass = float(mass)
match key:
     case "1":
          mass *= 1
     case "2":
          mass *= 1e-6
     case "3":
          mass *= 1e-3
     case "4":
          mass *= 1e3
     case "5":
          mass *= 1e2
     case other:
          print("Единицы измерения неизвестны! ")

print("Масса = " + str(mass) + " кг")