#https://editor.ponyorm.com/user/nikolasov/home_unit_7_v12/designer
#БД «Библиотека»
#Описание предметной области. БД создается для домашнего
#обслуживания библиотеки. Библиотека содержит книги разных авторов,
#изданий, тематик. БД предназначена для поиска выбранной книги на полке.
#Готовые запросы:
#1. Выдавать список книг по названию;
#2. Выдавать список трудов данного автора (учитывать труды, выполненные
#в соавторстве);
#3. Выдавать список книг по данной тематике;
#4. Выдавать список книг данного издательства;
#5. Выдавать местонахождение данной книги.
import psycopg2
import random
schema_string = """
CREATE TABLE "author" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(500) NOT NULL
);

CREATE TABLE "genre" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(255) NOT NULL
);

CREATE TABLE "place" (
  "id" SERIAL PRIMARY KEY,
  "description" VARCHAR(255) NOT NULL
);

CREATE TABLE "book" (
  "id" SERIAL PRIMARY KEY,
  "id_place" INTEGER NOT NULL,
  "name" VARCHAR(255) NOT NULL
);

CREATE INDEX "idx_book__id_place" ON "book" ("id_place");

ALTER TABLE "book" ADD CONSTRAINT "fk_book__id_place" FOREIGN KEY ("id_place") REFERENCES "place" ("id");

CREATE TABLE "book_author" (
  "id_books" INTEGER NOT NULL,
  "id_authors" INTEGER NOT NULL,
  PRIMARY KEY ("id_books", "id_authors")
);

CREATE INDEX "idx_book_author__id_authors" ON "book_author" ("id_authors");

ALTER TABLE "book_author" ADD CONSTRAINT "fk_book_author__id_authors" FOREIGN KEY ("id_authors") REFERENCES "author" ("id") ON DELETE CASCADE;

ALTER TABLE "book_author" ADD CONSTRAINT "fk_book_author__id_books" FOREIGN KEY ("id_books") REFERENCES "book" ("id") ON DELETE CASCADE;

CREATE TABLE "book_genre" (
  "id_books" INTEGER NOT NULL,
  "id_genres" INTEGER NOT NULL,
  PRIMARY KEY ("id_books", "id_genres")
);

CREATE INDEX "idx_book_genre__id_genres" ON "book_genre" ("id_genres");

ALTER TABLE "book_genre" ADD CONSTRAINT "fk_book_genre__id_books" FOREIGN KEY ("id_books") REFERENCES "book" ("id") ON DELETE CASCADE;

ALTER TABLE "book_genre" ADD CONSTRAINT "fk_book_genre__id_genres" FOREIGN KEY ("id_genres") REFERENCES "genre" ("id") ON DELETE CASCADE;

CREATE TABLE "publishing" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(255) NOT NULL
);

CREATE TABLE "book_publishing" (
  "id_books" INTEGER NOT NULL,
  "id_publishings" INTEGER NOT NULL,
  PRIMARY KEY ("id_books", "id_publishings")
);

CREATE INDEX "idx_book_publishing__id_publishings" ON "book_publishing" ("id_publishings");

ALTER TABLE "book_publishing" ADD CONSTRAINT "fk_book_publishing__id_books" FOREIGN KEY ("id_books") REFERENCES "book" ("id") ON DELETE CASCADE;

ALTER TABLE "book_publishing" ADD CONSTRAINT "fk_book_publishing__id_publishings" FOREIGN KEY ("id_publishings") REFERENCES "publishing" ("id") ON DELETE CASCADE
"""

def make_insert_cmd(table_name, field, n_values):
    return "INSERT INTO \""+table_name+"\" "+field+" VALUES "+",".join(["%s" for i in range(n_values)])


f_1="(\"id\", \"name\")"
#Тестовые данные
# Место на полке
place_data = ["(\"id\",\"description\")",
              [(i,f"Полка 0: место {i}")for i in range(1,6)]+
              [(i,f"Полка 1: место {i-5}")for i in range(6,11)]+
              [(i,f"Полка 2: место {i-10}")for i in range(11,16)]
              ]
# Список жанров
genre_data =[f_1,[
            (1,"Роман"),
            (2,"Комедия"),
            (3,"Трагедия"),
            (5,"Программирование"),
        ]] 

#Список авторов
authro_data = [f_1,[
            (1,"Уильям Шекспир"),
            (2,"Илья Ильф"),
            (3,"Евгений Петров"),
            (4,"Дуглас Адамс"),
            (5,"Лев Толстой"),
            (6,"Роберт Седжвик"),
            (7,"Кевин Уэйн"),
            (8,"Питер Сейбел"),
            (9,"Анонимный Автор")
        ]]

