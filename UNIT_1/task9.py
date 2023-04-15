# todo: Дан номер некоторого года (положительное целое число).
# Вывести соответствующий ему номер столетия, учитывая, что, к примеру, началом 20 столетия был 1901 год.
def please_input_year():
    print("Введите год (положительное целое число)")
    Num = input()
    if not Num.isdigit():
        print("Введенное значнеие не удовлетворяет условиям")
        return 0,False
    return int(Num),True

Y,Valid = please_input_year()

while not Valid:
    Y,Valid = please_input_year()

print("Год = "+ str(Y) + ", Столетие = "+str(int(Y/100) + (1 if Y%100 != 0 else 0)))

