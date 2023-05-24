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


ap = FastAPI()

origins = [
    "http://localhost:3000",
]

ap.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ap.include_router(note.router, tags=['Notes'])


@ap.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}
