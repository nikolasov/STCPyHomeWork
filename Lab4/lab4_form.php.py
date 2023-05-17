#todo:
# Необходимо разработать форму ввода тестовых вопросов пользователем в конструкторе форм https://beautifytools.com/html-form-builder.php
# Прикрутить форму к flask. Отдать флому  через шаблонизатор Jinja.
# При заполнении и отправки данных на сервер валидировать их и записать через модель ORM в PostgresSQL
from flask import render_template
from app import app, db, group_progress

#group_progress(3)
@app.route('/')
@app.route('/index.html')
def index():

    return render_template('add_task.html')

if __name__ == '__main__':
    app.run()