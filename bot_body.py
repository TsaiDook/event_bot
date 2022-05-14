import telebot
from telebot import types  # для указание типов
import config
import pandas as pd

# не знаю, насколько круто считывать данные сразу, но кажется логичным
bot = telebot.TeleBot(config.token)
users_data = pd.read_csv('users.csv', index_col=0)
events_data = pd.read_csv('events.csv', index_col=0)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = (types.KeyboardButton(button_text) for button_text in config.start_buttons)
    markup.add(*buttons)
    bot.send_message(message.chat.id,
                     text=f"Привет, {message.from_user.username}! {config.intro_text}",
                     reply_markup=markup)


# для добавления юзера
def add_user(message):
    global users_data
    username = message.from_user.username
    append_df = pd.DataFrame([[None, None, username, None, None, None, True]],
                             columns=list(users_data))
    users_data = users_data.append(append_df)
    users_data.to_csv('users.csv')


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


# возможно, я тут написал глупость
@bot.callback_query_handler(func=lambda call: True)
def update_data(call):
    if call.message:
        info = call.data
        # frame не обновляется, но в остальном работает валидно
        if info in config.genders:
            print(f'Gender: {info}')
            users_data.loc[users_data.username == call.message.from_user.username].gender = info
        if info in config.common_hobbies:
            users_data.loc[users_data.username == call.message.from_user.username, 'hobbies'] = info
        if info in config.common_conv_topics:
            users_data.loc[users_data.username == call.message.from_user.username, 'conv_topics'] = info
        if info in config.ages:
            print(f'Age-group: {info}')
            users_data.loc[users_data.username == call.message.from_user.username, 'age'] = info
        else:
            users_data.loc[users_data.username == call.message.from_user.username, 'about_me'] = info

        users_data.to_csv('users.csv')


@bot.message_handler(content_types=['text'])
def communicate(message):
    if message.text == "Найти похожие события":
        bot.send_message(message.chat.id, text="Опиши мне его!")
    elif message.text == "Создать событие":
        bot.send_message(message.chat.id, text="Опиши событие, которое хочешь создать!")

    elif message.text == "Найти похожих юзеров":
        if message.from_user.username in users_data.username:
            bot.send_message(message.chat.id, "Ща как сделаю мэтч!")
        else:
            bot.send_message(message.chat.id, "Сначала необходимо ввести информацию о себе!")

    elif message.text == 'Рассказать о себе':
        if message.from_user.username in users_data.username:
            bot.send_message(message.chat.id, "Хотите изменить данные о себе?")
        else:
            bot.send_message(message.chat.id, "Давай начнем!")
            if message.from_user.username not in users_data.username.values:
                add_user(message)
            # начинаем получать данные о юзере
            # в фукнциях мы меняем users_data, а затем пересохраняем ее в .csv (все-таки Pandas не создан для такого)
            get_gender(message)
            print(users_data[users_data.username == message.from_user.username].gender.values)
            if users_data[users_data.username == message.from_user.username].gender.values:
                print('Идем дальше!')
                get_age(message)


    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = (types.KeyboardButton(button_text) for button_text in config.start_buttons)
        markup.add(*buttons)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)


bot.polling(none_stop=True)

# https://habr.com/ru/post/522720/ -- прикольный ввод
