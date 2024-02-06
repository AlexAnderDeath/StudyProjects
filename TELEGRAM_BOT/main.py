import  telebot as tbot
from dotenv import load_dotenv
import  os
from os.path import join,dirname
from telebot import types
import random
import requests
import sqlite3
import datetime

def get_from_env(key):
    dotenv_path = join(dirname(__file__),'.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)
BOT_TOKEN = get_from_env('API_TOKEN')

bot = tbot.TeleBot(BOT_TOKEN)


@bot.message_handler(func=lambda message: message.text.lower() == "привет")
def handle_hello(message):
    bot.send_message(message.chat.id, "Привет! Как я могу тебя называть")
    bot.register_next_step_handler(message, handle_name)

@bot.message_handler(func=lambda message: message.text.lower() == "число")
def random_num(message):
    bot.reply_to(message,f'Число: {random.randint(0,100)}')


def handle_name(message):
    bot.send_message(message.chat.id, f"Приятно познакомиться, {message.text}!")

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS bot_users(id int auto_increment primary key,name varchar(50),date time)")
    connect.commit()
    cursor.close()
    connect.close()

    user_id = message.chat.id
    timestamp = str(datetime.datetime.now().strftime("%H:%M:%S"))
    user_name = message.from_user.username

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO bot_users (name,date) VALUES (?, ?)", (user_name, timestamp))
    connect.commit()
    cursor.close()
    connect.close()

    """ 
    cursor.execute("INSERT INTO bot_users VALUES(?);", user_id)
    connect.commit()"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
    start_button =types.KeyboardButton('/start')
    help_button = types.KeyboardButton('/help')
    random_num_butt = types.KeyboardButton('Число')
    send_voice_butt = types.KeyboardButton('тест гс')
    send_sticker_butt = types.KeyboardButton('Стикер')
    catalog_butt = types.KeyboardButton('Каталог1')

    markup.add(start_button,help_button,send_sticker_butt,send_voice_butt,random_num_butt,catalog_butt)

    bot.send_message(message.chat.id,'Привет я ТГ чат-бот, созданный Alex_AnderDeath. Введите /help, чтобы узнать, чем я могу быть полезен',reply_markup=markup)



@bot.message_handler(func=lambda message: message.text.lower() == "стикер")
def send_sticker(message):
    sicker_pack = ['CAACAgQAAxkBAAJCpGUOu79SMLzJ2YNBNoWT19RxX8exAAKtDQACM_kBUxS8b-wxB34XMAQ',
                   'CAACAgQAAxkBAAJDD2UQEl_CUYZLC76KEwEb89UT8HmXAAJJDwAChHT4Ujp_CH3VGhS5MAQ',
                   'CAACAgQAAxkBAAJDEWUQEnrMTQmfrE1TO6M44GLXXdDFAAJuEAACxC8BU2IIiWoW8ElWMAQ',
                   'CAACAgIAAxkBAAJDGmUQFffACg9NSFLuL4BSMAwsJNt_AALPPAACJNhQSfSRtbDuddrXMAQ']
    bot.send_sticker(message.chat.id,random.choice(sicker_pack))


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, """\
    Вы открыли справку. Я могу выполнить следующие команды: /start, /help, сгенерировать случайное число от 0 до 100 также прислать стикер или голосовое сообщение\
""")


def send_voice_message(file_path,chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVoice"
    files = {'voice': open(file_path, 'rb')}
    data = {'chat_id': chat_id}

    response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        print("Voice message sent successfully!")
    else:
        print("Failed to send voice message")


@bot.message_handler(func = lambda message: message.text.lower() == "тест гс")
def send_test_voice(message):
    chat_id = message.chat.id
    send_voice_message("voise_1_ipsum_lorem.wav",chat_id)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(content_types=['text'])
def echo_message(message):
    if message.text == 'Каталог1':
        markup =  types.ReplyKeyboardMarkup(resize_keyboard=True)
        catalog_sub1 = types.KeyboardButton('Подраздел1')
        catalog_sub2 = types.KeyboardButton('Подраздел2')
        back_to_menu = types.KeyboardButton('Назад')
        markup.add(catalog_sub1,catalog_sub2,back_to_menu)
        bot.send_message(message.chat.id,'Вы зашли в Каталог1', reply_markup=markup)

    elif message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_button = types.KeyboardButton('/start')
        help_button = types.KeyboardButton('/help')
        random_num_butt = types.KeyboardButton('Число')
        send_voice_butt = types.KeyboardButton('тест гс')
        send_sticker_butt = types.KeyboardButton('Стикер')
        catalog_butt = types.KeyboardButton('Каталог1')


        markup.add(start_button, help_button, send_sticker_butt, send_voice_butt,random_num_butt, catalog_butt)

        bot.send_message(message.chat.id,
                         'Привет я ТГ чат-бот, созданный Alex_AnderDeath. Введите /help, чтобы узнать, чем я могу быть полезен',
                         reply_markup=markup)

    else:
         bot.reply_to(message, message.text)

bot.polling(none_stop=True)