import telebot
from telebot import types
import config
from users_tb_action import insert_user, check_existence, update_user_tb, update_user_hobbies_tb, update_user_topics_tb, \
    get_user_tb_column_val, get_interest_val, get_interest
from match_users import interests_match
from events_tb_action import insert_event, update_event_tb, get_all_events_by_day
from match_events import event_match
import datetime

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id, username = message.chat.id, message.from_user.username
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = (types.KeyboardButton(button_text) for button_text in config.start_buttons)
    markup.add(*buttons)
    bot.send_message(chat_id,
                     text=f"Привет, {username}! {config.intro_text}",
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
                     'Выбери гендер:\nP.S. большинство юзеров хотели бы знать это перед встречей)',
                     reply_markup=keyboard)


def get_age(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=age,
                                          callback_data=age)
               for age in config.ages]
    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'Отлично! Теперь укажи свой возраст:',
                     reply_markup=keyboard)


def get_hobbies(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=hobby,
                                          callback_data=hobby)
               for hobby in config.common_hobbies]

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'Замечательно! Расскажи о своих хобби? ***Выбери от 1 до 8 вариантов:***',
                     reply_markup=keyboard, parse_mode="Markdown")


def get_conv_topics(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=topic,
                                          callback_data=topic)
               for topic in config.common_conv_topics]

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'С хобби закончили!\nА о чем ты предпочитаешь поговорить? ***Выбери от 1 до 8 вариантов:***',
                     reply_markup=keyboard, parse_mode="Markdown")


# СДЕЛАЛ ВОТ ТАКУЮ ШТУКУ
# +- ТО ЖЕ, ЧТО У ТЕБЯ -- Ю НОУ
# КОГДА ЮЗЕР ИЩЕТ СОБЫТИЯ ИЛИ ДРУГИХ ЮЗЕРОВ, У НЕГО 2 КНОПКИ: "В МЕНЮ" И "ЕЩЕ"
# ДАЛЕЕ ОПИШУ, ЧТО Я СДЕЛАЛ С "ЕЩЕ"
def back_to_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = (types.KeyboardButton(button_text) for button_text in config.start_buttons)
    markup.add(*buttons)
    bot.send_message(chat_id, text="Ты в главном меню", reply_markup=markup)


# В ФУНКЦИЯХ МЭТЧА ВЫТАСКИВАЮ ВООБЩЕ ВСЕ ОБЪЕКТЫ, А ПОТОМ БЕРУ ОПРЕДЕЛЕННЫЙ СРЕЗ ПО УСЛОВИЮ
# В СЛОВАРЕ ЮЗЕРОВ (КОСТЫЫЫЛЬ) Я ХРАНЮ ДЛЯ КАЖДОГО, СКОЛЬКО МЭТЧЕЙ ПОДРЯД ОН ДЕЛАЕТ
# И В ЗАВИСИМОСТИ ОТ ЭТОГО БЕРУ ЛИБО СНАЧАЛА TOP_N, ЛИБО С ОПРЕДЕЛЕННОГО МОМЕНТА
# КОГДА ЮЗЕР УХОДИТ В ГЛАВНОЕ МЕНЮ, СБРАСЫВАЮ ЭТИ ПЕРЕМЕННЫЕ ДО НУЛЕЙ
# СОБСТВЕННО, ВСЕ, ЧТО Я СДЕЛАЛ
# В КЛАССЕ ЮЗЕРА МОЖНО ХРАНИТЬ ЭТИ И НЕКОТОРЫЕ ДРУГИЕ АТРИБУТЫ И ДЕЛАТЬ ЭТО КРАСИВО

