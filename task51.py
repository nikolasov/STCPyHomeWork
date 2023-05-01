#todo:
# Определите класс Person. При создании объекта p=Person(‘Иванов’, ‘Михаил’, ‘Федорович’) необходимо ввести полное имя человека.
# При печати объекта должно выводиться следующее:
# print(p) # чивородеФлиахиМвонавИ
class Person:
    def __init__(self, name, second_name, son_of):
        if type(name) != type(str()) or \
            type(second_name) != type(str()) or \
            type(son_of) != type(str()):
            print("Полное имя должно состоять из строк")
            return
        
        print("".join(list(reversed(name+second_name+son_of))))


p = Person('Иванов', 'Михаил', 'Федорович')