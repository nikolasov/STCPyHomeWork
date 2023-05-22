#todo:
# Необходимо разработать форму ввода тестовых вопросов пользователем в конструкторе форм https://beautifytools.com/html-form-builder.php
# Прикрутить форму к flask. Отдать флому  через шаблонизатор Jinja.
# При заполнении и отправки данных на сервер валидировать их и записать через модель ORM в PostgresSQL
from flask import render_template, redirect, url_for, request
from orm_db_app import app, db, select, Category,Task
import json


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/category_task',methods=['GET', 'POST'])
@app.route('/category_task/<string:vals>', methods=['GET', 'POST'])
def add_task(vals=""):
    page = 'pages/add_task.html'
    navigation = db.session.execute(select(Category.id,Category.name)).all()
    if vals!="" :
        status = json.loads(vals)
        return render_template(page,navigation = navigation,tinfo=status['tinfo'],status=status)
    return render_template(page,navigation = navigation,tinfo=0,status={"code":255,"id_cat":-1})


@app.route('/handler_form', methods=['GET', 'POST'])
def handler_form():
    id_cat=request.form["task_cat"]
    task_desc=request.form["task_desc"]
    task_name=request.form["task_name"]
    task_status=request.form["task_status"]
    status={"code":1,"msg":task_name + ": Успешная запись в базу !","tinfo":0,"id_cat":id_cat}
    try:
        if Task.query.where(Task.name == task_name).count() > 0:
            status['code'] = 2
            status['msg'] = "Задача "+task_name + ": Уже существует"
        else:
            with app.app_context():
                db.session.add(Task(id_category=id_cat, status=task_status, name=task_name, description=task_desc))
                db.session.commit()
    except Exception as ex:  
        status['code'] = 0
        status['msg'] = str(ex)
    
    
    return redirect(url_for('.add_task', vals=json.dumps(status)))


if __name__ == '__main__':
    app.run()
