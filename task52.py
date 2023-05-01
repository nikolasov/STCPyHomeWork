#todo:
#  Разработать систему учета решения задач учениками курса «Разработчик на Питоне».
#
# Проблема.
# Преподаватель каждый урок задает некоторое количество задач в качестве домашнего задания, для упрощения можно считать, что одну.
# Каждый ученик решает каждую задачу. Переводит ее статус в решенную.
# Преподаватель проверяет каждую задачу каждого ученика и либо подтверждает ее статус как решенную или меняет ее статус как не решенную.
# Вопрос. Как спроектировать систему классов на Питоне для решения задачи учета?
# Разработайте систему
# классов (Teacher, Pupil, Lesson, Task. Нужен ли класс Группа?);
# атрибутов для каждого состояния каждого объекта;
# методов для каждого объекта.
# Отчетность? Запросы? Начните с формулировки решаемой задачи – спецификации или технического задания. Затем спроектируйте классы, атрибуты, методы. Протестируйте систему.
import random as rnd


""" Базовый класс для всех следующих классов
Id обеспечивает хранение и доступ к полю id, принимает уникальный для класса идентификатор
"""


class Id:
    def __init__(self, _id) -> None:
        self.__id = _id
    
    def __setattr__(self, name: str, value: int) -> None:
        if name == '_id':
            if name not in self.__dict__:
                    self.__dict__[name] = value
        else:
            self.__dict__[name] = value
    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, v):
        pass


""" Класс задача
Хранит поля:
description - описание задачи
status - статус решения задачи [no_solution, solution, solution_accepted, solution_not_accepted]
    ученик может только предложить решение, т.е указать статус solution при помощи метода set_solution
    если для задача задан id  проверяющего тогда статус результата проверки задачи сможет поставить только учитель с соответсвующим id
    методы: set_not_accepted,set_accepted
teacher_comment - коментарий проверяющего учителя
"""


class Task(Id):
    index = 0

    def __init__(self, desc="", orig=None) -> None:
        if orig is None:
            Task.index = Task.index + 1
            super().__init__(Task.index)
            self.__description = desc
        else:
            if isinstance(orig,Task):
                super().__init__(orig.id)
                self.__description = orig.__description
                if 'teacher_id' in orig.__dict__:
                    self.teacher_id = orig.teacher_id
        
        self.__status = "no_solution"
        self.__teacher_comment = ""

    def set_teacher(self, person):
        if isinstance(person, Teacher):
            self.teacher_id = person.id

    def set_solution(self, person):
        if isinstance(person,Pupil):
            if self.__status != "solution_accepted":
                self.__status = "solution"
    
    def set_accepted(self, person, comment=""):
        if isinstance(person, Teacher):
            if 'teacher_id' in self.__dict__:
                if self.teacher_id == person.id:
                    self.__status = "solution_accepted"
                    self.__teacher_comment = comment
            else:
                self.__status = "solution_accepted"
                self.__teacher_comment = comment
    
    def set_not_accepted(self, person, comment=""):
        if isinstance(person, Teacher):
            if 'teacher_id' in self.__dict__:
                if self.teacher_id == person.id:
                    self.__status = "solution_not_accepted"
                    self.__teacher_comment = comment
            else:
                self.__status = "solution_not_accepted"
                self.__teacher_comment = comment
    
    def isstatus(self, status):
        if type(status) != type(str()):
            return False
        return status == self.__status
    
    def status(self):
        return self.__status
    
    def description(self):
        return self.__description
    
    def comment(self):
        return self.__teacher_comment
    
    def __str__(self):
        show_str = str(f"t{self.id}.")
        if self.__description != "":
            show_str = show_str+str(f" {self.__description}")
        if self.__status != "":
            show_str = show_str+str(f" [{self.__status}]")
        if self.__teacher_comment != "":
            show_str = show_str+str(f"\nComment: {self.__teacher_comment}")

        return show_str
    
    def __eq__(self, obj) -> bool:
        if isinstance(obj,Task):
            return self.id == obj.id
        return False


""" Контейнер для хранения списка домашних задач
"""


class Lesson(Id):
    index = 0

    def __init__(self, desc="") -> None:
        Lesson.index = Lesson.index + 1
        super().__init__(Lesson.index)
        self.__description = desc
        self.__task_list = []
    
    def add_tasks(self, person, *args):
        if isinstance(person, Teacher):
            for i in args:
                if isinstance(i, Task):
                    i.set_teacher(person)
                    self.__task_list.append(i)
    
    def clear_tasks(self, person):
        if isinstance(person, Teacher):
             self.__task_list.clear()
    
    def __str__(self):
        head = str(f"{self.__description}\nСписок домашних задач:\n\t")
        return head + "\n\t".join(str(f"[{i}]:{self.__task_list[i].description()}") for i in range(len(self.__task_list)))
    
    def home_tasks_size(self):
        return len(self.__task_list)
    
    def get_task(self, i_d):
        if type(i_d) == type(int) and i_d <= (len(self.__task_list)-1):
                return self.__task_list[i_d]
        
    def tasks(self):
        return self.__task_list


""" Общий класс для учителя и ученика
храни поля ФИО и обеспечивает к ним доступ
"""


class Person(Id):
    index = 0

    def __init__(self, _id, fname, sname, sonof) -> None:
        super().__init__(_id)
        self.__name = fname
        self.__sname = sname
        self.__sonof = sonof
       
    @property
    def name(self):
        return self.__name

    @property
    def sname(self):
        return self.__sname

    @property
    def sonof(self):
        return self.__sonof
    
    @name.setter
    def name(self, val):
        pass

    @sname.setter
    def sname(self, val):
        pass

    @sonof.setter
    def sonof(self, val):
        pass

    def __str__(self) -> str:
        return str(f"{self.sname} {self.name} {self.sonof}")
    
    def str_plus_id(self):
        return str(f"p{self.id}. {self}")


