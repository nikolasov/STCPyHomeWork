# Назовем пароль хорошим, если
#
# его длина равна 9 или более символам
# в нем присутствуют большие и маленькие буквы любого алфавита
# в нем имеется хотя бы одна цифра
# Напишите программу, которая требует ввода нового пароля до тех пор, пока не будет введен хороший.
#
#
# На вход программе подается произвольное количество паролей, каждый на отдельной строке. Гарантируется, что среди них присутствует хороший.
#
#
# Для каждого введенного пароля программа должна вывести текст:
#
# LengthError, если длина введенного пароля меньше 9 символов
# LetterError, если в нем все буквы имеют одинаковый регистр
# DigitError, если в нем нет ни одной цифры
# Success!, если введенный пароль хороший
#
# После ввода хорошего пароля все последующие пароли должны игнорироваться.
# Примечание 1. Приоритет вывода сообщений об ошибке в случае невыполнения нескольких условий:
# LengthError, затем LetterError, а уже после DigitError.
#
#
# Sample Input 1:
#
# arr1
# Arrrrrrrrrrr
# arrrrrrrrrrrrrrr1
# Arrrrrrr1
# Sample Output 1:
#
# LengthError
# DigitError
# LetterError
# Success!
#
# Sample Input 2:
#
# beegeek
# Beegeek123
# Beegeek2022
# Beegeek2023
# Beegeek2024
# Sample Output 2:
# LengthError
# Success!

class PasswdChecker:
    def __init__(self, min_len=9) -> None:
        self.min_len = min_len

    def valid_password(self, passwd):
        if not self.valid_len(passwd):
            return "LengthError"
        if not self.valid_register(passwd):
            return "LetterError"
        if not self.digit_existing(passwd):
            return "DigitError"
        return "Success!"

    def valid_register(self, passwd):
        if type(passwd) is type(str()):
            return not(passwd.isupper() or passwd.islower())
                #self.result.append("LetterError")
        return False
    
    def valid_len(self,passwd):
        if type(passwd) is type(str()):
            return len(passwd) >= self.min_len
                #self.result.append("LengthError")
        return False

    def digit_existing(self,passwd):
        if  type(passwd) is type(str()):
            count = 0
            for i in passwd:
                if i.isdigit(): count = count+1
            return count != 0
        return False

def check_input(password_str):
    print(f"Input:\n{password_str}")
    passwords = password_str.split("\n")
    pchk = PasswdChecker(9)
    chec_results = []
    for i in passwords:
        msg = pchk.valid_password(i)
        chec_results.append(msg)
        if msg == "Success!":
            break
    chec_results = '\n'.join(chec_results)
    print(f'Output:\n{chec_results}')


first ="arr1\nArrrrrrrrrrr\narrrrrrrrrrrrrrr1\nArrrrrrr1"
check_input(first)
second = "beegeek\nBeegeek123\nBeegeek2022\nBeegeek2023\nBeegeek2024"
print("--------------------")
check_input(second)