import telebot
from telebot import types
import config
from users_tb_action import insert_user, check_existence, update_user_tb, update_user_hobbies_tb, update_user_topics_tb, \
    get_user_tb_column_val
from match_users import interests_match
from events_tb_action import insert_event, update_event_tb
import re
import datetime

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
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=gender,
                                          callback_data=gender)
               for gender in config.genders]
    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'Choose your genders:\nP.S. most of out users desire to know it before a meeting)',
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
                     'Hobbies are filled!\nFinally: what do you prefer to talk about? (mention at least 1 point 😄)',
                     reply_markup=keyboard)


def back_to_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = (types.KeyboardButton(button_text) for button_text in config.start_buttons)
    markup.add(*buttons)
    bot.send_message(chat_id, text="You are in the main menu now", reply_markup=markup)


def match_user(username, chat_id):
    challengers = interests_match(username)
    if challengers:
        bot.send_message(chat_id, text="По-моему, эти чуваки могли бы составить тебе компанию:")
        for challenger in challengers:
            bot.send_message(chat_id,
                             text=f"""***Хобби:***\n{', '.join(challenger[1])}\n\n***Любимые темы для разговора:***\n{', '.join(challenger[2])}\n\n***О себе:***\n"{challenger[3]}"\n\n***Тэг в Телеграмме:***\n@{challenger[0]}""",
                             parse_mode="Markdown")
    else:
        bot.send_message(chat_id, text="Пока что я не могу ни с кем тебя помэтчить :(")


@bot.callback_query_handler(func=lambda call: True)
def update_user_data(call):
    if call.message:
        answer = call.data
        username = call.message.chat.username
        info_stage = get_user_tb_column_val(username, "info_stage")
        event_stage = get_user_tb_column_val(username, "event_stage")
        chat_id = call.message.chat.id
        now = datetime.datetime.now()
        day_options = [(now + datetime.timedelta(days=i)).strftime("%d.%m.%y") for i in range(8)]
        if answer in config.genders and info_stage == 0:
            update_user_tb(username, "gender", answer)
            bot.send_message(chat_id, text=f'Gender has been changed to "{answer}"')
            get_age(chat_id)
            update_user_tb(username, "info_stage", 1)
        elif answer in config.ages and info_stage == 1:
            update_user_tb(username, "age", answer)
            bot.send_message(chat_id, text=f'Age has been changed to "{answer}"')
            get_hobbies(chat_id)
            update_user_tb(username, "info_stage", 2)
        elif answer in config.common_hobbies and answer != 'DONE' and info_stage in [2, 3]:
            update_user_hobbies_tb(username, config.hobbies_to_eng[answer])
            bot.send_message(chat_id, text=f'Hobby "{answer}" has been added')
            update_user_tb(username, "info_stage", 3)
        elif answer == 'DONE' and info_stage == 3:
            get_conv_topics(chat_id)
            update_user_tb(username, "info_stage", 4)
        elif answer in config.common_conv_topics and answer != 'FINISH' and info_stage in [4, 5]:
            update_user_topics_tb(username, config.topics_to_eng[answer])
            bot.send_message(chat_id, text=f'Topic "{answer}" has been added')
            update_user_tb(username, "info_stage", 5)
        elif answer == 'FINISH' and info_stage == 5:
            bot.send_message(chat_id,
                             text='Awesome!\nEventually add a little self-description:')
            update_user_tb(username, "info_stage", 6)
        elif answer in day_options and event_stage == 0:
            update_event_tb(username, "day", answer)
            update_user_tb(username, "event_stage", 1)
            bot.send_message(chat_id, text=f'Great! Day is {answer}. Now enter time:')
            get_time_period(chat_id)
        elif answer in config.time_periods and event_stage == 1:
            update_event_tb(username, "time", answer)
            bot.send_message(chat_id, text=f'Ok, time is "{answer}"\nMake a little event description:')
            update_user_tb(username, "event_stage", 2)


def get_date(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    now = datetime.datetime.now()
    options = [(now + datetime.timedelta(days=i)).strftime("%d.%m.%y") for i in range(8)]
    buttons = [types.InlineKeyboardButton(text=option,
                                          callback_data=option)
               for option in options]

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     "Enter event's date:",
                     reply_markup=keyboard)


def get_time_period(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=time_period,
                                          callback_data=time_period)
               for time_period in config.time_periods]

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     "Enter event's beginning time:",
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def communicate(message):
    message_text = message.text
    username = message.from_user.username
    info_stage = get_user_tb_column_val(username, "info_stage")
    event_stage = get_user_tb_column_val(username, "event_stage")
    chat_id = message.chat.id
    if message_text == "Find event":
        if info_stage == 7:
            bot.send_message(chat_id, text="Describe me that!")
        else:
            bot.send_message(chat_id, text="You have to fill information about yourself for start!")
    elif message_text == "Create event":
        if info_stage == 7:
            if event_stage != 3:
                insert_event(username)
                bot.send_message(chat_id, text="Describe the event you wanna add!\nChoose the date:")
                get_date(chat_id)
            else:
                bot.send_message(chat_id, text="You have already registered your event(\nYou may delete or edit it")
        else:
            bot.send_message(chat_id, text="You have to fill information about yourself for start!")
    elif message_text == "Find similar users":
        if info_stage == 7:
            match_user(username, chat_id)
        else:
            bot.send_message(chat_id, text="You have to fill information about yourself for start!")
    elif message_text == 'Edit my profile':
        update_user_tb(username, "info_stage", 0)
        bot.send_message(chat_id, "Let's start!")
        # start to getting data from user
        get_gender(chat_id)
    elif message_text == "Back to main menu":
        back_to_main_menu(chat_id)
    elif event_stage == 2:
        update_event_tb(username, "description", message_text)
        bot.send_message(chat_id,
                         text=f'Event description:\n"{message_text}"\nYou may change it later')
        update_user_tb(username, "event_stage", 3)
    # now we are getting a self-description. otherwise we shall ignore a user
    elif info_stage == 6:
        update_user_tb(username, "self_description", message_text)
        bot.send_message(chat_id,
                         text=f'Your self-description:\n"{message_text}"\nYou may change info with "Edit my profile"')
        update_user_tb(username, "info_stage", 7)


bot.polling(none_stop=True)