# ТАКЖЕ Я ЗАНЕС В CONFIG TOP_N И START (МЕСТО, ОТКУДА ДЕЛАЮ МЭТЧ), ЧТОБ НЕ ХАРДКОДИТЬ СЛИШКОМ
def make_user_match(username, chat_id, start=config.start, top_n=config.top_n):
    challengers = interests_match(username)
    try:
        challengers = challengers[start:start + top_n]
    except IndexError:
        try:
            challengers = challengers[start:]
        except IndexError:
            challengers = None
    if challengers:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton("Еще"), types.KeyboardButton("В главное меню")]
        markup.add(*buttons)

        bot.send_message(chat_id, text="По-моему, эти чуваки могли бы составить тебе компанию:", reply_markup=markup)
        for challenger in challengers:
            challenger_hobbies = ', '.join(challenger[2])
            challenger_topics = ', '.join(challenger[3])
            bot.send_message(chat_id,
                             text=f"""***Хобби:***\n{challenger_hobbies}\n\n***Любимые темы для разговора:***\n{challenger_topics}\n\n***О себе:***\n"{challenger[5]}"\n\n***Возраст:*** {challenger[4]}\n\n***Тэг в Телеграмме:***\n@{challenger[1]}""",
                             parse_mode="Markdown")
    else:
        bot.send_message(chat_id, text="Никого не нашел :(")

# ТУТ ТОЖЕ НЕБОЛЬШИЕ ИЗМЕНЕНИЯ
# + ЗАПРЕТИЛ ЮЗЕРУ ИСКАТЬ СОБЫТИЯ ИЗ ПРОШЛОГО
# НАДО НЕ ЗАБЫТЬ НАПИСАТЬ ФУНКЦИЮ ДЛЯ УДАЛЕНИЯ СТАРЫХ СОБЫТИЙ
# ОНА ИЗИ. + КИДАТЬ СООБЩЕНИЕ ЮЗЕРУ, ЧТО СОБЫТИЕ УДАЛЕНО, И ОН МОЖЕТ СОЗДАТЬ НОВОЕ
# ЕЩЕ ДОБАВИЛ В ВЫВОД ВОЗРАСТ ЮЗЕРОВ, А ТО ЧЕТ ЗАБЫЛИ
def make_event_match(username, chat_id, event_day=None, event_time=None, start=config.start, top_n=config.top_n):
    now = datetime.datetime.now()
    curr_time = str(datetime.time(now.hour, now.minute))
    curr_day = str(datetime.date(now.year, now.month, now.day))
    if curr_time > event_time[-4:] and curr_day.replace('-', '.') == event_day and event_time != "После 21:00":
        bot.send_message(chat_id, text="Не могу сделать мэтч в прошлое :)")
    else:
        possible_options = get_all_events_by_day(event_day)
        if possible_options:
            best_options = event_match(username, event_day, event_time)
            try:
                best_options = best_options[start:start + top_n]
            except IndexError:
                try:
                    best_options = best_options[start:]
                except IndexError:
                    best_options = None
            if best_options:
                for option in best_options:
                    creator_name, suggested_time, event_description = option[:3]
                    creator_age = get_user_tb_column_val(creator_name, "age")
                    bot.send_message(chat_id,
                                     text=f"""***Начало:***\n{suggested_time}\n\n***Описание:***\n{event_description}\n\n***Возраст:***\n{creator_age}\n\n***Автор:***\n@{creator_name}""",
                                     parse_mode="Markdown")
            else:
                bot.send_message(chat_id,
                                 text="На этом все (")
        else:
            bot.send_message(chat_id, text="В этот день пока что никто не тусит, но ты можешь создать свое событие!")

        update_user_tb(username, "searching_stage", 0)


def reset_info(username):
    update_user_tb(username, "info_stage", 0)
    for hobby in config.hobbies_to_eng.values():
        update_user_hobbies_tb(username, hobby, 0)
    for topic in config.topics_to_eng.values():
        update_user_topics_tb(username, topic, 0)


def show_user_profile(username, chat_id):
    user_hobbies, user_topics = get_interest(username, 'hobbies')[0], get_interest(username, 'topics')[0]
    user_hobbies = list(
        map(lambda x: list(config.hobbies_to_eng.keys())[list(config.hobbies_to_eng.values()).index(x)],
            user_hobbies))
    user_topics = list(
        map(lambda x: list(config.topics_to_eng.keys())[list(config.topics_to_eng.values()).index(x)],
            user_topics))
    user_hobbies = ", ".join(user_hobbies)
    user_topics = ", ".join(user_topics)
    self_description = get_user_tb_column_val(username, "self_description")
    bot.send_message(chat_id,
                     text=f"""***Хобби:***\n{user_hobbies}\n\n***Любимые темы для разговора:***\n{user_topics}\n\n***О себе:***\n"{self_description}"\n\n***Тэг в Телеграмме:***\n@{username}""",
                     parse_mode="Markdown")


