from sqlalchemy.orm import sessionmaker
import datetime


from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship

user = "augustru"
engine = create_engine(f"postgresql+psycopg2://{user}@localhost:5433/")

connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session() 

Base = declarative_base()

class Book(Base):
    __tablename__ = 'Books'
    
    book_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    published = Column(Integer, nullable=False)
    date_added = Column(DateTime, nullable=True)
    date_deleted = Column(DateTime, nullable=True)
    
#book = Book(title="title", author="author", published=123, date_added=datetime.datetime.now(),date_deleted=datetime.datetime.max)
class Borrow(Base):
    __tablename__ = 'Borrows'
    
    borrow_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("Books.book_id"))
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
  

Base.metadata.create_all(engine)

session.commit()


'''
INSERT INTO "Borrows" (borrow_id,book_id,date_start,date_end,user_id)
VALUES
  (1,5,'3-29-2023 9:37:18','8-14-2023 3:11:27','297'),
  (2,8,'3-7-2024 9:44:14','2-16-2023 12:54:25','730'),
  (3,1,'5-21-2023 8:57:2','6-27-2023 5:57:2','991'),
  (4,5,'7-27-2023 6:48:13','2-11-2023 8:4:24','638'),
  (5,8,'4-18-2023 1:42:46','8-23-2023 6:57:41','294'),
  (6,2,'1-24-2023 1:10:28','3-30-2024 9:58:43','448'),
  (7,9,'3-29-2024 6:21:51','6-12-2022 2:0:36','300'),
  (8,8,'10-12-2023 7:31:30','8-20-2023 11:17:8','343'),
  (9,7,'9-12-2022 12:52:17','11-17-2023 10:8:59','853'),
  (10,9,'3-10-2023 9:31:25','8-8-2023 3:38:34','502');


  INSERT INTO "Books" (book_id,title,author,published,date_added,date_deleted)
VALUES
  (1,'Cholet','Brittany Burks','2017','1-25-2019','7-28-2023'),
  (2,'Trier','Forrest Patel','2016','1-23-2021','6-21-2023'),
  (3,'Palopo','Holmes Doyle','2015','4-19-2018','1-20-2024'),
  (4,'Tokoroa','Carol Wilson','2016','12-5-2018','12-26-2022'),
  (5,'Bogotá','Giselle Simmons','2016','3-12-2019','5-15-2023'),
  (6,'Mmabatho','Simone Ashley','2017','8-19-2019','11-9-2022'),
  (7,'Crehen','Illiana Callahan','2018','12-7-2019','10-18-2023'),
  (8,'Scandriglia','Edward Hudson','2016','3-18-2020','6-3-2023'),
  (9,'Urdaneta','Galena Warren','2015','1-7-2020','10-16-2023'),
  (10,'Kallang','Jolene Cherry','2017','12-9-2020','12-13-2022');
'''




