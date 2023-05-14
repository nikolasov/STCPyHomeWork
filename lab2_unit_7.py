#https://editor.ponyorm.com/user/nikolasov/lab_2_10_05_23/designer
#todo:
#  БД "Система проверки задач"
# Описание предметной области. БД создается для информационного обслуживания учебного процесса.
# Преподаватель каждый урок выдает некоторое количество задач в качестве домашнего задания.
# Каждый ученик решает задачи и переводит ее в статус решенную выкладывая ее на Git
# Система, забирает задачу с Git'а и проверяет каждую задачу прогоняя ее через тесты и запуская ее в виртульном окружении
# и либо подтверждает ее статус как решенную либо возвращает сообщение об ошибки ( меняя ее статус как не решенную.)
#
#
# Разработайте систему с учетом бизнес сущностей:
# Группа, Преподаватель, Студент, Занятие, Задача
#
# Запросы:
#1. Выдавать список задач по категории (категориями являются темы занятий)
#2. Выдавать список задач по уровню сложности
#3. Выдавать список решенных и не решенных задач для слушателя
#4. Выдавать весь список задач выданный слушателю
#5. Выдавать список группы по преподавателю
#6. Предусмотреть возможность изменения статуса задачи для конкретного слушателя
#7. Выдавать процент решенных задач. (Соотношение между общим кол-вом и решенным)
#8. Выдавать процент успеваемости по всей группе.

#Система:
#1. Написать утилиту которая генерирует файлы taskN.py в папке classwork по номеру задачи.
#Задачи все храняться в БД.

import psycopg2

schema_string="""
CREATE TABLE "group" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(50) NOT NULL
);

CREATE TABLE "student" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(100) NOT NULL
);

CREATE TABLE "group_student" (
  "id_groups" INTEGER NOT NULL,
  "id_students" INTEGER NOT NULL,
  PRIMARY KEY ("id_groups", "id_students")
);

CREATE INDEX "idx_group_student__id_students" ON "group_student" ("id_students");

ALTER TABLE "group_student" ADD CONSTRAINT "fk_group_student__id_groups" FOREIGN KEY ("id_groups") REFERENCES "group" ("id") ON DELETE CASCADE;

ALTER TABLE "group_student" ADD CONSTRAINT "fk_group_student__id_students" FOREIGN KEY ("id_students") REFERENCES "student" ("id") ON DELETE CASCADE;

CREATE TABLE "teacher" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(100) NOT NULL
);

CREATE TABLE "category" (
  "id" SERIAL PRIMARY KEY,
  "id_teacher" INTEGER NOT NULL,
  "name" VARCHAR(100) NOT NULL
);

CREATE INDEX "idx_category__id_teacher" ON "category" ("id_teacher");

ALTER TABLE "category" ADD CONSTRAINT "fk_category__id_teacher" FOREIGN KEY ("id_teacher") REFERENCES "teacher" ("id") ON DELETE CASCADE;

CREATE TABLE "category_group" (
  "id_categorys" INTEGER NOT NULL,
  "id_groups" INTEGER NOT NULL,
  PRIMARY KEY ("id_categorys", "id_groups")
);

CREATE INDEX "idx_category_group__id_groups" ON "category_group" ("id_groups");

ALTER TABLE "category_group" ADD CONSTRAINT "fk_category_group__id_categorys" FOREIGN KEY ("id_categorys") REFERENCES "category" ("id") ON DELETE CASCADE;

ALTER TABLE "category_group" ADD CONSTRAINT "fk_category_group__id_groups" FOREIGN KEY ("id_groups") REFERENCES "group" ("id") ON DELETE CASCADE;

CREATE TABLE "task" (
  "id" SERIAL PRIMARY KEY,
  "id_category" INTEGER NOT NULL,
  "status" INTEGER,
  "name" VARCHAR(255) NOT NULL,
  "description" TEXT NOT NULL
);

CREATE INDEX "idx_task__id_category" ON "task" ("id_category");

ALTER TABLE "task" ADD CONSTRAINT "fk_task__id_category" FOREIGN KEY ("id_category") REFERENCES "category" ("id") ON DELETE CASCADE;

CREATE TABLE "task_student" (
  "id_tasks" INTEGER NOT NULL,
  "id_students" INTEGER NOT NULL,
  "code" TEXT,
  "solved" BOOLEAN NOT NULL,
  PRIMARY KEY ("id_tasks", "id_students")
);

CREATE INDEX "idx_task_student__id_students" ON "task_student" ("id_students");

ALTER TABLE "task_student" ADD CONSTRAINT "fk_task_student__id_students" FOREIGN KEY ("id_students") REFERENCES "student" ("id") ON DELETE CASCADE;

ALTER TABLE "task_student" ADD CONSTRAINT "fk_task_student__id_tasks" FOREIGN KEY ("id_tasks") REFERENCES "task" ("id") ON DELETE CASCADE;

CREATE TABLE "teacher_group" (
  "id_groups" INTEGER NOT NULL,
  "id_teachers" INTEGER NOT NULL,
  PRIMARY KEY ("id_groups", "id_teachers")
);

CREATE INDEX "idx_teacher_group__id_teachers" ON "teacher_group" ("id_teachers");

ALTER TABLE "teacher_group" ADD CONSTRAINT "fk_teacher_group__id_groups" FOREIGN KEY ("id_groups") REFERENCES "group" ("id") ON DELETE CASCADE;

ALTER TABLE "teacher_group" ADD CONSTRAINT "fk_teacher_group__id_teachers" FOREIGN KEY ("id_teachers") REFERENCES "teacher" ("id") ON DELETE CASCADE
"""

