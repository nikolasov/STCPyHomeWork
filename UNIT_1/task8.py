# todo: Проверить истинность высказывания: "Данное четырехзначное число читается одинаково
# слева направо и справа налево".
def please_input_val():
    print("Input Number with 4 digits ")
    Num = input()
    validation = True
    if not Num.isdigit():
        print("value is not digit!")
        validation = False
    Num=str(int(Num)) #исключаем 0 вначале 
    if validation and not len(Num) == 4:
        print("num of digit not equal 4!")
        validation = False
    return Num,validation

Num,is_valid = please_input_val()
while not is_valid:
    Num,is_valid = please_input_val()

if Num == ''.join(reversed(Num)):
    print("True, num is symetryc")
else:
    print("False, num is asymetryc")

