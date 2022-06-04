import datetime
import threading
import time
import traceback

import telebot
from telebot import types

from ConstantsClass import Constants
from Database.UsersClass import Users, User
from Database.events_tb_action import insert_event, update_event_tb, get_all_events_by_day, delete_event, \
    get_event_by_creator, get_event_tb_column_val, find_old_events
from Database.users_tb_action import insert_user, check_existence, update_user_tb, update_user_hobbies_tb, \
    update_user_topics_tb, get_user_tb_column_val, get_interest_val, get_interest, reset_info
from Match.match_events import event_match
from Match.match_users import interests_match

bot = telebot.TeleBot(Constants.token)

users = Users()


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Handle command "/start":
    sends start-message, adds user to DB and shows main_menu buttons
    :param message: message from user
    :type: telebot.types.Message
    """
    chat_id, username = message.chat.id, message.from_user.username
    bot.send_message(chat_id,
                     text=f"Привет, {username}! {Constants.intro_text}")
    if not check_existence(username):
        insert_user(username=username)
        users.add_user(User(message.from_user.id, message.from_user.username))
    main_menu(message)


def main_menu(message):
    """
    Shows menu buttons
    :param message: message from user
    :type: telebot.types.Message
    """
    key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    key.row("Перейти в профиль")
    key.row("Посмотреть события")
    key.row("Найти похожих пользователей")
    send = bot.send_message(message.from_user.id, "Ты в главном меню", reply_markup=key)
    bot.register_next_step_handler(send, profile_events_match_buttons)
    update_user_tb(message.from_user.username, "searching_stage", 0)


def profile_events_match_buttons(message):
    """
    Handle menu buttons
    :param message: message from user
    :type: telebot.types.Message
    """
    if message.text == "Перейти в профиль":
        user_profile_text = get_user_profile_text(message.from_user.username)
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        key.row("Редактировать профиль")
        key.row("Вернуться в меню")
        send = bot.send_message(message.from_user.id, text=user_profile_text, reply_markup=key)
        bot.register_next_step_handler(send, edit_profile_buttons)
    elif message.text == "Посмотреть события":
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if get_event_by_creator(message.from_user.username):
            keyboard.row("Покажи мое событие")
            keyboard.row("Редактировать мое событие")
            keyboard.row("Удали мое событие")
            keyboard.row("Найти события по времени")
            keyboard.row("Вернуться в меню")
        else:
            keyboard.row("Создать событие")
            keyboard.row("Найти события по времени")
            keyboard.row("Вернуться в меню")
        send = bot.send_message(message.from_user.id, "Что мне сделать дальше?", reply_markup=keyboard)
        bot.register_next_step_handler(send, event_buttons)

    elif message.text == "Найти похожих пользователей":
        if get_user_tb_column_val(message.from_user.username, "info_stage") == 6:
            make_users_match(message.from_user.username, message.chat.id)
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.row("Показать еще пользователей")
            keyboard.row("Вернуться в меню")
            send = bot.send_message(message.chat.id, text="Лови чуваков ☝", reply_markup=keyboard)
            bot.register_next_step_handler(send, match_handler)
        else:
            bot.send_message(message.chat.id, text="Сначала расскажи о себе в профиле)")
            main_menu(message)
    else:
        main_menu(message)


def make_users_match(username, chat_id, start=Constants.start, top_n=Constants.top_n):
    """
    Sends user profiles of the most similar other users if possible
    sends start-message, adds user to DB and shows main_menu buttons
    :param username: user`s telegram name
    :type: string
    :param chat_id: user`s telegram chat id
    :type: int
    :param start:
        default=Constants.start
    :type: int
    :param top_n: the number of user profiles to show
    :type: id
    """
    challengers = interests_match(username)
    try:
        challengers = challengers[start:start + top_n]
    except IndexError:
        try:
            challengers = challengers[start:]
        except IndexError:
            challengers = None
    if challengers:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row("Показать еще пользователей")
        keyboard.row("В главное меню")
        bot.send_message(chat_id, text="Ищу людей...", reply_markup=keyboard)
        for user in challengers:
            bot.send_message(chat_id, text=get_user_profile_text(user[1]))
    else:
        bot.send_message(chat_id, text="Никого не нашел :(")


def match_handler(message):
    """
    Handle "Show more ..." buttons
    :param message: message from user
    :type: telebot.types.Message
    """
    if message.text == "Показать еще пользователей":
        users.get_user(message.from_user.id).match_users_row += 1
        attempt = users.get_user(message.from_user.id).match_users_row
        make_users_match(message.from_user.username, message.chat.id, start=Constants.start + attempt * Constants.top_n)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row("Показать еще пользователей")
        keyboard.row("Вернуться в меню")
        send = bot.send_message(message.chat.id, text="Лови чуваков ☝", reply_markup=keyboard)
        bot.register_next_step_handler(send, match_handler)

    elif message.text == "Показать еще события":
        users.get_user(message.from_user.id).match_events_row += 1
        attempt = users.get_user(message.from_user.id).match_events_row
        make_event_match(message.from_user.username, message.chat.id,
                         event_day=users.get_user(message.from_user.id).event_day,
                         event_time=users.get_user(message.from_user.id).event_time,
                         start=Constants.start + attempt * Constants.top_n)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row("Показать еще события")
        keyboard.row("Вернуться в меню")
        send = bot.send_message(message.chat.id, text="Лови события ☝", reply_markup=keyboard)
        bot.register_next_step_handler(send, match_handler)

    elif message.text == "Вернуться в меню":
        users.get_user(message.from_user.id).match_users_row = 0
        users.get_user(message.from_user.id).match_events_row = 0
        main_menu(message)


def event_buttons(message):
    """
    Handle event buttons
    :param message: message from user
    :type: telebot.types.Message
    """
    if message.text == "Редактировать мое событие" or message.text == "Создать событие":
        delete_event(message.from_user.username)
        insert_event(message.from_user.username)
        update_user_tb(message.from_user.username, "event_stage", 0)
        get_date(message.chat.id)
    elif message.text == "Найти события по времени":
        update_user_tb(message.from_user.username, "searching_stage", 1)
        get_date(message.chat.id)
    elif message.text == "Вернуться в меню":
        main_menu(message)
    elif message.text == "Покажи мое событие":
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        key.row("Покажи мое событие")
        key.row("Редактировать мое событие")
        key.row("Удали мое событие")
        key.row("Найти события по времени")
        key.row("Вернуться в меню")
        event_profile = get_event_profile_text(message.from_user.username)
        if event_profile:
            reply_text = event_profile
        else:
            reply_text = "Упс... что-то пошло не так"
        send = bot.send_message(message.from_user.id, text=reply_text, reply_markup=key)
        bot.register_next_step_handler(send, event_buttons)

    elif message.text == "Удали мое событие":
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        key.row("Создать событие")
        key.row("Найти события по времени")
        key.row("Вернуться в меню")

        delete_event(message.from_user.username)
        send = bot.send_message(message.from_user.id, text="Сделано!", reply_markup=key)
        bot.register_next_step_handler(send, event_buttons)


def get_date(chat_id):
    """
    Show to user inline buttons of getting date of event
    :param chat_id: id of the chat where the date is got (similar to user`s telegram id in our bot due to it`s specific)
    :type: int
    """
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    now = datetime.datetime.now()
    options = [(now + datetime.timedelta(days=i + 1)).strftime("%d.%m.%y") for i in range(7)]
    buttons = [types.InlineKeyboardButton(text=option,
                                          callback_data=option)
               for option in options]

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     "Введи дату:",
                     reply_markup=keyboard)


def get_time_period(chat_id):
    """
    Show to user inline buttons of getting time-period of event
    :param chat_id: id of the chat where the date is got (similar to user`s telegram id in our bot due to it`s specific)
    :type: int
    """
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=time_period,
                                          callback_data=time_period)
               for time_period in Constants.time_periods]

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     "Укажи, во сколько ты хотел бы начать:",
                     reply_markup=keyboard)


def edit_profile_buttons(message):
    """
    Handle profile edit button
    :param message: message from user
    :type: telebot.types.Message
    """
    if message.text == "Редактировать профиль":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if get_user_tb_column_val(message.from_user.username, "is_active"):
            keyboard.row("Изменить данные")
            keyboard.row("Выключить поиск")
            keyboard.row("Вернуться в меню")
        else:
            keyboard.row("Изменить данные")
            keyboard.row("Выключить поиск")
            keyboard.row("Вернуться в меню")
        send = bot.send_message(message.chat.id, text="Что хочешь сделать?", reply_markup=keyboard)
        bot.register_next_step_handler(send, edit_profile)
    elif message.text == "Вернуться в меню":
        main_menu(message)


def edit_profile(message):
    """
    Handle profile editing buttons
    :param message: message from user
    :type: telebot.types.Message
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if message.text == "Изменить данные":
        reset_info(message.from_user.username)
        get_gender(message.chat.id)
    elif message.text == "Включить поиск":
        update_user_tb(message.from_user.username, "is_active", 1)
        keyboard.row("Изменить данные")
        keyboard.row("Выключить поиск")
        keyboard.row("Вернуться в меню")
        send = bot.send_message(message.chat.id, text="Готово! Что дальше?", reply_markup=keyboard)
        bot.register_next_step_handler(send, edit_profile)
    elif message.text == "Выключить поиск":
        update_user_tb(message.from_user.username, "is_active", 0)
        keyboard.row("Изменить данные")
        keyboard.row("Включить поиск")
        keyboard.row("Вернуться в меню")
        send = bot.send_message(message.chat.id, text="Готово! Что дальше?", reply_markup=keyboard)
        bot.register_next_step_handler(send, edit_profile)
    elif message.text == "Вернуться в меню":
        main_menu(message)


