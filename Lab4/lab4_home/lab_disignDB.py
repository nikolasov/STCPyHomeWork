#todo:
# Для вашего варианта системы разработать интерфейсы ввода данных и записать их в БД.
from flask import render_template, redirect, url_for, request
from orm_db_book_library import app, db,select,book_author,book_genre,book_publishing,select_books_by_name,select_books_by_author_id,select_books_by_genre_id,select_books_by_publish_id,select_all_genres,select_all_place ,select_all_publish, select_all_authors,Book,Genre,Author,Place,Publishing
import json
import orm_db_book_library as odbl

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/books',methods=['GET', 'POST'])
@app.route('/books/<string:vals>',methods=['GET', 'POST'])
def books(vals="",page='pages/books.html'):
    status = {"code":255}
    if vals!="" :
        status = json.loads(vals)
    status["authors"] = select_all_authors()
    status["publishs"] = select_all_publish()
    status["genres"] = select_all_genres()
    status["places"] = select_all_place()
    return render_template(page,status=status)

# --- Старница авторов
@app.route('/authors')
@app.route('/authors/<string:vals>',methods=['GET', 'POST'])
def authors(vals="",page='pages/authors.html'):
    status = {"code":255}
    if vals!="" :
        status = json.loads(vals)
    status["authors"] = select_all_authors()
    return render_template('pages/authors.html',status=status)

# --- Старница издателей
@app.route('/publishs/')
@app.route('/publishs/<string:vals>',methods=['GET', 'POST'])
def publishs(vals="",page = 'pages/publishs.html'):
    status = {"code":255}
    if vals!="" :
        status = json.loads(vals)
    status["publishs"] = select_all_publish()
    return render_template(page,status=status)

# --- Страница жанров
@app.route('/genres')
@app.route('/genres/<string:vals>',methods=['GET', 'POST'])
def genres(vals="",page = 'pages/genres.html'):
    status = {"code":255}
    if vals!="" :
        status = json.loads(vals)
    status["genres"] = select_all_genres()
    return render_template(page,status=status)

@app.route('/places')
@app.route('/places/<string:vals>',methods=['GET', 'POST'])
def places(vals="",page = 'pages/places.html'):
    status = {"code":255}
    if vals!="" :
        status = json.loads(vals)
    status["places"] = select_all_place()
    return render_template(page,status=status)


# Обработка форм 
@app.route('/add_publish',methods=['GET', 'POST'])
def add_publish():
    publish_name = request.form['publish_name']
    status={"code":1,"msg":publish_name + ": Успешная запись в базу !"}
    try:
        if Publishing.query.where(Publishing.name == publish_name).count()>0:
            status['code'] = 2
            status['msg'] = "Издатель "+publish_name + ": Уже существует"
        else:
            with app.app_context():
                db.session.add(Publishing(name=publish_name))
                db.session.commit()
    except Exception as ex:
        status['code'] = 0
        status['msg'] = str(ex)
    return redirect(url_for('.publishs', vals=json.dumps(status)))

@app.route('/add_author',methods=['GET', 'POST'])
def add_author():
    author_name = request.form['author_name']
    status={"code":1,"msg":author_name + ": Успешная запись в базу !"}
    try:
        if Publishing.query.where(Author.name == author_name).count()>0:
            status['code'] = 2
            status['msg'] = "Автор "+author_name + ": Уже существует"
        else:
            with app.app_context():
                db.session.add(Author(name=author_name))
                db.session.commit()
    except Exception as ex:
        status['code'] = 0
        status['msg'] = str(ex)

    return redirect(url_for('.authors', vals=json.dumps(status)))

@app.route('/add_genre',methods=['GET', 'POST'])
def add_genre():
    genre_name = request.form['genre_name']
    status={"code":1,"msg":"Жанр "+genre_name + ": Успешная запись в базу !"}
    try:
        if Genre.query.where(Genre.name == genre_name).count()>0:
            status['code'] = 2
            status['msg'] = ":Жанр "+genre_name + ": Уже существует"
        else:
            with app.app_context():
                db.session.add(Genre(name=genre_name))
                db.session.commit()
    except Exception as ex:
        status['code'] = 0
        status['msg'] = str(ex)

    return redirect(url_for('.genres', vals=json.dumps(status)))

@app.route('/add_place',methods=['GET', 'POST'])
def add_place():
    place_desc = request.form['place_desc']
    status={"code":1,"msg":"Место "+place_desc + ": Успешная запись в базу !"}
    try:
        if Place.query.where(Place.description == place_desc).count()>0:
            status['code'] = 2
            status['msg'] = ":Место "+place_desc + ": Уже существует"
        else:
            with app.app_context():
                db.session.add(Place(description=place_desc))
                db.session.commit()
    except Exception as ex:
        status['code'] = 0
        status['msg'] = str(ex)

    return redirect(url_for('.places', vals=json.dumps(status)))


