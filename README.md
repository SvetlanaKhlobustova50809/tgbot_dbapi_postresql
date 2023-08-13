# A bot for interacting with the library database, where you can add, delete, take, return or find a book

The parts of project:
1. DB access module: description of data models and API interaction with these models
2. The module of interaction with Telegram
3. The database itself.

To launch the bot, you need: 
1) enter your data about an empty database in postgresql - name, port, password if available 
2) run the entire project using `__init__.py ` or run `models.py ` 
3) launch `telegram.py`

You should also install the following packages:
```
pip install pytelegrambotapi
pip install SQLAlchemy
pip install psycopg2
```