"""Ученик 
дополнительно к поля ФИО хранит список ДЗ, которые он должен решить
"""


class Pupil(Person):
    index = 0

    def __init__(self, fname, sname, sonof) -> None:
        Pupil.index = Pupil.index + 1
        super().__init__(Pupil.index, fname, sname, sonof)
        self.__task_dict = dict()
    
    def set_tasks(self, *args):
        for i in args:
            if isinstance(i, Task):
                    self.__task_dict[i.id] = Task(orig=i)
        
    def set_task_list(self, task_list):
        for i in task_list:
            if isinstance(i, Task):
                    self.__task_dict[i.id] = Task(orig=i)

    def __str__(self) -> str:
        return "Ученик: " + super().__str__() #+ ("\n" if len(self.__task_dict)!=0 else "") + "\n".join([str(i) for i in self.__task_dict.values()])

    def home_work_nfo(self) -> str:
        return "Ученик: " + super().__str__() + ("\n" if len(self.__task_dict)!=0 else "") +"\n".join([str(i) for i in self.__task_dict.values()])

    def print_task(self, task_id):
        if task_id in self.__task_dict:
            return str(self.__task_dict[task_id])
        return ""

    def get_task(self, task_id):
        if task_id in self.__task_dict:
            return self.__task_dict[task_id]
        return None

    def get_all_task(self):
        return self.__task_dict


"""Учитель 
дополнительно к полям ФИО хранит список уроков которые он провел 
хранит словарь групп студентов
"""   

class Teacher(Person):
    index = 0

    def __init__(self, fname, sname, sonof) -> None:
        Teacher.index = Teacher.index + 1
        super().__init__(Teacher.index, fname, sname, sonof)
        self.__course = []
        self.__groups = dict()
    
    def init_lesson(self, desc, *args):
        less = Lesson(desc)
        less.add_tasks(self,*args)
        self.__course.append(less)

    def full_course_str(self):
        return "\n".join(str(i) for i in self.__course)
    
    def group_list(self):
        return self.__groups.keys()
    
    def less_size(self):
        return len(self.__course)
    
    def less_info(self, less_id):
        if less_id >= len(self.__course):
            print("Id урока вне диапазона значений")
            return
        return str(self.__course[less_id])
    
    def set_home_for_group(self, group_name, less_id):
        if group_name in self.__groups:
            for i in self.__groups[group_name]:
                self.set_tasks_for_pupil(i, less_id)

    def set_tasks_for_pupil(self, pupil, less_id):
        if not isinstance(pupil, Pupil):
            return
        if less_id >= len(self.__course):
            print("Id урока вне диапазона значений")
            return
        pupil.set_task_list(self.__course[less_id].tasks())
    
    def init_from_group_list(self, group_name, pup_list):
        if type(pup_list) == type(list()):
            self.__groups[group_name] = pup_list

    def init_group(self,group_name, *args):
        self.__groups[group_name] = []
        for i in args:
            if isinstance(i, Pupil):
                self.__groups[group_name].append(i)

    def get_group_list(self, group_name):
        if group_name in self.__groups:
            return self.__groups[group_name]
        return None

    def get_tasks_for_course(self, course_id):
        if course_id >= len(self.__course):
            return None
        return self.__course[course_id].tasks()
            


group_1 = [Pupil("Иван","Иванов","Иванович"),Pupil("Леонид","Леонидов","Леонидович"),Pupil("Олег","Олегов","Олегович")]

print("----------------------------------")
t = Teacher("Петр","Петров","Петрович")
t.init_lesson("Вводный Урок: основы ООП в Python",
              Task("Создать первый класс"), 
              Task("Создать простую иерархию наследования из трех классов"))
t.init_from_group_list(1, group_1)
#Выводим список домашки у каждого из группы
print("---------Список группы-----------------")
for i in group_1:
    print(i.home_work_nfo())

#Задаем группе домашку по уроку
print("--------- "+str(t)+" задает группе домашку")
print("--------- В списке учеников добавились нерешенные задачи ------------")
t.set_home_for_group(1,0)
for i in group_1:
    print(i.home_work_nfo())

#Допустим все в группе предложили решение по домашке
print("-------- Ученики представили свои решения")
print("-------- Статус решения задачи в квадратных скобках  изменился  ------------")
for pup in group_1:
    for key,val in pup.get_all_task().items():
        val.set_solution(group_1[0])
for i in group_1:
    print(i.home_work_nfo())

print("-------Учитель проверяет заданные задачи-------")
print("-------Результат проверки статус задач изменился [accepted/not_accepted]. После каждой задачи появился коментарий учителя-------")
#Будучи учителем просматриваем  задачки принимаем или нет
for task in t.get_tasks_for_course(0):
    for p in t.get_group_list(1):
        task_p = p.get_task(task.id)
        if rnd.randint(0, 1) == 1:
            task_p.set_accepted(t, "Принято")
        else:
            task_p.set_not_accepted(t, "Нужно переделать")
for i in group_1:
    print(i.home_work_nfo())

print("------ Учитель может вывести весь результат по уроку и по группе ")
print(t.less_info(0))
print("Группа 1:")
for task in t.get_tasks_for_course(0):
    for p in t.get_group_list(1):
        task_p = p.get_task(task.id)
        print(p)
        print(task_p)