# КОСТЫЛИЩЕ
users = {}

# В ХЭНДЛЕР-ФУНКЦИЯХ ЕЩЕ ПАРОЧКА ИФОВ, СООТВЕТСТВЕННО (ЗАЕБАЛИ УЖЕ)
@bot.callback_query_handler(func=lambda call: True)
def update_user_data(call):
    if call.message:
        answer = call.data
        username = call.message.chat.username
        if username not in users:
            users[username] = {"event_day": None, "event_time": None, "match_users_row": 0, "match_events_row": 0}

        info_stage = get_user_tb_column_val(username, "info_stage")
        event_stage = get_user_tb_column_val(username, "event_stage")
        searching_stage = get_user_tb_column_val(username, "searching_stage")
        chat_id = call.message.chat.id
        now = datetime.datetime.now()
        day_options = [(now + datetime.timedelta(days=i)).strftime("%d.%m.%y") for i in range(8)]

        if answer in config.genders and info_stage == 0:
            update_user_tb(username, "gender", answer)
            bot.send_message(chat_id, text=f'Гендер был изменен на "{answer}"')
            get_age(chat_id)
            update_user_tb(username, "info_stage", 1)

        elif answer in config.ages and info_stage == 1:
            update_user_tb(username, "age", answer)
            bot.send_message(chat_id, text=f'Возраст был изменен на "{answer}"')
            get_hobbies(chat_id)
            update_user_tb(username, "info_stage", 2)

        elif answer in config.common_hobbies and answer != 'DONE' and info_stage in [2, 3]:
            eng_answer = config.hobbies_to_eng[answer]
            if get_interest_val(username, eng_answer, hobbies=True) == 0:
                update_user_hobbies_tb(username, config.hobbies_to_eng[answer])
                bot.send_message(chat_id, text=f'Добавил хобби "{answer}"')
                update_user_tb(username, "info_stage", 3)

        elif answer == 'DONE' and info_stage == 3:
            get_conv_topics(chat_id)
            update_user_tb(username, "info_stage", 4)

        elif answer in config.common_conv_topics and answer != 'FINISH' and info_stage in [4, 5]:
            eng_answer = config.topics_to_eng[answer]
            if get_interest_val(username, eng_answer, hobbies=False) == 0:
                update_user_topics_tb(username, config.topics_to_eng[answer])
                bot.send_message(chat_id, text=f'Добавил тему "{answer}"')
                update_user_tb(username, "info_stage", 5)

        elif answer == 'FINISH' and info_stage == 5:
            bot.send_message(chat_id,
                             text='Круто!\nНаконец, кратко опиши себя:')
            update_user_tb(username, "info_stage", 6)

        elif answer in day_options and searching_stage == 1:
            answer = str(datetime.datetime.strptime(answer, "%d.%m.%y"))[:10].replace('-', '.')
            users[username]["event_day"] = answer
            bot.send_message(chat_id, text=f'День: {answer}\nТеперь выбери время:')
            get_time_period(chat_id)
            update_user_tb(username, "searching_stage", 2)

        elif answer in config.time_periods and searching_stage == 2:
            users[username]["event_time"] = answer
            make_event_match(username, chat_id, users[username]["event_day"], users[username]["event_time"])

        elif answer in day_options and event_stage == 0:
            answer = str(datetime.datetime.strptime(answer, "%d.%m.%y"))[:10].replace('-', '.')
            update_event_tb(username, "day", answer)
            update_user_tb(username, "event_stage", 1)
            bot.send_message(chat_id, text=f'Отлично! День: {answer}\nТеперь введи время:')
            get_time_period(chat_id)

        elif answer in config.time_periods and event_stage == 1:
            update_event_tb(username, "time", answer)
            bot.send_message(chat_id, text=f'Начало: "{answer}"\nКратко опиши событие:')
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
                     "Введи дату:",
                     reply_markup=keyboard)


def get_time_period(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=time_period,
                                          callback_data=time_period)
               for time_period in config.time_periods]

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     "Укажи, во сколько ты хотел бы начать:",
                     reply_markup=keyboard)


