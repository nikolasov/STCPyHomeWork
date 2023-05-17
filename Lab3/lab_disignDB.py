#todo:
#https://editor.ponyorm.com/user/nikolasov/home_unit_7_v12/designer
# Для модели вашего варианта БД создать ORM модель в SQLAlchemy. Сгенерировать ее в БД.
# Переписать запросы с SQL на ORM. 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert, select, update
import random
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://psql_user:12345678@localhost:5432/library_book'
db = SQLAlchemy(app)

book_author = db.Table(
    'book_author',
    db.Column('id_books',db.Integer(), db.ForeignKey('book.id',ondelete="CASCADE"), primary_key=True,nullable=False),
    db.Column('id_authors',db.Integer(), db.ForeignKey('author.id',ondelete="CASCADE"), primary_key=True,nullable=False),
    db.Index('idx_book_author__id_authors','id_authors')
)

book_genre = db.Table(
    'book_genre',
    db.Column('id_books',db.Integer(), db.ForeignKey('book.id',ondelete="CASCADE"), primary_key=True,nullable=False),
    db.Column('id_genres',db.Integer(), db.ForeignKey('genre.id',ondelete="CASCADE"), primary_key=True,nullable=False),
    db.Index('idx_book_genre__id_genres','id_genres')
)

book_publishing = db.Table(
    'book_publishing',
    db.Column('id_books',db.Integer(), db.ForeignKey('book.id',ondelete="CASCADE"), primary_key=True,nullable=False),
    db.Column('id_publishings',db.Integer(), db.ForeignKey('publishing.id',ondelete="CASCADE"), primary_key=True,nullable=False),
    db.Index('idx_book_publishing__id_publishings','id_publishings')
)

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer(),primary_key=True, unique=True)
    name = db.Column(db.String(500), nullable=False)
    id_book_author = db.relationship('Book', secondary=book_author, back_populates='id_book_author', uselist=False)

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer(),primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    id_book_genre = db.relationship('Book',secondary=book_genre, back_populates='id_book_genre', uselist=False)