def make_insert_cmd(table_name, field, n_values):
    return "INSERT INTO \""+table_name+"\" "+field+" VALUES "+",".join(["%s" for i in range(n_values)])

f_1="(\"id\", \"name\")"

# тестовые данные для учителей
teacher_data = [f_1,[(1,"Федоров Федор")]]

# тестовые данные для студентов
student_data = [f_1,[(1,"Миронова Софья"),
                (2,"Андрианов Филипп"),
                (3,"Александров Лев"),
                (4,"Жданов Константин"),
                (5,"Бирюков Мирон"),
                (6,"Кошелева Елизавета"),
                (7,"Захаров Даниил"),
                (8,"Платонов Пётр"),
                (9,"Герасимов Даниил"),
                (10,"Моисеев Мирон"),
                (11,"Ермаков Иван"),
                (12,"Григорьев Кирилл"),
                (13,"Иванова Ксения"),
                (14,"Попова София"),
                (15,"Владимиров Денис"),
                (16,"Власов Константин"),
                (17,"Ковалева Виктория"),
                (18,"Петров Сергей"),
                (19,"Поляков Макар"),
                (20,"Егорова Елизавета"),
                ]]

#тестовые данные группы
group_data = [f_1,[(1,"А"),(2,"Б"),(3,"В")]]

#тестовые для уроков
category_data = ["(\"id\",\"name\",\"id_teacher\")",[
              (1,"1 - Вводная лекция",1),
              (2,"2 - Основы SQL",1),
              (3,"3 - Архитектура БД",1),
              (4,"4 - Тест",1)
]]

#тестовые данные задач
task_data = ["(\"id\",\"id_category\",\"status\",\"name\",\"description\")",[
            (1,1,1,"Д3_1","Ознакомиться с основными командами sql"),
            (2,2,1,"Лаба_1","Настроить сервер базы данных"),
            (3,2,1,"ДЗ_2","Создать тестовую таблицу, реализовать несколько запросов SELECT"),
            (4,3,2,"ДЗ_3","Проработать архитектуру базы данных и реализовать заданные запросы"),
            (5,4,3,"Тест_1","Решить тестовую задачу")
            ]]

#Все группы у одного учителя
teacher_group_data = ["(\"id_teachers\",\"id_groups\")",[
              (1,1),
              (1,2),
              (1,3)
]]

#Распределяем студентов по группам
group_student_data = ["(\"id_groups\",\"id_students\")",
                      [(1,i) for i in range(1,21,3)] + 
                      [(2,i) for i in range(2,21,3)] +
                      [(3,i) for i in range(3,21,3)]]

# Допустим 1-я группа прослушала одну лекцию 
#          2-я две лекции
#          3-я все лекции
category_group_data = ["(\"id_categorys\",\"id_groups\")",
                     [(1,1)] +
                     [(i,2) for i in range(1,3)] +
                     [(i,3) for i in range(1,5)]]

#Задачи и студенты
task_student_data = ["(\"id_students\",\"id_tasks\",\"solved\")",
                     [(i,1,False) for i in range(1,21,3)] + # Для студентов 1-й группы только первая задача
                     [(i,j,False) for i in range(2,21,3) for j in range(1,4)]+ # Для студентов 2-й все задачи для 2-х уроков
                     [(i,j,False) for i in range(3,21,3) for j in range(1,6)] # Для все задачаи
                     ]

vals = {
        "teacher":teacher_data,
        "category":category_data,
        "student":student_data,
        "group":group_data,
        "task":task_data,
        "teacher_group":teacher_group_data,
        "group_student":group_student_data,
        "category_group":category_group_data,
        "task_student":task_student_data
        }

#1 Список задач по категории
def select_task_list_by_category_id(identificator:int):
    return f"""SELECT "id", "name", "description" FROM task WHERE id_category = {identificator}"""
def select_task_list_by_category_name(name:str):
    return f"""SELECT "id", "name", "description" FROM task t WHERE EXISTS ( SELECT 1 FROM category c WHERE t.id_category = c.id AND c.name = '{name}') """

#2 Список задач по сложности
def select_task_list_by_status(level:int):
    return f"""SELECT "id", "name", "status", "description" FROM task WHERE status = {level}"""