def change_activity_status(username, chat_id):
    curr_activity = get_user_tb_column_val(username, "is_active")
    if curr_activity == 1:
        update_user_tb(username, "is_active", 0)
        bot.send_message(chat_id,
                         text="Теперь тебя не потревожат!")
    else:
        update_user_tb(username, "is_active", 1)
        bot.send_message(chat_id,
                         text="Ты снова виден другим!")


@bot.message_handler(content_types=['text'])
def communicate(message):
    message_text = message.text
    username = message.from_user.username
    info_stage = get_user_tb_column_val(username, "info_stage")
    event_stage = get_user_tb_column_val(username, "event_stage")
    chat_id = message.chat.id

    if username not in users:
        users[username] = {"event_day": None, "event_time": None, "match_users_row": 0, "match_events_row": 0}

    if message_text == "Найти событие":
        if info_stage == 7:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [types.KeyboardButton("Далее"), types.KeyboardButton("В главное меню")]
            markup.add(*buttons)
            bot.send_message(chat_id, text="Опиши мне его!", reply_markup=markup)
            update_user_tb(username, "searching_stage", 1)
            get_date(chat_id)
        else:
            bot.send_message(chat_id, text='Для начала расскажи о себе в ***Редактировать профиль***!',
                             parse_mode="Markdown")

    elif message_text == "Создать событие":
        if info_stage == 7:
            if event_stage != 3:
                insert_event(username)
                bot.send_message(chat_id, text="Опиши мне его!\nУкажи дату:")
                get_date(chat_id)
            else:
                bot.send_message(chat_id, text="Ты уже создал событие(\nЕго можно редактировать или удалить")
        else:
            bot.send_message(chat_id, text='Для начала расскажи о себе в ***Редактировать профиль***!',
                             parse_mode="Markdown")

    elif message_text == "Найти похожих юзеров":
        if info_stage == 7:
            make_user_match(username, chat_id, start=config.start)
        else:
            bot.send_message(chat_id, text='Для начала расскажи о себе в ***Редактировать профиль***!',
                             parse_mode="Markdown")

    elif message_text == "Еще":
        attempt = users[username]["match_users_row"] + 1
        make_user_match(username, chat_id, start=config.start + config.top_n * attempt)
        users[username]["match_users_row"] += 1

    elif message_text == "Далее":
        attempt = users[username]["match_events_row"] + 1
        make_event_match(username, chat_id, users[username]["event_day"], users[username]["event_time"],
                         start=config.start + config.top_n * attempt)
        users[username]["match_events_row"] += 1

    elif message_text == 'Редактировать профиль':
        # clear old info
        reset_info(username)
        # start to getting data from user
        bot.send_message(chat_id, "Давай начнем!")
        get_gender(chat_id)

    elif message_text == "В главное меню":
        back_to_main_menu(chat_id)
        users[username]["match_users_row"] = 0
        users[username]["match_events_row"] = 0

    # now we are getting a self-description. otherwise we shall ignore a user
    elif info_stage == 6 and message_text:
        update_user_tb(username, "self_description", message_text)
        bot.send_message(chat_id,
                         text=f'Твое описание:\n"{message_text}"\n\n***Ты можешь ввести информацию о себе сначала в "Редактировать профиль", если захочешь изменить что-то***',
                         parse_mode="Markdown")
        update_user_tb(username, "info_stage", 7)

    elif message_text == "Сменить видимость":
        change_activity_status(username, chat_id)

    elif message_text == "Мой профиль":
        if info_stage == 7:
            show_user_profile(username, chat_id)
        else:
            bot.send_message(chat_id,
                             text='Пока что ты не указал о себе нужную информацию)\nМожешь сделать это в ***"Редактировать профиль"***',
                             parse_mode="Markdown")

    elif event_stage == 2 and message_text:
        update_event_tb(username, "description", message_text)
        bot.send_message(chat_id,
                         text=f'Описание события:\n"{message_text}"\n\n***Ты можешь изменить или удалить его***',
                         parse_mode="Markdown")
        update_user_tb(username, "event_stage", 3)


bot.polling(none_stop=True)