class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer(),primary_key=True, unique=True)
    description = db.Column(db.String(255), nullable=False)

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer(),primary_key=True, unique=True)
    id_place = db.Column(db.ForeignKey('place.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    id_book_author = db.relationship('Author',secondary=book_author, back_populates='id_book_author', uselist=False)
    id_book_genre= db.relationship('Genre',secondary=book_genre, back_populates='id_book_genre', uselist=False)
    id_book_publishing= db.relationship('Publishing',secondary=book_publishing, back_populates='id_book_publishing', uselist=False)

db.Index('idx_book__id_place',Book.id_place)

class Publishing(db.Model):
    __tablename__ = 'publishing'
    id = db.Column(db.Integer(),primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    id_book_publishing = db.relationship('Book', secondary=book_publishing, back_populates='id_book_publishing', uselist=False)

with app.app_context():
    db.drop_all()
    db.session.commit()
    try:
        db.create_all()
    except Exception as ex:
        print(ex)
    db.session.commit()
    
    try:
        db.session.add_all( [Place(id=i,description=f"Полка 0: место {i}")for i in range(1,6)]+
                        [Place(id=i,description=f"Полка 1: место {i-5}")for i in range(6,11)]+
                        [Place(id=i,description=f"Полка 2: место {i-10}")for i in range(11,16)])
        db.session.add_all([
            Genre(id=1,name="Роман"),
            Genre(id=2,name="Комедия"),
            Genre(id=3,name="Трагедия"),
            Genre(id=5,name="Программирование")
        ])
        db.session.add_all([
            Author(id=1,name="Уильям Шекспир"),
            Author(id=2,name="Илья Ильф"),
            Author(id=3,name="Евгений Петров"),
            Author(id=4,name="Дуглас Адамс"),
            Author(id=5,name="Лев Толстой"),
            Author(id=6,name="Роберт Седжвик"),
            Author(id=7,name="Кевин Уэйн"),
            Author(id=8,name="Питер Сейбел"),
            Author(id=9,name="Анонимный Автор")
        ])
        db.session.add_all([
            Book(id=1, id_place=1, name="Ромео и Джульетта"),
            Book(id=2, id_place=2, name="Гамлет"),
            Book(id=3, id_place=3, name="Король Лир"),
            Book(id=4, id_place=4, name="Макбет"),
            Book(id=5, id_place=6, name="Двенадцать стульев"),
            Book(id=6, id_place=7, name="Автостопом по галактике"),
            Book(id=7, id_place=8, name="Война и Мир"),
            Book(id=8, id_place=11,name="Алгоритмы на Java"),
            Book(id=9, id_place=12,name="Кодеры за работой. Размышления о ремесле программиста"),
            Book(id=10,id_place=13,name="Война и Мир")
        ])
        db.session.add_all([
            Publishing(id=1,name="Феникс"),
            Publishing(id=2,name="Росмен"),
            Publishing(id=3,name="Триумф"),
            Publishing(id=4,name="Аст"),
            Publishing(id=5,name="Питер"),
        ])
        db.session.commit()
    except Exception as ex:
        print('------')
        print(ex)

    with db.session.connection() as conn:
            random.seed(1)
            conn.execute(
                insert(book_publishing),[{'id_books':i,'id_publishings':random.randint(1,5)} for i in range(1,11) ],
            )
            conn.commit()

            conn.execute(
                insert(book_genre),[
                    {'id_books':1, 'id_genres':3},
                    {'id_books':2, 'id_genres':3},
                    {'id_books':3, 'id_genres':3},
                    {'id_books':4, 'id_genres':3},
                    {'id_books':5, 'id_genres':2},
                    {'id_books':6, 'id_genres':2},
                    {'id_books':7, 'id_genres':1},
                    {'id_books':8, 'id_genres':5},
                    {'id_books':9, 'id_genres':5},
                    {'id_books':10,'id_genres':2}  ]
            )
            conn.commit()

            conn.execute(
                insert(book_author),[
                    {'id_books':1, 'id_authors':1},
                    {'id_books':2, 'id_authors':1},
                    {'id_books':3, 'id_authors':1},
                    {'id_books':4, 'id_authors':1},
                    {'id_books':5, 'id_authors':2},
                    {'id_books':5, 'id_authors':3},
                    {'id_books':6, 'id_authors':4},
                    {'id_books':7, 'id_authors':5},
                    {'id_books':8, 'id_authors':6},
                    {'id_books':8, 'id_authors':7},
                    {'id_books':9, 'id_authors':8},
                    {'id_books':10,'id_authors':9}]
            )
            conn.commit()

#Условие 5 выполняется по всем запросам
#1
def select_books_by_name(name:str):
    return db.session.execute(select(Book.name, Author.name, Place.description)
                      .join_from(book_author,Book)
                      .join_from(book_author,Author)
                      .join(Place)
                      .where(Book.name == name)).all()
#2
def select_books_by_author_id(author_id:int):
    return db.session.execute(select(Book.name, Author.name, Place.description)
                      .join_from(book_author,Book)
                      .join_from(book_author,Author)
                      .join(Place)
                      .where(Author.id == author_id)).all()

def select_books_by_author_name(name:str):
    return db.session.execute(select(Book.name, Author.name, Place.description)
                      .join_from(book_author,Book)
                      .join_from(book_author,Author)
                      .join(Place)
                      .where(Author.name == name)).all()
#3
def select_books_by_genre_id(genre_id:int):
    return db.session.execute(select(Book.name, Genre.name, Place.description)
                      .join_from(book_genre,Book)
                      .join_from(book_genre,Genre)
                      .join(Place).where(Genre.id == genre_id)).all()

#4
def select_books_by_publish_id(publish_id:int):
    return db.session.execute(select(Book.name, Publishing.name, Place.description)
                      .join_from(book_publishing,Book)
                      .join_from(book_publishing,Publishing)
                      .join(Place).where(Publishing.id == publish_id)).all()   

# Тестируем селекты    
with app.app_context():
    try:
        tests = [select_books_by_name("Война и Мир"),
                   select_books_by_author_id(2),
                   select_books_by_author_id(3),
                   select_books_by_author_name("Илья Ильф"),
                   select_books_by_author_name("Евгений Петров"),
                   select_books_by_publish_id(4),
                   select_books_by_genre_id(3)
                 ]
        for t in tests:
                for v in t:
                    print(v)
                print("---------------")
    except Exception as ex:
        print(ex)