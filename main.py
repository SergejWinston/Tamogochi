import database
import translate
import telebot
import time
from datetime import datetime, timedelta
from PIL import Image
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = '6730956910:AAEOuQEmi_MCAiGzCxkFTGGXg1LyjZysmjw'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def start_keyboard(language="ru"):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(eval(f"translate.{language}_k_show_menu"), callback_data="show_menu"))
    markup.add(InlineKeyboardButton(eval(f"translate.{language}_k_change_lang"), callback_data="change_language"))
    return markup

def status_keyboard(language="ru"):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(eval(f"translate.{language}_k_delete_menu"), callback_data="delete_menu"))
    markup.add(InlineKeyboardButton(eval(f"translate.{language}_k_change_lang"), callback_data="change_language"))
    return markup

def calculate_elapsed_time(unix_timestamp):
    
    minutes = int(unix_timestamp) // 60
    hours = minutes * 60 
    days = int(unix_timestamp) // 86400
    months = int(unix_timestamp) // 31536000
    years = int(unix_timestamp) // 315360000

    return {
        "minutes": minutes,
        "hours": hours,
        "days": days,
        "months": months,
        "years": years
    }

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call.data)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == "show_menu":
        x = str(eval(f"translate.{database.check('users', 'user_id', call.message.chat.id)[0][1]}_m_state")).format(
            database.check('pets', 'pet_id', call.message.chat.id)[0][1], # pet
            (datetime.utcfromtimestamp(int(database.check('pets', 'pet_id', call.message.chat.id)[0][8])) + timedelta(hours=3)).strftime('%H:%M %d.%m.%Y'), # age
            calculate_transformation(database.check('pets', 'pet_id', call.message.chat.id)[0][1], database.check('pets', 'pet_id', call.message.chat.id)[0][8]), # transformation
            database.check('pets', 'pet_id', call.message.chat.id)[0][2], # hp
            database.check('pets', 'pet_id', call.message.chat.id)[0][3], # happiness
            database.check('pets', 'pet_id', call.message.chat.id)[0][4], # education
            database.check('pets', 'pet_id', call.message.chat.id)[0][5], # action
            database.check('pets', 'pet_id', call.message.chat.id)[0][6], # bath
            database.check('pets', 'pet_id', call.message.chat.id)[0][7], # satiety
        )
        with open(f"images/{database.check('pets', 'pet_id', call.message.chat.id)[0][1]}.png", 'rb') as image:
            bot.send_photo(call.message.chat.id, image, caption=x, parse_mode="HTML", reply_markup=status_keyboard(database.check('users', 'user_id', call.message.chat.id)[0][1]))

    if call.data == "delete_menu":
        bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == "change_language":
        to_change = "en" if database.check('users', 'user_id', call.from_user.id)[0][1] == "ru" else "ru"
        database.set('users', 'user_id', call.from_user.id, 'lang', to_change)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        with open(f"images/{database.check('pets', 'pet_id', call.message.chat.id)[0][1]}.png", 'rb') as image:
            bot.send_photo(call.message.chat.id, image, caption=eval(f"translate.{database.check('users', 'user_id', call.message.chat.id)[0][1]}_start_again_command"), parse_mode="HTML", reply_markup=start_keyboard(database.check('users', 'user_id', call.message.chat.id)[0][1]))

@bot.message_handler(commands=['start'])
def start(message):
    new_user = False if len(database.check('users', 'user_id', message.from_user.id)) > 0 else True
    if new_user:
        database.remove_line('pets', 'pet_id', message.from_user.id)
        database.insert('pets', 'pet_id,type,hp,happiness,education,action,bath,satiety,time', f"{message.from_user.id},'egg',101,101,0,'NOTHING',0,101,{round(time.time())}")
        database.insert('users', 'user_id,lang', f"{message.from_user.id},'ru'")
        with open("images/egg.png", 'rb') as image:
            bot.send_photo(message.chat.id, image, caption=translate.ru_start_command, parse_mode="HTML", reply_markup=start_keyboard())
    else:
        with open(f"images/{database.check('pets', 'pet_id', message.from_user.id)[0][1]}.png", 'rb') as image:
            bot.send_photo(message.chat.id, image, caption=eval(f"translate.{database.check('users', 'user_id', message.from_user.id)[0][1]}_start_again_command"), parse_mode="HTML", reply_markup=start_keyboard(database.check('users', 'user_id', message.from_user.id)[0][1]))

@bot.message_handler(commands=['status'])
def status(message):
    x = str(eval(f"translate.{database.check('users', 'user_id', message.from_user.id)[0][1]}_m_state")).format(
        database.check('pets', 'pet_id', message.from_user.id)[0][1], # pet
        (datetime.utcfromtimestamp(int(database.check('pets', 'pet_id', message.from_user.id)[0][8])) + timedelta(hours=3)).strftime('%H:%M %d.%m.%Y'), # age
        calculate_transformation(database.check('pets', 'pet_id', message.from_user.id)[0][1], database.check('pets', 'pet_id', message.from_user.id)[0][8]), # transformation
        database.check('pets', 'pet_id', message.from_user.id)[0][2], # hp
        database.check('pets', 'pet_id', message.from_user.id)[0][3], # happiness
        database.check('pets', 'pet_id', message.from_user.id)[0][4], # education
        database.check('pets', 'pet_id', message.from_user.id)[0][5], # action
        database.check('pets', 'pet_id', message.from_user.id)[0][6], # bath
        database.check('pets', 'pet_id', message.from_user.id)[0][7], # satiety
    )
    with open(f"images/{database.check('pets', 'pet_id', message.from_user.id)[0][1]}.png", 'rb') as image:
        bot.send_photo(message.chat.id, image, caption=x, parse_mode="HTML", reply_markup=status_keyboard(database.check('users', 'user_id', message.from_user.id)[0][1]))


def calculate_transformation(*x):
    p_type = x[0]
    p_old = x[1]
    p_wait = datetime.utcfromtimestamp(int(p_old)) + timedelta(days=3)
    return (p_wait + timedelta(hours=3)).strftime('%H:%M %d.%m.%Y')

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    print()


bot.infinity_polling()