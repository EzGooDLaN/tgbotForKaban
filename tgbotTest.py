import sqlite3
import telebot
from telebot import types

# Создание бота
API_TOKEN = "8189682279:AAH3AfnCEjj4v9m7ruTMxpGtX1hTBoXTrJ8"
bot = telebot.TeleBot(API_TOKEN)

# Пользовательские данные
user_data = {}


def db_connection():
    conn = sqlite3.connect('requests.db')
    return conn


def create_table():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS requests
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       info TEXT)''')
    conn.commit()
    conn.close()


@bot.message_handler(commands=['start', 'main', 'hello'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Проблема')
    button2 = types.KeyboardButton('Справка')
    markup.row(button1)
    markup.row(button2)

    if message.text == '/start':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n'
                                          f'В этом телеграмм-боте мы можем помочь тебе с поломками техники!\n'
                                          f'Контакт моего разработчика: https://t.me/LittleHopik', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Перекинул тебя в главное меню! Выбирай!', reply_markup=markup)


@bot.message_handler()
def info(message):
    if message.text == 'Проблема':
        catalogChapter(message)
    elif message.text == 'Справка':
        infoChapter(message)
    elif message.text == 'Телеграмм разработчика':
        bot.send_message(message.chat.id, 'https://t.me/LittleHopik')
    elif message.text == 'Почта разработчика':
        bot.send_message(message.chat.id, 'n.tkachenko_05@mail.ru')
    elif message.text == 'Назад в меню':
        welcome(message)
    elif message.text in ['Бытовая техника', 'Строительная техника', 'Электроника']:
        person_info(message)
    elif message.text == 'Готово':
        if message.chat.id in user_data:
            save_to_db(message.chat.id)
            bot.send_message(message.chat.id, 'Ваша заявка успешно сохранена!\n'
                                              'Ожидайте ответа.')
        else:
            bot.send_message(message.chat.id, 'Вы не ввели данные!')
    else:
        if message.chat.id not in user_data:
            user_data[message.chat.id] = []
        user_data[message.chat.id].append(message.text)
        bot.send_message(message.chat.id, 'Данные сохранены. Нажмите "Готово", когда закончите ввод.')


def catalogChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Бытовая техника')
    button2 = types.KeyboardButton('Строительная техника')
    button3 = types.KeyboardButton('Электроника')
    button5 = types.KeyboardButton('Назад в меню')
    markup.row(button1, button2)
    markup.row(button3)
    markup.row(button5)
    bot.send_message(message.chat.id, 'С чем мы можем помочь:', reply_markup=markup)


def infoChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Телеграмм разработчика')
    button2 = types.KeyboardButton('Назад в меню')
    button3 = types.KeyboardButton('Почта разработчика')
    markup.row(button1, button3)
    markup.row(button2)
    bot.send_message(message.chat.id, 'Раздел справки.\n'
                                      'Информация для связи с разработчиком:', reply_markup=markup)


def person_info(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Назад в меню')
    button2 = types.KeyboardButton('Готово')
    markup.row(button2)
    markup.row(button1)
    bot.send_message(message.chat.id, '1. Пожалуйста, введите ваше имя:\n'
                                      '2. Введите вашу контактную информацию:\n'
                                      '3. Опишите вашу проблему:\n'
                                      '4. Введите предпочтительное время для связи:', reply_markup=markup)


def save_to_db(chat_id):
    conn = db_connection()
    cursor = conn.cursor()
    info_text = "\n".join(user_data[chat_id])
    cursor.execute('INSERT INTO requests (info) VALUES (?)', (info_text,))
    conn.commit()
    conn.close()
    del user_data[chat_id]


if __name__ == '__main__':
    create_table()
    bot.polling(none_stop=True)
