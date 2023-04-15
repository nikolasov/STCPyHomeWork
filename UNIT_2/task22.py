#todo: Напишите функцию, которая шифрует строку, содержащую латинские буквы с помощью шифра Цезаря. Каждая буква сдвигается на заданное число n позиций вправо. Пробелы, знаки препинания не меняются. Например, для n = 1.
# a → b,   b → c,    p → q,    y → z,    z V a
# A → B,   B → C,   Z → A
# Т.е. заголовок функции будет def code(string, n):
# В качестве результата печатается сдвинутая строка.
#abpyz, abpyz-- abpyz

# Проверка символа на соответсвие латинскому алфавиту + возврат границ индекса с учетом регистра
def check(word):
     id = ord(word)
     upper_case = (ord('A'),ord('Z'))
     lower_case = (ord('a'),ord('z'))
     if upper_case[0] <= id <= upper_case[1]:
        return True,upper_case[0],upper_case[1]
     if lower_case[0] <= id <= lower_case[1]:
        return True,lower_case[0],lower_case[1]
     return False,0,0

# Определяем новый индекс буквы в заданных границах
def get_new_id(w_id, n_shift,lbound,rbound):
     a = int(n_shift/26)
     if a == 0: a=n_shift
     elif a == 1: return w_id
     
     new_id = w_id+a
     if new_id > rbound:
        new_id = lbound+(new_id-rbound-1)

     return new_id

# Преобразование строки 
def get_shift_str(in_string, n_shift):
  shift_str=""
  # Основной цикл обработки строки по каждому символу
  for word in in_string:
    vals = check(word)
    if not vals[0]: 
       shift_str += word
    else:
       shift_str += chr(get_new_id(ord(word),n_shift,vals[1],vals[2]))

  return shift_str

# Старт 
#Ввод строки
in_string = ""
while len(in_string) == 0:
   print("Введите непустую строку")
   in_string=input()

#Ввод сдвига
n = "" 
while not n.isdigit() or int(n) <= 0:
    print("Введите величину сдвига для шифра Цезаря > 0",end=": ")
    n = input()   
n = int(n)

if len(in_string) == 0:
    exit()

print(get_shift_str(in_string,n))