def get_gender(chat_id):
    """
    Show to user inline buttons of getting his gender
    :param chat_id: id of the chat where the date is got (similar to user`s telegram id in our bot due to it`s specific)
    :type: int
    """
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=gender,
                                          callback_data=gender)
               for gender in Constants.genders]
    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'Выбери гендер:\nP.S. большинство юзеров хотели бы знать это перед встречей)',
                     reply_markup=keyboard)


def get_age(chat_id):
    """
    Show to user inline buttons of getting his age
    :param chat_id: id of the chat where the date is got (similar to user`s telegram id in our bot due to it`s specific)
    :type: int
    """
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=age,
                                          callback_data=age)
               for age in Constants.ages]
    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'Отлично! Теперь укажи свой возраст:',
                     reply_markup=keyboard)


def get_hobbies(chat_id):
    """
    Show to user inline buttons of getting his hobbies
    :param chat_id: id of the chat where the date is got (similar to user`s telegram id in our bot due to it`s specific)
    :type: int
    """
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=hobby,
                                          callback_data=hobby)
               for hobby in Constants.common_hobbies]

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'Замечательно! Расскажи о своих хобби? Выбери от 1 до 8 вариантов:',
                     reply_markup=keyboard)


def get_conv_topics(chat_id):
    """
    Show to user inline buttons of getting his favourite conversation topics
    :param chat_id: id of the chat where the date is got (similar to user`s telegram id in our bot due to it`s specific)
    :type: int
    """
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=topic,
                                          callback_data=topic)
               for topic in Constants.common_conv_topics]

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'С хобби закончили!\nА о чем ты предпочитаешь поговорить? Выбери от 1 до 8 вариантов:',
                     reply_markup=keyboard)


