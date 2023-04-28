from  database import *
from telebot import *
token = "6276712204:AAEtq4ljl9x14uPhWXm35zxXtFxTcf7G5NI"  # заполните значением вашего токена, полученного от BotFather
bot = telebot.TeleBot(token)
a=DatabaseConnector()
@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Добавить книгу')
    btn2 = types.KeyboardButton('Удалить книгу')
    btn3 = types.KeyboardButton('Все книги')
    btn4 = types.KeyboardButton('Найти книгу')
    btn5 = types.KeyboardButton('Взять себе')
    btn6 = types.KeyboardButton('Вернуть')
    btn7 = types.KeyboardButton('INFO по книге')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(message.from_user.id, "Добро пожаловать в чат бота-библиотеки! Выберите действие", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    ans.clear()
    if message.text == 'Добавить книгу': 
        answer =bot.send_message(message.chat.id, 'Введите название книги')
        bot.register_next_step_handler(answer, get_book)

    if message.text == 'Удалить книгу': 
       answer =bot.send_message(message.chat.id, 'Введите название книги') 
       bot.register_next_step_handler(answer, del_book)

    if message.text == 'Все книги': #LIZA
        ret = a.list_books()
        if ret ==[]:
            bot.send_message(message.from_user.id, "Нет книг")
        else:
            bot.send_message(message.from_user.id,  f'Список всех книг {ret}')
            

    if message.text == 'Найти книгу': #LIZA
        answer = bot.send_message(message.chat.id, 'Введите название книги') 
        bot.register_next_step_handler(answer, find_book)

    if message.text == 'Взять себе': #LIZA
        answer =bot.send_message(message.chat.id, 'Введите название книги') 
        bot.register_next_step_handler(answer, bor_book)

    if message.text == 'Вернуть': 
        answer =bot.send_message(message.chat.id, 'Введите название книги') 
        bot.register_next_step_handler(answer, retrieve_book)

    if message.text == 'INFO по книге': 
        answer = bot.send_message(message.chat.id, 'Введите название книги')
        bot.register_next_step_handler(answer, stats_book)  

ans =[]
# ADD
@bot.message_handler(content_types=['text'])
def get_book(message):
    ans.append(message.text)

    answer = bot.send_message(message.chat.id, "Введите автора:")
    bot.register_next_step_handler(answer, get_author)
    
@bot.message_handler(content_types=['text'])
def get_author(message):
    ans.append(message.text)
    answer = bot.send_message(message.chat.id, "Введите год создания:")
    bot.register_next_step_handler(answer, get_year, ans)
    
@bot.message_handler(content_types=['text'])
def get_year(message, ans):
    ans.append(message.text)
    req = a.add( ans[0], ans[1], int(ans[2]))
    ans.clear()
    if req==False:
        bot.send_message(message.chat.id, "Oшибка при добавлении книги")
    else:
        bot.send_message(message.chat.id, f"Книга добавлена {req}")

# DELETE
@bot.message_handler(content_types=['text'])
def del_book(message):
    answer = bot.send_message(message.chat.id, "Введите автора:")
    ans.append(message.text)
    bot.register_next_step_handler(answer, del_author)
    
@bot.message_handler(content_types=['text'])
def del_author(message):
    ans.append(message.text)
    answer = bot.send_message(message.chat.id, "Введите год создания:")
    bot.register_next_step_handler(answer, del_year, ans)
    
@bot.message_handler(content_types=['text'])
def del_year(message, ans):
    ans.append(message.text)
    r = a.get_book(ans[0], ans[1])
    if r==False:
        bot.send_message(message.chat.id, "Книга не найдена")
        ans=[]
    else : 
        answer = bot.send_message(message.chat.id, f"Найдена книга: {ans[0]} {ans[1]} {ans[2]} Удаляем?")
        bot.register_next_step_handler(answer, del_books, r)

@bot.message_handler(content_types=['text'])
def del_books(message,  r):
    change = message.text
    if change == "да":
        r = a.delete(r)
        ans=[]
        if r == True:
            answer = bot.send_message(message.chat.id, "Книга удалена")

        else:
            answer = bot.send_message(message.chat.id, "Невозможно удалить книгу")


#   RETRIEVE
@bot.message_handler(content_types=['text'])
def retrieve_book(message):
    ans.append(message.text)
    answer = bot.send_message(message.chat.id, "Введите автора:")
    bot.register_next_step_handler(answer, retrieve_author, ans)
    
@bot.message_handler(content_types=['text'])
def retrieve_author(message, ans):
    ans.append(message.text)
    answer = bot.send_message(message.chat.id, "Введите год создания:")
    bot.register_next_step_handler(answer, retrieve_year, ans)
    
@bot.message_handler(content_types=['text'])
def retrieve_year(message, ans):
    ans.append(message.text)
    rl = a.get_book(ans[0], ans[1])
    r = a.get_borrow(rl)
    if r==False:
        bot.send_message(message.chat.id, "Вы не брали такую книгу")
        ans=[]
    else : 
        answer = bot.send_message(message.chat.id, f"Найдена книга: {ans[0]} {ans[1]} {ans[2]} Возвращаем?")
        bot.register_next_step_handler(answer, retrieve_books, ans, r)

@bot.message_handler(content_types=['text'])
def retrieve_books(message,ans, r):
    change = message.text
    if change == "да":
        ra = a.retrieve(r)
        if ra == True:
            answer = bot.send_message(message.chat.id, f"Вы вернули книгу {ans[0]} {ans[1]} {ans[2]}")
        else:
            answer = bot.send_message(message.chat.id, "Невозможно вернуть книгу")

#STATS
@bot.message_handler(content_types=['text'])
def stats_book(message):
    ans.append(message.text)
    answer = bot.send_message(message.chat.id, "Введите автора:")
    bot.register_next_step_handler(answer, stats_author, ans)
    
@bot.message_handler(content_types=['text'])
def stats_author(message, ans):
    ans.append(message.text)
    answer = bot.send_message(message.chat.id, "Введите год создания:")
    bot.register_next_step_handler(answer, stats_year, ans)

@bot.message_handler(content_types=['text'])
def stats_year(message, ans):
    ans.append(message.text)
    r = a.get_book(ans[0], ans[1]) 
    ans=[]
    if r==False:
        bot.send_message(message.chat.id, "Нет такой книги")
    else : 
        bot.send_message(message.chat.id, f'Статистика доступна по ссылке [тык](http://127.0.0.1:8081/download/{r})',parse_mode='MarkdownV2')
    

#BORROW
@bot.message_handler(content_types=['text'])
def bor_book(message):
    answer = bot.send_message(message.chat.id, "Введите автора:")
    ans.append(message.text)
    bot.register_next_step_handler(answer, bor_author)
    
@bot.message_handler(content_types=['text'])
def bor_author(message):
    ans.append(message.text)
    answer = bot.send_message(message.chat.id, "Введите год создания:")
    bot.register_next_step_handler(answer, bor_year, ans)
    
@bot.message_handler(content_types=['text'])
def bor_year(message, ans):
    ans.append(message.text)
    ra = a.get_book(ans[0], ans[1]) 
    if ra==None:
        ans=[]
        bot.send_message(message.chat.id, "Книга не найдена")
    else : 
        answer = bot.send_message(message.chat.id, f"Найдена книга: {ans[0]} {ans[1]} {ans[2]} Берем?")
        bot.register_next_step_handler(answer, bor_books, ra)

@bot.message_handler(content_types=['text'])
def bor_books(message,  r):
    change = message.text
    if change == "да":
        r = a.borrow(r, message.chat.id)
        
        ans=[]
        if r == False:
            answer = bot.send_message(message.chat.id, "Сейчас невозможно взять книгу")
        else:
            answer = bot.send_message(message.chat.id, "Вы взяли книгу")



#GET BOOK
@bot.message_handler(content_types=['text'])
def find_book(message):
    ans.append(message.text)
    answer = bot.send_message(message.chat.id, "Введите автора:")
    bot.register_next_step_handler(answer, find_author, ans)
    
@bot.message_handler(content_types=['text'])
def find_author(message, ans):
    ans.append(message.text)
    answer = bot.send_message(message.chat.id, "Введите год создания:")
    bot.register_next_step_handler(answer, find_year, ans)
    
@bot.message_handler(content_types=['text'])
def find_year(message, ans):
    ans.append(message.text)
    req = a.get_book(ans[0], ans[1])
    ans=[]
    if req==None:
        bot.send_message(message.chat.id, "Книга не найдена")
    else:
        bot.send_message(message.chat.id, f"ID книги {req}")





bot.polling(none_stop=True)