#Список книг
book_data = ["(\"id\",\"id_place\",\"name\")",[
    (1,1,"Ромео и Джульетта"),
    (2,2,"Гамлет"),
    (3,3,"Король Лир"),
    (4,4,"Макбет"),
    (5,6,"Двенадцать стульев"),
    (6,7,"Автостопом по галактике"),
    (7,8,"Война и Мир"),
    (8,11,"Алгоритмы на Java"),
    (9,12,"Кодеры за работой. Размышления о ремесле программиста"),
    (10,13,"Война и Мир")

]]

#Список издательств
publishing_data=[f_1,[
    (1,"Феникс"),
    (2,"Росмен"),
    (3,"Триумф"),
    (4,"Аст"),
    (5,"Питер"),
]]

#Перекрестные таблицы
random.seed(1)
book_pablishing_data=["(\"id_books\",\"id_publishings\")",
                      [ (i,random.randint(1,5)) for i in range(1,11) ]]

book_genre_data = ["(\"id_books\",\"id_genres\")",[
                    (1,3),
                    (2,3),
                    (3,3),
                    (4,3),
                    (5,2),
                    (6,2),
                    (7,1),
                    (8,5),
                    (9,5),
                    (10,2)               
                ]]

book_author_data=["(\"id_books\",\"id_authors\")",[
    (1,1),
    (2,1),
    (3,1),
    (4,1),
    (5,2),
    (5,3),
    (6,4),
    (7,5),
    (8,6),
    (8,7),
    (9,8),
    (10,9)
]]

#Общий контейнер 
vals={"place":place_data,
      "genre":genre_data,
      "author":authro_data,
      "book":book_data,
      "publishing":publishing_data,
      "book_publishing":book_pablishing_data,
      "book_author":book_author_data,
      "book_genre":book_genre_data
      }

#Условие 5 выполняется по всем запросам
#1
def select_books_by_name(name:str):
    return f"""SELECT b.name, a.name, p.description
    FROM book b 
    JOIN book_author ba ON b.name = '{name}' AND b.id =ba.id_books
    JOIN author a ON ba.id_authors = a.id
    JOIN place p ON p.id = b.id_place"""
#2
def select_books_by_author_id(author_id:int):
    return f"""SELECT b.name, a.name, p.description
    FROM book b 
    JOIN book_author ba ON ba.id_authors = {author_id} AND ba.id_books = b.id
    JOIN author a ON a.id = {author_id}
    JOIN place p ON p.id = b.id_place"""

def select_books_by_author_name(name:str):
    return f"""SELECT b.name, a.name, p.description
    FROM book b 
    JOIN book_author ba ON ba.id_books = b.id
    JOIN author a ON a.id = ba.id_authors AND a.name = '{name}'
    JOIN place p ON p.id = b.id_place"""
#3
def select_books_by_genre_id(genre_id:int):
    return f"""SELECT b.name, g.name, p.description
        FROM book b 
        JOIN book_genre bg ON bg.id_genres = {genre_id} AND bg.id_books = b.id
        JOIN genre g ON g.id = {genre_id}
        JOIN place p ON p.id = b.id_place"""

#4
def select_books_by_publish_id(publish_id:int):
    return f"""SELECT b.name, pu.name, p.description
        FROM book b 
        JOIN book_publishing pb ON pb.id_publishings = {publish_id} AND pb.id_books = b.id
        JOIN publishing pu ON pu.id = {publish_id}
        JOIN place p ON p.id = b.id_place"""

test_selects =[select_books_by_name("Война и Мир"),
               select_books_by_author_id(2),
               select_books_by_author_id(3),
               select_books_by_author_name("Илья Ильф"),
               select_books_by_author_name("Евгений Петров"),
               select_books_by_publish_id(4),
               select_books_by_genre_id(3)]

#Подключение к базе инициализация таблиц заполнение и проверка запросов
with psycopg2.connect("dbname=library_book user=psql_user password=12345678") as conn:
    
    # --- Создаем схему базы
    with conn.cursor() as cur:
        try:
            cur.execute(schema_string)
        except Exception as ex:
            print(ex)
            conn.commit()
            
        conn.commit() 

    # Заполняем схему 
    with conn.cursor() as cur:
      for key,val in vals.items():
          try:
              cur.execute(make_insert_cmd(key,val[0],len(val[1])),val[1])
          except Exception as ex : print(ex)
          conn.commit() 

    
    # Делаем  тестовые выборки
    with conn.cursor() as cur:
      for cmd in test_selects:
        try:
            cur.execute(cmd)
        except Exception as ex:
            print(ex)
        finally:
            for row in cur.fetchall():
                print(row)
        print("------------------")