def self_describing(message):
    """
    Ask user to write his self description
    :param message: message from user
    :type: telebot.types.Message
    """
    update_user_tb(message.from_user.username, "self_description", message.text)
    main_menu(message)


def event_describing(message):
    """
    Ask user to write event description
    :param message: message from user
    :type: telebot.types.Message
    """
    update_event_tb(message.from_user.username, "description", message.text)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row("Покажи мое событие")
    keyboard.row("Редактировать мое событие")
    keyboard.row("Удали мое событие")
    keyboard.row("Найти события по времени")
    keyboard.row("Вернуться в меню")
    sent = bot.send_message(message.from_user.id, "Готово! Что дальше?", reply_markup=keyboard)
    bot.register_next_step_handler(sent, event_buttons)


def make_event_match(username, chat_id, event_day=None, event_time=None, start=Constants.start):
    """
    Sends events` describes with their creators` profiles relying on the biggest similarity of user and creators in the definite day

    :param username: user`s telegram name
    :type: string
    :param chat_id: user`s telegram chat id
    :type: int
    :param start:
        default=Constants.start
    :type: int
    :param event_day: the day when user wants to find events
    :type: string
    :param event_time: the most pleasant time when user wants to find events
    :type:
    :param start:
        default=Constants.start
    :type: int
    """
    #TODO
    # time type
    possible_options = get_all_events_by_day(event_day, username)
    if possible_options:
        best_options = event_match(username, event_day, event_time)
        try:
            best_options = best_options[start:start + Constants.top_n]
        except IndexError:
            try:
                best_options = best_options[start:]
            except IndexError:
                best_options = None

        if best_options:
            for option in best_options:
                creator_name = option[:3][0]
                event_profile = get_event_profile_text(creator_name)
                if event_profile:
                    bot.send_message(chat_id,
                                     text=event_profile)
    else:
        bot.send_message(chat_id, text="В этот день нет событий, но ты можешь создать свое событие!")

    update_user_tb(username, "searching_stage", 0)