@app.route('/add_book',methods=['GET', 'POST'])
def add_book():
    try:
        print(request.form)
        book_name = request.form['book_name'].strip()
        book_author_1 = request.form['book_author_1'].strip()
        book_author_2 = request.form['book_author_2'].strip()
        genre_name_1 = request.form['genre_name_1'].strip()
        genre_name_2 = request.form['genre_name_2'].strip()
        genre_name_3 = request.form['genre_name_3'].strip()
        place_desc = request.form['place_desc'].strip()
        publish_name = request.form['publish_name'].strip()

        #----- selected_fields
        sel_author_1 = request.form['author_selection_1']
        sel_author_2 = request.form['author_selection_2']
        sel_genre_1 = request.form['genre_selection_1']
        sel_genre_2 = request.form['genre_selection_2']
        sel_genre_3 = request.form['genre_selection_3']
        sel_place = request.form['place_selection']
        sel_publish = request.form['publish_selection']
    except Exception as ex:
        print(ex)
  
    
    status={"code":1,"msg":"Книга " + book_name + ": Успешная запись в базу !"}

    # У книги должно быть место и название
    if len(book_name) == 0 or len(place_desc) == 0:
        status['code'] = 2
        status['msg'] = "Не указано место или или название книги"
        return redirect(url_for('.books'), vals=json.dump(status))
    
    books_by_name = db.session.execute(select(Book.id, Place.description).join(Place).where(Book.name == book_name)).all()  
    ex_author1= db.session.execute(select(Author.name).where(Author.id == sel_author_1)).first()[0]
    ex_author2 = db.session.execute(select(Author.name).where(Author.id == sel_author_2)).first()[0]
    ex_genre1 = db.session.execute(select(Genre.name).where(Genre.id == sel_genre_1)).first()[0]
    ex_genre2 = db.session.execute(select(Genre.name).where(Genre.id == sel_genre_2)).first()[0]
    ex_genre3 = db.session.execute(select(Genre.name).where(Genre.id == sel_genre_3)).first()[0]
    ex_place = db.session.execute(select(Place.description).where(Place.id == sel_place)).first()[0]
    ex_publish = db.session.execute(select(Publishing.name).where(Publishing.id == sel_publish)).first()[0]
    
    # Если книга имеется в базе
    if len(books_by_name) >0:
        print("Book exist")
    # Если книга в базе отсутствует 
    else:
        try:
            id_place = odbl.check_place(place_desc,ex_place,sel_place)
            id_book = odbl.add_book(book_name,id_place)
             
            if len(publish_name)>0:
                id_pub = odbl.check_publish(publish_name,ex_publish,sel_publish)
                with app.app_context():
                    db.session.execute(odbl.insert(odbl.book_publishing),
                                       {'id_books':id_book, 'id_publishings':id_pub})
                    db.session.commit()
                status['msg'] = status['msg']+"\n"+" добавлено соответсвие с издателем "+publish_name
            if len(book_author_1)> 0:
                id_auth1 = odbl.check_author(book_author_1,ex_author1,sel_author_1)
                with app.app_context():
                    db.session.execute(odbl.insert(odbl.book_author),
                                       {'id_books':id_book, 'id_authors':id_auth1})
                    db.session.commit()
                status['msg'] = status['msg']+"\n"+" добавлено соответсвие с автором "+book_author_1
            
            if len(book_author_2)> 0:
                id_auth2 = odbl.check_author(book_author_2,ex_author2,sel_author_2)
                with app.app_context():
                    db.session.execute(odbl.insert(odbl.book_author),
                                       {'id_books':id_book, 'id_authors':id_auth2})
                    db.session.commit()
                status['msg'] = status['msg']+"\n"+" добавлено соответсвие с автором "+book_author_2
            
            if len(genre_name_1)> 0:
                id_gen1 = odbl.check_genre(genre_name_1,ex_genre1,sel_genre_1)
                with app.app_context():
                    db.session.execute(odbl.insert(odbl.book_genre),
                                       {'id_books':id_book, 'id_genres':id_gen1})
                    db.session.commit()        
                status['msg'] = status['msg']+"\n"+" добавлено соответсвие с жанром "+genre_name_1
            
            if len(genre_name_2)> 0:
                id_gen2 = odbl.check_genre(genre_name_2,ex_genre2,sel_genre_2)
                with app.app_context():
                    db.session.execute(odbl.insert(odbl.book_genre),
                                       {'id_books':id_book, 'id_genres':id_gen2})
                    db.session.commit()
                status['msg'] = status['msg']+"\n"+" добавлено соответсвие с жанром "+genre_name_2
            
            if len(genre_name_3)> 0:
                id_gen3 = odbl.check_genre(genre_name_3,ex_genre3,sel_genre_3)
                with app.app_context():
                    db.session.execute(odbl.insert(odbl.book_genre),
                                       {'id_books':id_book, 'id_genres':id_gen3})
                    db.session.commit()
                status['msg'] = status['msg']+"\n"+" добавлено соответсвие с жанром "+genre_name_3


        except Exception as ex:
            status['code'] = 0
            status['msg'] = str(ex)
    # Теперь запра
    return redirect(url_for('.books', vals=json.dumps(status)))

if __name__ == '__main__':
    app.run()