#todo:
#https://editor.ponyorm.com/user/nikolasov/lab_2_10_05_23/designer
#  Установить FLASK, установить SQLAlchemy
#  Настроить ORM на базу PostgresSQL
#  Для модели  БД "Система проверки задач" создать ORM модель. Сгенерировать ее в БД.
#  Переписать запросы с SQL на ORM


# https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application
# https://stackabuse.com/using-sqlalchemy-with-flask-and-postgresql/
# https://habr.com/ru/companies/yandex/articles/511892/

# Создать интерфейсы ввода GUI согласно бизнес логики.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert, select, update,Column
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user1:123@localhost:5432/check_tasks'
db = SQLAlchemy(app)


group_student = db.Table(
    'group_student',
    db.Column('id_groups', db.Integer(), db.ForeignKey('group.id',ondelete="CASCADE"), primary_key=True,nullable=False),
    db.Column('id_students', db.Integer(), db.ForeignKey('student.id',ondelete="CASCADE"), primary_key=True,nullable=False),
    db.Index("idx_group_student__id_students", "id_students")
)


teacher_group = db.Table(
    'teacher_group',
    db.Column('id_groups', db.Integer(), db.ForeignKey('group.id',ondelete="CASCADE"), primary_key=True,nullable=False),
    db.Column('id_teachers', db.Integer(), db.ForeignKey('teacher.id',ondelete="CASCADE"), primary_key=True,nullable=False),
    db.Index('idx_teacher_group__id_teachers','id_teachers')
)


task_student = db.Table(
    'task_student',
    db.Column('id_tasks', db.Integer(), db.ForeignKey('task.id',ondelete="CASCADE"), primary_key=True,nullable=False),
    db.Column('id_students', db.Integer(), db.ForeignKey('student.id',ondelete="CASCADE"), primary_key=True,nullable=False),
    db.Column('code', db.String()),
    db.Column('solved', db.Boolean(),nullable=False),
    db.Index('idx_task_student__id_students','id_students')
)


category_group = db.Table(
    'category_group',
    db.Column('id_categorys', db.Integer(), db.ForeignKey('category.id',ondelete="CASCADE"), primary_key=True, nullable=False),
    db.Column('id_groups', db.Integer(), db.ForeignKey('group.id',ondelete="CASCADE"), primary_key=True, nullable=False),
    db.Index("idx_category_group__id_groups", "id_groups")
)


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer(),primary_key=True, unique=True,autoincrement=True)
    id_category = db.Column(db.ForeignKey('category.id', ondelete="CASCADE"), nullable=False)
    id_task_students = db.relationship('Student',secondary=task_student, back_populates='id_task_students', uselist=False)
    status = db.Column(db.Integer)  # статус 1 - 10
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String, nullable=False)
db.Index('idx_task__id_category',Task.id_category)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id_task = db.relationship('Task', backref="category", uselist=False)
    id_teacher = db.Column(db.ForeignKey('teacher.id', ondelete="CASCADE"), nullable=False)
    id_category_groups = db.relationship('Group',secondary=category_group, back_populates='id_category_groups', uselist=False)
    name = db.Column(db.String(100),nullable=False)
db.Index('idx_category__id_teacher',Category.id_teacher)


class Teacher(db.Model):
    __tablename__= 'teacher'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id_teacher_groups = db.relationship('Group',secondary=teacher_group, back_populates='id_teacher_groups', uselist=False)
    name = db.Column(db.String(255),nullable=False)
    

class Student(db.Model):
    __tablename__= 'student'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id_task_students = db.relationship('Task',secondary=task_student, back_populates='id_task_students', uselist=False)
    id_student_groups = db.relationship('Group',secondary=group_student, back_populates='id_student_groups', uselist=False)
    name = db.Column(db.String(255),nullable=False)


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id_student_groups = db.relationship('Student', secondary=group_student,  back_populates='id_student_groups', uselist=False)
    id_teacher_groups = db.relationship('Teacher', secondary=teacher_group,  back_populates='id_teacher_groups', uselist=False)
    id_category_groups = db.relationship('Category',secondary=category_group, back_populates='id_category_groups', uselist=False)
    name = db.Column(db.String(50), nullable=False)


# 1 Список задач по категории
def select_task_list_by_category_id(identificator: int):
    return db.session.execute(select(Task.id, Task.name, Task.description)
                              .where(Task.id_category == identificator)).all()


def select_task_list_by_category_name(name: str):
    return db.session.execute(select(Task.id, Task.name, Task.description)
                              .join(Category).filter(Category.name == name)).all()


# 2 Список задач по сложности
def select_task_list_by_status(level: int):
    return db.session.execute(select(Task.id, Task.name, Task.status, Task.description)
                              .where(Task.status == level)).all()


# 3 Список задач по статусу решения
def select_all_tak_for_stud_by_id_solved_status(ident: int, solved: bool):
    return db.session.execute(select(Student.name, Task.name)
                              .join_from(task_student, Student)
                              .join_from(task_student, Task)
                              .filter(Student.id == ident)
                              .filter(task_student.c.solved == solved)
                              ).all()


