#todo: Дан генетический код ДНК (строка, состоящая из букв G, C, T, A)
# Постройте РНК, используя принцип замены букв: G → C, C → G, T → A, A→T.
# Напишите функцию, которая на вход получает ДНК, и возвращает РНК. Например:
#Ввод: GGCTAA
#Вывод: CCGATT
dnk_rnk_map = {"G": "C", "C": "G", "T": "A", "A": "T"}


def check_input(val):
    if len(val) == 0:
        return False
    for i in val:
        if not i in dnk_rnk_map:
            return False
    return True


inp = ""
while not check_input(inp):
    print("input dnk, only G, C, T, A")
    inp = input()

print("".join([dnk_rnk_map[i] for i in inp]))
