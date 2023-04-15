#todo: Напишите калькулятор (простой). На вход подается строка, например:
# 1 + 2  или  5 – 3  или  3 * 4  или  10 / 2.
# Вывод: сосчитать и напечатать результат операции.
# Гарантируется, что два операнда и операция есть в каждой строчке, и все они разделены пробелами. 

def to_float(v):
    try:
       return float(v)
    except:
        return None 
    
def calculate(express):
    v1 = to_float(express[0])
    v2 = to_float(express[2])
    if v1 == None or v2 == None:
        return None, False, "Невозможно посчитать выражение со значениями "+express[0]+" - "+express[2]
    if express[1] == "+":
        return v1 + v2,True,"Рузультат = "
    if express[1] == "-":
        return v1 - v2,True,"Рузультат = "
    if express[1] == "*":
        return v1 * v2,True,"Рузультат = "
    if express[1] == "/":
        try:
            val = v1/v2
            return val, True,"Рузультат = "
        except:
            return None,False,"Невозможно выполнить деление на ноль "
    return None, False,"Невозможно посчитать выражение с оператором "+ express[1]

# Main
while True:
    print("Введите простое выражение с одним оператором, список операторов [+, - , * , /].\nЧтобы выйти введите quit.")
    expression = input().split(" ")
    if len(expression) == 1:
        if expression[0] == "quit":
            break
        else: 
            continue
    if len(expression) != 3: 
        continue
    result = calculate(expression)

    if result[1]:
        print(result[2]+str(result[0]))
    else:
        print(result[2])


