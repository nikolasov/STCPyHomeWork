from .database import Base
import sqlalchemy as db
from sqlalchemy import MetaData


group_student = db.Table(
    'group_student',
    Base.metadata,
    db.Column('id_groups', db.Integer(), db.ForeignKey('group.id', ondelete="CASCADE"), primary_key=True, nullable=False),
    db.Column('id_students', db.Integer(), db.ForeignKey('student.id', ondelete="CASCADE"), primary_key=True, nullable=False),
    db.Index("idx_group_student__id_students", "id_students")
)

teacher_group = db.Table(
    'teacher_group',
    Base.metadata,
    db.Column('id_groups', db.Integer(), db.ForeignKey('group.id', ondelete="CASCADE"), primary_key=True, nullable=False),
    db.Column('id_teachers', db.Integer(), db.ForeignKey('teacher.id', ondelete="CASCADE"), primary_key=True, nullable=False),
    db.Index('idx_teacher_group__id_teachers', 'id_teachers')
)

task_student = db.Table(
    'task_student',
    Base.metadata,
    db.Column('id_tasks', db.Integer(), db.ForeignKey('task.id', ondelete="CASCADE"), primary_key=True, nullable=False),
    db.Column('id_students', db.Integer(), db.ForeignKey('student.id', ondelete="CASCADE"), primary_key=True, nullable=False),
    db.Column('code', db.String()),
    db.Column('solved', db.Boolean(), nullable=False),
    db.Index('idx_task_student__id_students', 'id_students')
)

category_group = db.Table(
    'category_group',
    Base.metadata,
    db.Column('id_categorys', db.Integer(), db.ForeignKey('category.id', ondelete="CASCADE"), primary_key=True, nullable=False),
    db.Column('id_groups', db.Integer(), db.ForeignKey('group.id', ondelete="CASCADE"), primary_key=True, nullable=False),
    db.Index("idx_category_group__id_groups", "id_groups")
)


class Task(Base):
    __tablename__ = 'task'
    id = db.Column(db.Integer(), primary_key=True, unique=True, autoincrement=True)
    id_category = db.Column(db.ForeignKey('category.id', ondelete="CASCADE"), nullable=False)
    id_task_students = db.orm.relationship('Student', secondary=task_student, back_populates='id_task_students', uselist=False)
    status = db.Column(db.Integer)  # статус 1 - 10
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String, nullable=False)


db.Index('idx_task__id_category', Task.id_category)


class Category(Base):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id_task = db.orm.relationship('Task', backref="category", uselist=False)
    id_teacher = db.Column(db.ForeignKey('teacher.id', ondelete="CASCADE"), nullable=False)
    id_category_groups = db.orm.relationship('Group', secondary=category_group, back_populates='id_category_groups', uselist=False)
    name = db.Column(db.String(100), nullable=False)


db.Index('idx_category__id_teacher', Category.id_teacher)


class Teacher(Base):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id_teacher_groups = db.orm.relationship('Group', secondary=teacher_group, back_populates='id_teacher_groups',uselist=False)
    name = db.Column(db.String(255), nullable=False)


class Student(Base):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id_task_students = db.orm.relationship('Task', secondary=task_student, back_populates='id_task_students', uselist=False)
    id_student_groups = db.orm.relationship('Group', secondary=group_student, back_populates='id_student_groups', uselist=False)
    name = db.Column(db.String(255), nullable=False)


class Group(Base):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id_student_groups = db.orm.relationship('Student', secondary=group_student, back_populates='id_student_groups', uselist=False)
    id_teacher_groups = db.orm.relationship('Teacher', secondary=teacher_group, back_populates='id_teacher_groups', uselist=False)
    id_category_groups = db.orm.relationship('Category', secondary=category_group, back_populates='id_category_groups', uselist=False)
    name = db.Column(db.String(50), nullable=False)


