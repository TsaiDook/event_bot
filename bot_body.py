import telebot
from telebot import types  # для указание типов
import config
from users_tb_iter import insert_user, check_existence, update_user_tb, update_user_hobbies_tb, update_user_topics_tb, \
    is_not_empty_match_info

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


def get_hobbies(message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(text=hobby,
                                          callback_data=hobby)
               for hobby in config.common_hobbies]

    keyboard.add(*buttons)
    bot.send_message(message.chat.id,
                     'Великолепно! Расскажи нам о своих интересах. Можешь выбрать от 1 до 8 вариантов:',
                     reply_markup=keyboard)


def get_conv_topics(message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(text=topic,
                                          callback_data=topic)
               for topic in config.common_conv_topics]

    keyboard.add(*buttons)
    bot.send_message(message.chat.id,
                     'И последнее: о чем предпочитаешь говорить? (укажи хотя бы 1 пункт 😄)',
                     reply_markup=keyboard)


# CODE DOUBLING!!
@bot.callback_query_handler(func=lambda call: True)
def update_data(call):
    if call.message:
        info = call.data
        if info in config.genders:
            update_user_tb(call.message.chat.username, "gender", info)
            bot.send_message(call.message.chat.id, text=f'Гендер изменен на "{info}"')
            get_age(call.message)
        elif info in config.ages:
            update_user_tb(call.message.chat.username, "age", info)
            bot.send_message(call.message.chat.id, text=f'Возраст изменен на "{info}"')
            get_hobbies(call.message)
        elif info in config.common_hobbies and info != 'DONE':
            update_user_hobbies_tb(call.message.chat.username, info)
            bot.send_message(call.message.chat.id, text=f'Добавил хобби "{info}"')
        elif info == 'DONE':
            bot.send_message(call.message.chat.id, text='Хобби добавлены! Идем к разговорам!')
            get_conv_topics(call.message)
        elif info in config.common_conv_topics and info != 'FINISH':
            update_user_topics_tb(call.message.chat.username, info)
            bot.send_message(call.message.chat.id, text=f'Добавил тему "{info}"')
        elif info == 'FINISH':
            bot.send_message(call.message.chat.id,
                             text='Отлично! Чтобы люди лучше понимали, что ты за фрукт, немного опиши себя в свободной форме:')


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
        if is_not_empty_match_info(message.from_user.username):
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

    else:
        update_user_tb(message.chat.username, "self_description", message.text)
        bot.send_message(message.chat.id, text=f'Отлично! Мы закончили.\nТвое описание:\n"{message.text}"')


bot.polling(none_stop=True)
