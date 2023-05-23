#todo:
# Установить фреймворк  fast-api, библиотеку SQLAlchemy и pydantic
# https://fastapi.tiangolo.com/
# https://www.sqlalchemy.org/
# https://docs.pydantic.dev/latest/


#Настроить проект аналогично статье:
#https://codevoweb.com/build-a-crud-app-with-fastapi-and-sqlalchemy/
#
#1. Написать CRUD для системы тестирования. Реализовать роутеры:
#
#GET	/api/tests	Retrieve all tests
#POST	/api/tests	Add a new test
#GET	/api/tests/{testId}	Get a single test
#PATCH	/api/tests/{testId}	Edit a test
#DELETE	/api/tests/{testId} Remove a test
#
#3. Прикруить к роутерам ранее спроектированую  ORM модель системы тестирования.
#4. Настроить взаимодействие с БД и вернуть клиенту json с данными.
import app.models as models
import app.note as note
from fastapi import FastAPI
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db
from app.models import Category,Task,Group,Student,Teacher,group_student,category_group,task_student,teacher_group
from sqlalchemy import insert, select, update
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(note.router, tags=['Notes'])


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}

db = SessionLocal()
# 1 Список задач по категории
def select_task_list_by_category_id(identificator: int):
    return db.execute(select(Task.id, Task.name, Task.description)
                              .where(Task.id_category == identificator)).all()


def select_task_list_by_category_name(name: str):
    return db.execute(select(Task.id, Task.name, Task.description)
                              .join(Category).filter(Category.name == name)).all()


# 2 Список задач по сложности
def select_task_list_by_status(level: int):
    return db.execute(select(Task.id, Task.name, Task.status, Task.description)
                              .where(Task.status == level)).all()


# 3 Список задач по статусу решения
def select_all_tak_for_stud_by_id_solved_status(ident: int, solved: bool):
    return db.execute(select(Student.name, Task.name)
                              .join_from(task_student, Student)
                              .join_from(task_student, Task)
                              .filter(Student.id == ident)
                              .filter(task_student.c.solved == solved)
                              ).all()


# 4 Весь список задач для выбранного студента
def select_all_task_for_student_by_id(ident: int):
    return db.execute(select(Student.name, Task.name, task_student.c.solved)
                              .join_from(task_student, Student)
                              .join_from(task_student, Task)
                              .filter(Student.id == ident)
                              ).all()


# 5 Вывод списка групп по учителю
def select_groups_by_teacher(teacher_id: int):
    return db.execute(select(Group.id, Group.name, Teacher.name)
                              .join_from(teacher_group, Group)
                              .join_from(teacher_group, Teacher)
                              .filter(Teacher.id == teacher_id)
                              ).all()


# 6 Установить решение для студента по id
def update_solution_for_student_t_id(index: int, t_id: int, _code: str, _solved: bool):
    db.execute(update(task_student)
                       .where(task_student.c.id_students == index)
                       .where(task_student.c.id_tasks == t_id).values(code=_code, solved=_solved))
    db.commit()


# 7 Вывести общее число задач для студента
def count_task_bystudent_id(index: int):
    
    return len(select_all_task_for_student_by_id(index))


# Вывести число задача по статусу решения
def count_task_bystudent_id_solved(ident: int, solved: bool):
    return len(select_all_tak_for_stud_by_id_solved_status(ident, solved))


#  Вывести всех студентов по id группы
def select_all_students_by_group_id(group_id: int):
    return db.execute(select(Student.id, Student.name)
                              .join_from(group_student, Group)
                              .join_from(group_student, Student)
                              .filter(Group.id == group_id)
                              ).all()

# Общая успеваемость группы
def student_progress(student_id: int):
    # --- Процент решенных задач
    try:
        full = count_task_bystudent_id(student_id)
        solved = count_task_bystudent_id_solved(student_id, True)
    except Exception as ex:
        print(ex)
    finally:
        print(f"Успеваемость студента id_{student_id} = {solved / (full * 0.01)}%")


def group_progress(group_id: int):
    try:
        update_solution_for_student_t_id(3, 1, "My_solution", True)
        students = select_all_students_by_group_id(3)
        solved_count = 0
        task_count = len(students) * (count_task_bystudent_id(students[0][0]))
        for val in students:
            solved_count += count_task_bystudent_id_solved(val[0], True)
    except Exception as ex:
        print(ex)
    finally:
        print(f"Успеваемость группы id_3{3}= {solved_count / (task_count * 0.01)}%")
        print("--------------")
        for stud in students:
            print(stud[1], end=": ")
            student_progress(stud[0])




