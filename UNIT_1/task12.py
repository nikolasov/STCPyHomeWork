# Написать игру "Поле чудес"

#Отгадываемые слова и описание лежат в разных  массивах по одинаковому индексу.
#words = ["оператор", "конструкция", "объект"]
#desc_  = [ "Это слово обозначает наименьшую автономную часть языка программирования", "..", ".." ]
#Пользователю выводится определение слова и количество букв в виде шаблона. Стиль шаблона может быть любым.
#Слово из массива берется случайным порядком. Принимая из ввода букву мы ее открываем
#в случае успеха а в случае неуспеха насчитывам штрафные балы. Игра продолжается до 10 штрафных баллов
#либо победы.
#
#Пример вывода:
#
#"Это слово обозначает наименьшую автономную часть языка программирования"
#
#▒  ▒  ▒  ▒  ▒  ▒  ▒  ▒
#
#Введите букву: O
#
#O  ▒  ▒  ▒  ▒  ▒  O  ▒
#
#
#Введите букву: Я
#
#Нет такой буквы.
#У вас осталось 9 попыток !
#Введите букву:
words = ["оператор","тест"]
desc_ = [ "Это слово обозначает наименьшую автономную часть языка программирования","Проверка корректности"]
stop_word = "!q"
game_step_message = "Введите букву или " + stop_word +" для окончания игры:"

# Проверка буквы
def check_template(literal, in_word, template, n_steps): 
    guess = False
    for i in range(len(in_word)):
        if in_word[i] == literal:
            guess = True
            template[i] = in_word[i]
    if not guess:
        n_steps-=1 
        
    return  n_steps

# Проверка отгадано ли слово
def check_result(out_template):
    for lit in out_template:
        if lit == "▒":
            return False
    return True

# Вывод итогового сообщения в зависимости от результата игры 
def get_result_mg(literal,n_steps,word):
    if literal == stop_word:
        return "Пропуск слова"
    else:
        if n_steps == 0:
            return "Провал! лимит попыток исчерпан"
        else:
            return "Успех! Слово - \n"+" ".join(l for l in word)
    
def start_game(id):
    if id >= len(words):
        return "Вышли за границы массива"
    n_steps     = 10
    word        = words[id]
    description = desc_[id]
    template    = ["▒"]*len(word)
    literal     = " "
    print(description)
    while (not check_result(template)) and n_steps>0 :
        print(" ".join(lit for lit in template))
        print(game_step_message, end=" ")
        literal = input()
        if literal == stop_word:
            break
        result = check_template(literal,word,template,n_steps)
        if result < n_steps:
            n_steps = result
            print("Нет такой буквы\nУ вас осталось " + str(n_steps) + " попыток!")
    return get_result_mg(literal,n_steps,word)
    
    
for i in range(len(words)):
    msg = start_game(i)
    print(msg)
    if i != len(words)-1:
          print("Хотите продолжить [да/нет]")
          if input()=="нет":
              break
        