#todo: Реализовать игровую механику морского боя.
# 1. Система в случайном порядке расставляет 10 однопалубных кораблей в игровом поле 10x10
# 2. Между караблями при расстановке должно соблюдаться правило пустых полей.
# 3. Игра заканчивается при 20 промахах.
import random as rnd
from json import dump,load


# ---------------Инициализация поля
# Проверка возможности установить однопалубник в указанную позицию
def check_position(lst, i, j):
    count = len(lst[0])-1
    _sum = 0

    def cond(_i, _j):
        return 0 <= _i <= count and 0 <= _j <= count
    # Шаблон обхода сосединх ячеек
    cycle = [(i-1, j-1), (i-1, j), (i-1, j+1),
             (i, j-1), (i, j), (i, j+1),
             (i+1, j-1), (i+1, j), (i+1, j+1)]
    for val in cycle:
        if cond(val[0], val[1]):
            _sum = _sum+lst[val[0]][val[1]]
    return _sum


# формируем поле
def make_field(dimension=10):
    n = 0
    lst = [[0] * dimension for i in range(dimension)]
    while n < dimension:
        i = rnd.randint(0, dimension-1)
        j = rnd.randint(0, dimension-1)
        # Первый однопалубник выставляем остальные перед постановкой проверяем
        if n == 0 or check_position(lst, i, j) == 0:
            lst[i][j] = 1
            n = n+1
    return lst


# ------------Игровые функции
# Вывод текущего состояния поля
def print_field(lst, cols, deb=False):
    # определяем сивол клетки в зависимости от ее значения
    def get_sym_for(num):
        if num == 0 or num == 1:
            return "▇"# "■" # не использованная ячейка
        if num == 2:
            return "✳"# промах
        if num == 3:
            return "x"# подбит
    end_s = " " if deb else "\n"
    for i in range(-1, len(lst)):
        if i < 0:
            print(f"{' '*2}", end="")
            print(" ".join([key for key in cols.keys()]), end=end_s)
            if deb:
                print(f"{' '*2}", end="")
                print("  "+" ".join([key for key in cols.keys()]))

        else:
            print(f"{i}", end=" ")
            print(" ".join(map(lambda num: get_sym_for(num), lst[i])), end=end_s)
            if deb:
                print(f" {i}", end=" ")
                print(" "+" ".join([str(i) for i in lst[i]]))


# Подсчет живых кораблей
def check_result(field):
    ships = 0
    for i in field:
        for j in i:
            if j == 1: ships = ships+1
    return ships


# Ввод ячейки, проврека на соответствие
def process_input_val(cols,dimension):
    inp = ''

    def check_step(step_str):
        if len(step_str) < 2:
            return False
        if step_str[0] == "!":
            return True
        if step_str[0] not in cols:
            return False
        if step_str[1].isdigit() and 0 > int(step_str[1]) > dimension-1:
            return False
        return True
    while True:
        print("! - обозначение начала управляющей команды:\n\tq - закончить игру\n\ts - сохранить прогресс\nУкажите позицию выстрела (например b0), или управляющую команду:", end=" ")
        inp = input()
        if check_step(inp):
            break
        else:
            print("Позиция не соответсвует формату!")
    return inp


# Обработка
def process_command(command, field, cols, n_trys):
    msg = ""
    command = command.lower()
    if command[0] == "!":
        for i in range(1, len(command)):
            if command[i] == "s":
                save_state(field, n_trys)
                msg = "Сохранение!"
            if command[i] == "q":
                msg = "Выход!"
    else:
        i = int(command[1])
        j = cols[command[0]]
        field[i][j] = field[i][j]+2

        # Вывод сообщение о результате
        msg = "Промах!" if field[i][j] == 2 else "Попал!"
    return msg


# ----- Функции загрузки/сохранения прогресса
def save_state(field, n_trys):
    dump_str = {"Field": field, "Try`s": n_trys}
    with open("save.json", "wt") as f:
        dump(dump_str, f)


def load_state():
    try:
        with open("save.json", "rt") as f:
            obj = load(f)
        return obj
    except:
        return None
    

'''
Запуск основного цикла
dimension -  размер поля и количество объектов
n_trys - общее число допустимых промахов
debug_mode - Отладочный режим, если выставлен в True рядом с основным полем будет отображться расшифрованное поле с расстановкой объектов
'''


def start_game_cycle(dimension=10, n_trys=20, debug_mode=False):
    saved = load_state()
    field = make_field(dimension)
    if saved != None:
        print("Имеется сохраненный прогресс хотите продолжить [да/нет = по умолчанию]?", end =" ")
        inp = input()
        if inp == "да":
            field = saved["Field"]
            dimension = len(field[0])
            n_trys = saved["Try`s"] 

    cols = {chr(ord('a')+i): i for i in range(dimension)} #буквенные индексы колонок
    trys = n_trys
    result = dimension
    while trys > 0 :
        # Отрисовка игрового поля на текущем шаге
        print_field(field,cols,debug_mode)

        # Проверка результата, вывод статуса
        result = check_result(field)
        if result == 0:
            print("Вражеский флот уничтожен!")
            break
        else:
            print(f"Осталось уничтожить {result} кораблей, у вас {trys} попыток")
        
        message = process_command(process_input_val(cols,dimension),field,cols,n_trys)
        print(message)
        if message == "Промах!":
            trys = trys - 1
        if message == "Выход!":
            break 
        
    if trys == 0:
        print(f"У вас кончились попытки")   
    

if __name__ == "__main__":
    start_game_cycle(debug_mode=True)
