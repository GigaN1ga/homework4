import sqlite3
from pathlib import Path
from aiogram import Dispatcher
DB_PATH = Path(__file__).parent.parent
DB_NAME = 'db.sqlite'
db = sqlite3.connect(DB_PATH / DB_NAME)
cursor = db.cursor()


def init_db():
    global db, cursor

def create_tables():

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Genres (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )""")


    cursor.execute("""CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        image_url TEXT,
        genre_id INTEGER,
        FOREIGN KEY(genre_id) REFERENCES Genres(id)
    )""")
    db.commit()

def insert_data():

    cursor.execute("""INSERT INTO Genres (name) VALUES
        ('Фантастика'),
        ('Романы'),
        ('Детективы')""")


    cursor.execute("""INSERT INTO Books (name, price, image_url, genre_id) VALUES
        ('Война и мир', 1500.00, 'images/cover.jpg', 2),
        ('Мастер и Маргарита', 1200.00, 'images/cover.jpg', 4),
        ('Дозоры', 1700.00, 'images/cover.jpg', 1),
        ('Братья Карамазовы', 1600.00, 'images/cover.jpg', 2),
        ('Азазель', 1000.00, 'images/cover.jpg', 3)
    """)
    db.commit()


def drop_tables():
    cursor.execute("""DROP TABLE IF EXISTS Books""")
    cursor.execute("""DROP TABLE IF EXISTS Genres""")
    db.commit()


def fetch_books():
    # -- Fetch all books
    cursor.execute("""SELECT * FROM Books""")
    books = cursor.fetchall()
    # for b in books:
    #     print(b[1])
    return books

async def show_mag(message):
    products = cursor.execute('SELECT * FROM Books').fetchall()
    for i in products:
        await message.answer(f'{i}')


if __name__ == "__main__":
    init_db()
    drop_tables()
    create_tables()
    insert_data()
    fetch_books()

def register_handlers_db(dp:Dispatcher):
    dp.register_message_handler(show_mag, commands=['magaz'])