#3 Список задач по статусу решения
def select_all_tak_for_stud_by_id_solved_status(ident:int,solved:bool):
    return f"""
    SELECT s.name, t.name 
    FROM task t
    JOIN task_student ts ON ts.id_students = {ident} AND ts.solved = {solved} AND ts.id_tasks = t.id
    JOIN student s ON s.id = {ident}
    """

#4 Весь список задач для выбранного студента
def select_all_task_for_student_by_id(ident:int):
    return f"""
      SELECT s.name, t.name, ts.solved
      FROM task t
      JOIN task_student ts ON ts.id_students = {ident} AND ts.id_tasks = t.id
      JOIN student s ON s.id = {ident}"""

#5 Вывод списка групп по учителю
def select_groups_by_teacher(teacher_id:int):
    return f"""SELECT g.id, g.name, t.name
    FROM "group" g
    JOIN teacher_group tg ON tg.id_teachers = {teacher_id} AND tg.id_groups = g.id
    JOIN teacher t ON t.id = {teacher_id}"""     

#6 Установить решение для студента по id
def update_solution_for_student_t_id(index:int, t_id:int, code:str, solved:bool):
    return f"""
    UPDATE task_student SET solved = {solved}, code = '{code}' WHERE id_students = {index} AND id_tasks = {t_id}
    """

#7 Вывести общее число задач для студента
def count_task_bystudent_id(index:int):
    return f"""
    SELECT COUNT(*)
    FROM task t
    JOIN task_student ts ON ts.id_students = {index} AND ts.id_tasks = t.id
    JOIN student s ON s.id = {index}
    """

# Вывести число задача по статусу решения
def count_task_bystudent_id_solved(ident:int,solved:bool):
    return f"""
    SELECT COUNT(*)
    FROM task t
    JOIN task_student ts ON ts.id_students = {ident} AND ts.solved = {solved} AND ts.id_tasks = t.id
    JOIN student s ON s.id = {ident}
    """
#  Вывести всех студентов по id группы
def select_all_students_by_group_id(group_id:int):
    return f"""
    SELECT s.id, s.name
    FROM student s
    JOIN group_student gs ON s.id = gs.id_students AND gs.id_groups = {group_id} 
    """

test_selects = [select_task_list_by_category_id(2),
                select_task_list_by_category_name("2 - Основы SQL"),
                select_task_list_by_status(1),
                select_task_list_by_status(2),
                select_all_task_for_student_by_id(3),
                select_groups_by_teacher(1),
                select_all_tak_for_stud_by_id_solved_status(3,True),
                select_all_tak_for_stud_by_id_solved_status(3,False),
                select_all_students_by_group_id(3)]

def student_progress(conn, student_id:int):
  # --- Процент решенных задач
    with conn.cursor() as cur:
        try:
            cur.execute(count_task_bystudent_id(student_id))
            full = cur.fetchone()
            cur.execute(count_task_bystudent_id_solved(student_id,True))
            solved = cur.fetchone()
        except Exception as ex:
            print(ex)
        finally:
            print(f"Успеваемость студента id_{student_id} = { solved[0] / (full[0]*0.01)}%")
        conn.commit()    

def group_progress(conn, group_id:int):
    with conn.cursor() as cur:
      try:  
        cur.execute(select_all_students_by_group_id(3))
        students = cur.fetchall()
        solved_count = 0
        cur.execute(count_task_bystudent_id(students[0][0]))
        task_count = len(students)*(cur.fetchone()[0])
        for val in students:
            cur.execute(count_task_bystudent_id_solved(val[0],True))
            solved_count+= (cur.fetchone())[0]
      except Exception as ex:
          print(ex)
      finally:
          print(f"Успеваемость группы id_3{3}= {  solved_count/(task_count*0.01)}%")
          print("--------------")
          for stud in students:
              print(stud[1], end=": ")
              student_progress(conn,stud[0])

with psycopg2.connect("dbname=test user=psql_user password=12345678") as conn:
    
    # --- Создаем схему базы
    with conn.cursor() as cur:
        try:
            cur.execute(schema_string)
        except Exception as ex:
            print(ex)
            conn.commit()
            
        conn.commit() 

    # --- Заполняем схему 
    with conn.cursor() as cur:
      for key,val in vals.items():
          try:
              cur.execute(make_insert_cmd(key,val[0],len(val[1])),val[1])
          except Exception as ex : print(ex)
          conn.commit() 
    
    # --- Делаем тестовые выборки 
    with conn.cursor() as cur:
      for cmd in test_selects:
        try:
            cur.execute(cmd)
        except Exception as ex:
            print(ex)
        finally:
            for row in cur.fetchall():
                print(row)
        conn.commit()     
        print("------------------")
    
    #Общая успеваемость группы
    group_progress(conn, 3)

    
          
      
        
    
      