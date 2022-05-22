import telebot
from telebot import types  # для указание типов
import config
from users_tb_itter import insert_user, check_existence, update_user, get_user_feature_val, is_user_info_filled

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = (types.KeyboardButton(button_text) for button_text in config.start_buttons)
    markup.add(*buttons)
    bot.send_message(message.chat.id,
                     text=f"Привет, {message.from_user.username}! {config.intro_text}",
                     reply_markup=markup)
    if not check_existence(message.from_user.username):
        insert_user(username=message.from_user.username)


def get_gender(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(text=gender,
                                          callback_data=gender)
               for gender in config.genders]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id,
                     'Выбери свой гендер:\n P.S. большинство наших юзеров хотели бы знать это перед встречей)',
                     reply_markup=keyboard)


def get_age(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=age,
                                          callback_data=age)
               for age in config.ages]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id,
                     'Отлично! Теперь укажи свой возраст:',
                     reply_markup=keyboard)


# CODE DOUBLING!!
@bot.callback_query_handler(func=lambda call: True)
def update_data(call):
    if call.message:
        info = call.data
        if info in config.genders:
            update_user(call.message.chat.username, "gender", info)
            bot.send_message(call.message.chat.id, text=f"""Гендер изменен на "{info}" """)
            get_age(call.message)
        elif info in config.ages:
            update_user(call.message.chat.username, "age", info)
            bot.send_message(call.message.chat.id, text=f"""Возраст изменен на "{info}" """)
        else:
            update_user(call.message.chat.username, "self_description", info)
            bot.send_message(call.message.chat.id, text=f"""Описание изменено на на "{info}" """)


@bot.message_handler(content_types=['text'])
def communicate(message):
    if message.text == "Найти похожие события":
        bot.send_message(message.chat.id, text="Опиши мне его!")
    elif message.text == "Создать событие":
        bot.send_message(message.chat.id, text="Опиши событие, которое хочешь создать!")

    elif message.text == "Найти похожих юзеров":
        if check_existence(message.from_user.username):
            bot.send_message(message.chat.id, "Ща как сделаю мэтч!")
        else:
            bot.send_message(message.chat.id, "Сначала необходимо ввести информацию о себе!")

    elif message.text == 'Рассказать о себе':
        if is_user_info_filled(message.from_user.username):
            bot.send_message(message.chat.id, "Хотите изменить данные о себе?")
        else:
            bot.send_message(message.chat.id, "Давай начнем!")
            # начинаем получать данные о юзере
            get_gender(message)
        if message.text in config.genders:
            print('Идем дальше!')
            get_age(message)


    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = (types.KeyboardButton(button_text) for button_text in config.start_buttons)
        markup.add(*buttons)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)


bot.polling(none_stop=True)

# https://habr.com/ru/post/522720/ -- прикольный ввод
