#todo:
# Необходимо разработать форму ввода тестовых вопросов пользователем в конструкторе форм https://beautifytools.com/html-form-builder.php
# Прикрутить форму к flask. Отдать флому  через шаблонизатор Jinja.
# При заполнении и отправки данных на сервер валидировать их и записать через модель ORM в PostgresSQL
from flask import render_template, request
from app import app, db, group_progress, select, Category

#group_progress(3)
@app.route('/')
@app.route('/index.html')
def index():
    navigation = db.session.execute(select(Category.id,Category.name)).all()
    print(navigation)
    return render_template('add_task.html',navigation = navigation)


@app.route('/handler_form', methods=['GET', 'POST'])
def handler_form():
    return request.form['select-1684343059734']

if __name__ == '__main__':
    app.run()