def get_user_profile_text(username):
    """
    Returns text of user profile to show
    :param message: message from user
    :type: telebot.types.Message
    """
    user_hobbies = get_interest(username, "hobbies")
    user_hobbies = list(
        map(lambda x: list(Constants.hobbies_to_eng.keys())[list(Constants.hobbies_to_eng.values()).index(x)],
            user_hobbies))
    user_topics = get_interest(username, "topics")
    user_topics = list(
        map(lambda x: list(Constants.topics_to_eng.keys())[list(Constants.topics_to_eng.values()).index(x)],
            user_topics))
    user_hobbies = ", ".join(user_hobbies) if user_hobbies else "Пусто"
    user_topics = ", ".join(user_topics) if user_topics else "Пусто"
    self_description = get_user_tb_column_val(username, "self_description")
    return f"""Хобби:\n{user_hobbies}\n\nЛюбимые темы для разговора:\n{user_topics}\n\nО себе:\n"{self_description}"\n\nТэг в Телеграмме:\n@{username}"""


def get_event_profile_text(username):
    """
    Returns text of user`s event to show
    :param username: user`s telegram username
    :type: string
    """
    suggested_day = get_event_tb_column_val(username, "day")
    suggested_day = suggested_day.strftime("%d.%m.%y")
    suggested_time = get_event_tb_column_val(username, "time")
    description = get_event_tb_column_val(username, "description")
    author_description = get_user_profile_text(username)

    event_profile = f"День:\n{suggested_day}\n\nНачало:\n{suggested_time}\n\nОписание:\n{description}\n\nОб авторе:\n\n{author_description}"

    return event_profile


def get_chat_id_by_username(username):
    """
    Returns telegram id of user by his telegram username
    :param username: user`s telegram username
    :type: string
    """
    for user_id, user_class in users.users.items():
        if user_class.name == username:
            return user_id


def delete_and_notify():
    """
    Deletes all old events and sends notifies to their creators
    """
    users_to_notify = find_old_events()
    for author in users_to_notify:
        author_name = author[0]
        chat_id = get_chat_id_by_username(author_name)
        delete_event(author_name)
        bot.send_message(chat_id=chat_id, text=Constants.delete_notification.format(author_name))


def every(delay, task):
    """
    Delay function for an hour
    """
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except Exception:
            traceback.print_exc()
        next_time += (time.time() - next_time) // delay * delay + delay


# threading.Thread(target=lambda: every(3600, delete_and_notify)).start()