# 4 Весь список задач для выбранного студента
def select_all_task_for_student_by_id(ident: int):
    return db.session.execute(select(Student.name, Task.name, task_student.c.solved)
                              .join_from(task_student, Student)
                              .join_from(task_student, Task)
                              .filter(Student.id == ident)
                              ).all()


# 5 Вывод списка групп по учителю
def select_groups_by_teacher(teacher_id: int):
    return db.session.execute(select(Group.id, Group.name, Teacher.name)
                              .join_from(teacher_group, Group)
                              .join_from(teacher_group, Teacher)
                              .filter(Teacher.id == teacher_id)
                              ).all()


# 6 Установить решение для студента по id
def update_solution_for_student_t_id(index: int, t_id: int, _code: str, _solved: bool):
    db.session.execute(update(task_student)
                       .where(task_student.c.id_students == index)
                       .where(task_student.c.id_tasks == t_id).values(code=_code, solved=_solved))
    db.session.commit()


# 7 Вывести общее число задач для студента
def count_task_bystudent_id(index: int):
    return len(select_all_task_for_student_by_id(index))


# Вывести число задача по статусу решения
def count_task_bystudent_id_solved(ident: int, solved: bool):
    return len(select_all_tak_for_stud_by_id_solved_status(ident, solved))


#  Вывести всех студентов по id группы
def select_all_students_by_group_id(group_id: int):
    return db.session.execute(select(Student.id, Student.name)
                              .join_from(group_student, Group)
                              .join_from(group_student, Student)
                              .filter(Group.id == group_id)
                              ).all()

# Общая успеваемость группы
def student_progress(student_id: int):
    # --- Процент решенных задач
    with app.app_context():
        try:
            full = count_task_bystudent_id(student_id)
            solved = count_task_bystudent_id_solved(student_id, True)
        except Exception as ex:
            print(ex)
        finally:
            print(f"Успеваемость студента id_{student_id} = {solved / (full * 0.01)}%")


def group_progress(group_id: int):
    with app.app_context():
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
    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
        except Exception as ex:
            print(ex)

        try:
            db.session.add(Teacher(id=1, name='Федоров Федер'))
            db.session.add_all([
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
            db.session.add_all([Group(name="А"),
                                Group(name="Б"),
                                Group(name="В")])
            db.session.commit()
            db.session.add_all([
                Category(name="1 - Вводная лекция", id_teacher=1),
                Category(name="2 - Основы SQL", id_teacher=1),
                Category(name="3 - Архитектура БД", id_teacher=1),
                Category(name="4 - Тест", id_teacher=1)])
            db.session.commit()
            db.session.add_all([
                Task(id_category=1, status=1, name="Д3_1", description="Ознакомиться с основными командами sql"),
                Task(id_category=2, status=1, name="Лаба_1", description="Настроить сервер базы данных"),
                Task(id_category=2, status=1, name="ДЗ_2",
                     description="Создать тестовую таблицу, реализовать несколько запросов SELECT"),
                Task(id_category=3, status=2, name="ДЗ_3",
                     description="Проработать архитектуру базы данных и реализовать заданные запросы"),
                Task(id_category=4, status=3, name="Тест_1", description="Решить тестовую задачу")])
            db.session.commit()
            with db.session.connection() as conn:
                conn.execute(
                    insert(teacher_group), [{'id_teachers': 1, 'id_groups': 1},
                                            {'id_teachers': 1, 'id_groups': 2},
                                            {'id_teachers': 1, 'id_groups': 3}],
                )
                conn.execute(
                    insert(group_student), [{'id_groups': 1, 'id_students': i} for i in range(1, 21, 3)] +
                                           [{'id_groups': 2, 'id_students': i} for i in range(2, 21, 3)] +
                                           [{'id_groups': 3, 'id_students': i} for i in range(3, 21, 3)],
                )
                conn.execute(
                    insert(category_group), [{'id_categorys': 1, 'id_groups': 1}] +
                                            [{'id_categorys': i, 'id_groups': 2} for i in range(1, 3)] +
                                            [{'id_categorys': i, 'id_groups': 3} for i in range(1, 5)],
                )
                conn.execute(
                    insert(task_student), [{'id_students': i, 'id_tasks': 1, 'solved': False} for i in
                                           range(1, 21, 3)] +  # Для студентов 1-й группы только первая задача
                                          [{'id_students': i, 'id_tasks': j, 'solved': False} for i in range(2, 21, 3)
                                           for j in range(1, 4)] +  # Для студентов 2-й все задачи для 2-х уроков
                                          [{'id_students': i, 'id_tasks': j, 'solved': False} for i in range(3, 21, 3)
                                           for j in range(1, 6)],
                )
                db.session.commit()
        except Exception as ex:
            print('----------')
            print(ex)


    # Тестируем селекты
    with app.app_context():
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

            q = db.session.execute(select(Task.id, Task.name, Task.status, Category.name, Task.description).join(Category)).all()
            for i in q:
                print(i)
        except Exception as ex:
            print(ex)
    group_progress(3)


