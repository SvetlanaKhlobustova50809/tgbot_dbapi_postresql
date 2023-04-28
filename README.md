# A bot for interacting with the library database, where you can add, delete, take, return or find a book

The parts of project:
1. The server that will post links to files with statistics
2. DB access module: description of data models and API interaction with these models
3. The module of interaction with Telegram
4. The database itself.

To launch the bot, you need: 
1) enter your data about an empty database in postgresql - name, port, password if available 
2) run the entire project using `__init__.py ` or run `models.py ` 
3) launch `telegram.py`