@bot.callback_query_handler(func=lambda call: True)
def update_user_data(call):
    if call.message:
        answer = call.data
        username = call.message.chat.username

        info_stage = get_user_tb_column_val(username, "info_stage")
        event_stage = get_user_tb_column_val(username, "event_stage")
        searching_stage = get_user_tb_column_val(username, "searching_stage")
        chat_id = call.message.chat.id
        now = datetime.datetime.now()
        day_options = [(now + datetime.timedelta(days=i + 1)).strftime("%d.%m.%y") for i in range(7)]

        if answer in Constants.genders and info_stage == 0:
            update_user_tb(username, "gender", answer)
            bot.send_message(chat_id, text=f'Гендер был изменен на "{answer}"')
            get_age(chat_id)
            update_user_tb(username, "info_stage", 1)
        elif answer in Constants.ages and info_stage == 1:
            update_user_tb(username, "age", answer)
            bot.send_message(chat_id, text=f'Возраст был изменен на "{answer}"')
            get_hobbies(chat_id)
            update_user_tb(username, "info_stage", 2)

        elif answer in Constants.common_hobbies and answer != 'DONE' and info_stage in [2, 3]:
            eng_answer = Constants.hobbies_to_eng[answer]
            if get_interest_val(username, eng_answer, hobbies=True) == 0:
                update_user_hobbies_tb(username, Constants.hobbies_to_eng[answer])
                bot.send_message(chat_id, text=f'Добавил хобби "{answer}"')
                update_user_tb(username, "info_stage", 3)

        elif answer == 'DONE' and info_stage == 3:
            get_conv_topics(chat_id)
            update_user_tb(username, "info_stage", 4)

        elif answer == 'DONE':
            bot.send_message(chat_id, text="Укажи хотя бы одно хобби 😈")

        elif answer in Constants.common_conv_topics and answer != 'FINISH' and info_stage in [4, 5]:
            eng_answer = Constants.topics_to_eng[answer]
            if get_interest_val(username, eng_answer, hobbies=False) == 0:
                update_user_topics_tb(username, Constants.topics_to_eng[answer])
                bot.send_message(chat_id, text=f'Добавил тему "{answer}"')
                update_user_tb(username, "info_stage", 5)

        elif answer == 'FINISH' and info_stage == 5:
            sent = bot.send_message(chat_id,
                                    text=Constants.sample_user_description)
            update_user_tb(username, "info_stage", 6)
            bot.register_next_step_handler(sent, self_describing)

        elif answer == 'FINISH':
            bot.send_message(chat_id, text="Укажи хотя бы одну тему 😈")

        elif answer in day_options and searching_stage == 1:
            answer = str(datetime.datetime.strptime(answer, "%d.%m.%y"))[:10].replace('-', '.')
            users.get_user(call.message.chat.id).event_day = answer
            bot.send_message(chat_id, text=f'День: {answer}\nТеперь выбери время:')
            get_time_period(chat_id)
            update_user_tb(username, "searching_stage", 2)

        elif answer in Constants.time_periods and searching_stage == 2:
            users.get_user(call.message.chat.id).event_time = answer
            bot.send_message(chat_id,
                             text=f'Принял! Учитывая время и интересы пользователей, думаю, эти варианты неплохи:')

            make_event_match(username, chat_id, users.get_user(call.message.chat.id).event_day,
                             users.get_user(call.message.chat.id).event_time)

            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.row("Показать еще события", "Вернуться в меню")
            sent = bot.send_message(call.message.chat.id, "Готово! Что дальше?", reply_markup=keyboard)
            bot.register_next_step_handler(sent, match_handler)

        elif answer in day_options and event_stage == 0:
            answer = str(datetime.datetime.strptime(answer, "%d.%m.%y"))[:10].replace('-', '.')
            update_event_tb(username, "day", answer)
            update_user_tb(username, "event_stage", 1)
            bot.send_message(chat_id, text=f'Отлично! День: {answer}\nТеперь введи время:')
            get_time_period(chat_id)

        elif answer in Constants.time_periods and event_stage == 1:
            update_event_tb(username, "time", answer)
            sent = bot.send_message(chat_id,
                                    text=f'Начало: "{answer}"' + Constants.sample_event_description)
            update_user_tb(username, "event_stage", 2)
            bot.register_next_step_handler(sent, event_describing)


bot.polling(none_stop=True)