if __name__ == '__main__':
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(bind=engine)
    models.Base.metadata.create_all(engine,tables=[group_student, 
                                               category_group, 
                                               task_student,
                                               teacher_group]) 
    db.add(Teacher(id=1, name='Федоров Федер'))
    db.add_all([
        Student(name="Миронова Софья"),
        Student(name="Андрианов Филипп"),
        Student(name="Александров Лев"),
        Student(name="Жданов Константин"),
        Student(name="Бирюков Мирон"),
        Student(name="Кошелева Елизавета"),
        Student(name="Захаров Даниил"),
        Student(name="Платонов Пётр"),
        Student(name="Герасимов Даниил"),
        Student(name="Моисеев Мирон"),
        Student(name="Ермаков Иван"),
        Student(name="Григорьев Кирилл"),
        Student(name="Иванова Ксения"),
        Student(name="Попова София"),
        Student(name="Владимиров Денис"),
        Student(name="Власов Константин"),
        Student(name="Ковалева Виктория"),
        Student(name="Петров Сергей"),
        Student(name="Поляков Макар"),
        Student(name="Егорова Елизавета")])
    db.add_all([Group(name="А"),
                Group(name="Б"),
                Group(name="В")])
    db.commit()
    db.add_all([
                Category(name="1 - Вводная лекция", id_teacher=1),
                Category(name="2 - Основы SQL", id_teacher=1),
                Category(name="3 - Архитектура БД", id_teacher=1),
                Category(name="4 - Тест", id_teacher=1)])
    db.commit()
    db.add_all([
        Task(id_category=1, status=1, name="Д3_1", description="Ознакомиться с основными командами sql"),
        Task(id_category=2, status=1, name="Лаба_1", description="Настроить сервер базы данных"),
        Task(id_category=2, status=1, name="ДЗ_2",
             description="Создать тестовую таблицу, реализовать несколько запросов SELECT"),
        Task(id_category=3, status=2, name="ДЗ_3",
             description="Проработать архитектуру базы данных и реализовать заданные запросы"),
        Task(id_category=4, status=3, name="Тест_1", description="Решить тестовую задачу")])
    db.commit()
    db.execute(
        insert(models.teacher_group), [{'id_teachers': 1, 'id_groups': 1},
                                            {'id_teachers': 1, 'id_groups': 2},
                                            {'id_teachers': 1, 'id_groups': 3}],
                )
    db.execute(
        insert(models.group_student), [{'id_groups': 1, 'id_students': i} for i in range(1, 21, 3)] +
                               [{'id_groups': 2, 'id_students': i} for i in range(2, 21, 3)] +
                               [{'id_groups': 3, 'id_students': i} for i in range(3, 21, 3)],
    )
    db.execute(
        insert(models.category_group), [{'id_categorys': 1, 'id_groups': 1}] +
                                [{'id_categorys': i, 'id_groups': 2} for i in range(1, 3)] +
                                [{'id_categorys': i, 'id_groups': 3} for i in range(1, 5)],
    )
    db.execute(
        insert(models.task_student), [{'id_students': i, 'id_tasks': 1, 'solved': False} for i in
                               range(1, 21, 3)] +  # Для студентов 1-й группы только первая задача
                              [{'id_students': i, 'id_tasks': j, 'solved': False} for i in range(2, 21, 3)
                               for j in range(1, 4)] +  # Для студентов 2-й все задачи для 2-х уроков
                              [{'id_students': i, 'id_tasks': j, 'solved': False} for i in range(3, 21, 3)
                               for j in range(1, 6)],
    )
    db.commit()

    tests = [select_task_list_by_category_id(2)
            , select_task_list_by_category_name("2 - Основы SQL")
            , select_task_list_by_status(1)
            , select_task_list_by_status(2)
            , select_all_task_for_student_by_id(3)
            , select_groups_by_teacher(1)
            , select_all_tak_for_stud_by_id_solved_status(3, True)
            , select_all_tak_for_stud_by_id_solved_status(3, False)
            , select_all_students_by_group_id(3)
                 ]
    try:
        for t in tests:
            for v in t:
                print(v)
            print("---------------")
        q = db.query(Task.id, Task.name, Task.status, Category.name, Task.description).join(Category).all()
        for i in q:
            print(i)
    except Exception as ex:
        print(ex)
    group_progress(3)