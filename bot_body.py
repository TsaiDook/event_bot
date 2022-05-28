import telebot
from telebot import types
import config
from users_tb_iter import insert_user, check_existence, update_user_tb, update_user_hobbies_tb, update_user_topics_tb, \
    get_user_tb_column_val

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id, username = message.chat.id, message.from_user.username
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = (types.KeyboardButton(button_text) for button_text in config.start_buttons)
    markup.add(*buttons)
    bot.send_message(chat_id,
                     text=f"Hello, {username}! {config.intro_text}",
                     reply_markup=markup)
    if not check_existence(username):
        insert_user(username=username)


def get_gender(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(text=gender,
                                          callback_data=gender)
               for gender in config.genders]
    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'Choose your genders:\n P.S. most of out users desire to know it before a meeting)',
                     reply_markup=keyboard)


def get_age(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=age,
                                          callback_data=age)
               for age in config.ages]
    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'Great! Now enter your age group:',
                     reply_markup=keyboard)


def get_hobbies(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=hobby,
                                          callback_data=hobby)
               for hobby in config.common_hobbies]

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'Excellent! Tell me about your interests. You are supposed to choose from 1 to 8 options:',
                     reply_markup=keyboard)


def get_conv_topics(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=topic,
                                          callback_data=topic)
               for topic in config.common_conv_topics]

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'Finally: what do you prefer to talk about? (mention at least 1 point 😄)',
                     reply_markup=keyboard)


def back_to_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = (types.KeyboardButton(button_text) for button_text in config.start_buttons)
    markup.add(*buttons)
    bot.send_message(chat_id, text="You are in the main menu now", reply_markup=markup)


# CODE DOUBLING!!
@bot.callback_query_handler(func=lambda call: True)
def update_data(call):
    if call.message:
        answer = call.data
        username = call.message.chat.username
        stage = get_user_tb_column_val(username, "stage")
        chat_id = call.message.chat.id
        if answer in config.genders and stage == 0:
            update_user_tb(username, "gender", answer)
            bot.send_message(chat_id, text=f'Gender has been changed to "{answer}"')
            get_age(chat_id)
            update_user_tb(username, "stage", 1)
        elif answer in config.ages and stage == 1:
            update_user_tb(username, "age", answer)
            bot.send_message(chat_id, text=f'Age has been changed to "{answer}"')
            get_hobbies(chat_id)
            update_user_tb(username, "stage", 2)
        elif answer in config.common_hobbies and answer != 'DONE' and stage in [2, 3]:
            update_user_hobbies_tb(username, answer)
            bot.send_message(chat_id, text=f'Hobby "{answer}" has been added')
            update_user_tb(username, "stage", 3)
        elif answer == 'DONE' and stage == 3:
            bot.send_message(chat_id, text='Hobbies are filled! It it time for conversation topics now!')
            get_conv_topics(chat_id)
            update_user_tb(username, "stage", 4)
        elif answer in config.common_conv_topics and answer != 'FINISH' and stage in [4, 5]:
            update_user_topics_tb(username, answer)
            bot.send_message(chat_id, text=f'Topic "{answer}" has been added')
            update_user_tb(username, "stage", 5)
        elif answer == 'FINISH' and stage == 5:
            bot.send_message(chat_id,
                             text='Awesome! Finally add a little self-description ')


@bot.message_handler(content_types=['text'])
def communicate(message):
    message_text = message.text
    username = message.from_user.username
    stage = get_user_tb_column_val(username, "stage")
    chat_id = message.chat.id
    if message_text == "Найти похожее событие":
        if stage == 6:
            bot.send_message(chat_id, text="Describe me that!")
        else:
            bot.send_message(chat_id, text="You have to fill information about yourself for start!")
    elif message_text == "Создать событие":
        if stage == 6:
            bot.send_message(chat_id, text="Describe the event you wanna add!")
        else:
            bot.send_message(chat_id, text="You have to fill information about yourself for start!")
    elif message_text == "Найти похожих юзеров":
        if stage == 6:
            bot.send_message(chat_id, "I'm about to match!")
        else:
            bot.send_message(chat_id, text="You have to fill information about yourself for start!")
    elif message_text == 'Редактировать профиль':
        update_user_tb(username, "stage", 0)
        bot.send_message(chat_id, "Let's start!")
        # start to getting data from user
        get_gender(chat_id)
    elif message_text == "Вернуться в главное меню":
        back_to_main_menu(chat_id)
    # now we are getting a self-description. otherwise we shall ignore a user
    elif stage == 5:
        update_user_tb(username, "self_description", message_text)
        bot.send_message(chat_id, text=f'Perfect! We have just finished.\nYour self-description\n"{message_text}"')
        update_user_tb(username, "stage", 6)


bot.polling(none_stop=True)
