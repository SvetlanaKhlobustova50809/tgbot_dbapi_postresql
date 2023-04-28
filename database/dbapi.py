from sqlalchemy.orm import sessionmaker
import datetime
import pandas

from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship
from database.models import Book, Borrow

user = "augustru"
engine = create_engine(f"postgresql+psycopg2://{user}@localhost:5433/")

connection = engine.connect()
Session = sessionmaker(bind=engine)


class DatabaseConnector:
    def __init__(self):
        self.session = Session()
        
    @classmethod
    def get_borrowsExcel(cls, book_id):
        try:
            int(book_id)
        except:
            pass
        else:
            frame = pandas.read_sql(f"SELECT borrow_id, book_id, date_start, date_end FROM public.\"Borrows\" WHERE book_id = {book_id}", connection)
            frame.to_excel(f"statisticsBook{book_id}.xlsx")
        return book_id

    def add(self, title, author, published):
        # Создание новой книги и добавление ее в базу данных
        book = Book(title=title, author=author, published=published, date_added=datetime.datetime.now(),
                    date_deleted=datetime.datetime.max)
        self.session.add(book)
        try:
            self.session.commit()
            return book.book_id
        except:
            self.session.rollback()
            return False

    def delete(self, book_id):
        # Удаление книги из базы данных
        book = self.session.query(Book).get(book_id)
        if not book:
            return False
        # if book.borrow:
        #     return False
        book.date_deleted = datetime.datetime.now()
        self.session.delete(book)
        try:
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def list_books(self):
        # Получение списка всех книг, которые есть в библиотеке
        books = self.session.query(Book).filter(Book.date_deleted == datetime.datetime.max).all()
        return [(book.book_id, book.title, book.author, book.published) for book in books]

    def get_book(self, title, author):
        # Получение книги по ее названию и автору
        book = self.session.query(Book).filter(Book.title.ilike(f'%{title}%')).filter(
            Book.author.ilike(f'%{author}%')).filter(Book.date_deleted == datetime.datetime.max).first()
        return book.book_id if book else None

    def borrow(self, book_id, user_id):
        # Взять книгу из библиотеки
        book = self.session.query(Borrow).filter(Borrow.book_id==book_id).first()
        if book == None:
            borrow = Borrow(book_id=book_id, date_start=datetime.datetime.now(), date_end=datetime.datetime.min,
                        user_id=user_id)
            self.session.add(borrow)
        elif book and book.date_end == datetime.datetime.min:
            return False
        
        try: 
            self.session.commit()
            
            return borrow.borrow_id
        except:
            self.session.rollback()
            return False

    def get_borrow(self, book_id):
        # Получение информации о взятой книге
        borrow = self.session.query(Borrow).filter(Borrow.book_id==book_id).first()
        
        return borrow

    def retrieve(self, borrow):
        if not borrow:
            return False
        if borrow.date_end != datetime.datetime.min:  # проверяем, была ли книга уже возвращена
            return False
        borrow_id=borrow.borrow_id
        book = self.session.query(Borrow).get(borrow_id)
        print(book)
        if not book:
            return False
        user_borrows = self.session.query(Borrow).filter_by(user_id=borrow.user_id,
                                                            date_end=datetime.datetime.min).all()

        borrow.date_end = datetime.datetime.now()
        book.borrow = None
        self.session.add(borrow)
        try:
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False




