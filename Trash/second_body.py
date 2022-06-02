import telebot
from telebot import types
import ConstantsClass
from Database.users_tb_action import update_user_tb, update_user_hobbies_tb, update_user_topics_tb, \
    get_user_tb_column_val
from Match.match_users import interests_match, extract_features
from Database.events_tb_action import get_all_events_by_day
from Match.match_events import event_match
import datetime

bot = telebot.TeleBot(config.token)

a = telebot.types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start'])
def menu(message):
    chat_id, username = message.chat.id, message.from_user.username
    key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    key.row("Мой профиль", "События", "Найти похожих юзеров")
    send = bot.send_message(message.from_user.id, "Ты в главном меню", reply_markup=key)
    bot.register_next_step_handler(send, profile_or_events)

    # if not check_existence(username):
    #     insert_user(username=username)


def profile_or_events(message):
    chat_id, username = message.chat.id, message.from_user.username
    if message.text == "Мой профиль":
        # show_user_profile("username", chat_id)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row("Редактировать", "Вернуться в меню")
        send = bot.send_message(message.from_user.id, "Ваш профиль", reply_markup=keyboard)
        bot.register_next_step_handler(send, get_gender_or_menu)
    # elif message.text == "События":
    #     keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    #     keyboard.row("Найти похожих юзеров", "6")
    #     send = bot.send_message(message.from_user.id, "2lvl", reply_markup=keyboard)
    #     bot.register_next_step_handler(send, third)
    # elif message.text == "Найти похожих юзеров":
    #     make_user_match(username, chat_id)


def get_gender_or_menu(message):
    if message.text == "Редактировать":
        # bot.send_message(message.from_user.id,
        #                  "Большинство пользователей хотели бы знать твой гендер перед встречей",
        #                  reply_markup=a)

        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        buttons = [types.InlineKeyboardButton(text=gender,
                                              callback_data=gender)
                   for gender in config.genders]

        keyboard.row(*buttons)
        send = bot.send_message(message.from_user.id,
                         'Укажи гендер',
                         reply_markup=keyboard)
        bot.register_next_step_handler(send, get_age)

    if message.text == "Вернуться в меню":
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        key.row("Мой профиль", "События", "Найти похожих юзеров")
        send = bot.send_message(message.from_user.id, "Ты в главном меню", reply_markup=key)
        bot.register_next_step_handler(send, profile_or_events)

def get_age(message):
    if message.text in config.genders:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        buttons = [types.InlineKeyboardButton(text=age,
                                              callback_data=age)
                   for age in config.ages]
        keyboard.add(*buttons)

        send = bot.send_message(message.from_user.id,
                         'Укажи возраст',
                         reply_markup=keyboard)
        bot.register_next_step_handler(send, get_hobbies)

def get_hobbies(message):
    if message.text in config.ages:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        buttons = [types.InlineKeyboardButton(text=hobby,
                                              callback_data=hobby)
                   for hobby in config.common_hobbies]
        keyboard.add(*buttons)
        send = bot.send_message(message.from_user.id,
                                'Укажи свои хобби',
                                reply_markup=keyboard)
        bot.register_next_step_handler(send, get_topics)

def get_topics(message):
    if message.text == "DONE":
        print(1)
    elif message.text in config.common_hobbies:
        #update
        pass



# def get_gender(message):
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     buttons = [types.InlineKeyboardButton(text=gender,
#                                           callback_data=gender)
#                for gender in config.genders]
#     keyboard.add(*buttons)
#     bot.send_message(chat_id,
#                      'Выбери гендер:\nP.S. большинство юзеров хотели бы знать это перед встречей)',
#                      reply_markup=keyboard)


# def get_age(chat_id):
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     buttons = [types.InlineKeyboardButton(text=age,
#                                           callback_data=age)
#                for age in config.ages]
#     keyboard.add(*buttons)
#     bot.send_message(chat_id,
#                      'Отлично! Теперь укажи свой возраст:',
#                      reply_markup=keyboard)


# def get_hobbies(chat_id):
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     buttons = [types.InlineKeyboardButton(text=hobby,
#                                           callback_data=hobby)
#                for hobby in config.common_hobbies]
#
#     keyboard.add(*buttons)
#     bot.send_message(chat_id,
#                      'Замечательно! Расскажи о своих хобби? ***Выбери от 1 до 8 вариантов:***',
#                      reply_markup=keyboard, parse_mode="Markdown")


def get_conv_topics(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=topic,
                                          callback_data=topic)
               for topic in config.common_conv_topics]

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                     'С хобби закончили!\nА о чем ты предпочитаешь поговорить? ***Выбери от 1 до 8 вариантов:***',
                     reply_markup=keyboard, parse_mode="Markdown")


def edit_event(username, chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=event_edit,
                                          callback_data=event_edit)
               for event_edit in ["Удалить", "Изменить"]]
    keyboard.add(*buttons)
    bot.send_message(chat_id, text="Ты уже создал событие(\nЕго можно редактировать или удалить",
                     reply_markup=keyboard)


def back_to_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = (types.KeyboardButton(button_text) for button_text in config.start_buttons)
    markup.add(*buttons)
    bot.send_message(chat_id, text="Ты в главном меню!", reply_markup=markup)


# It is not logical that this piece of code is here, not in match_users.py
def make_user_match(username, chat_id):
    challengers = interests_match(username)
    if challengers:
        bot.send_message(chat_id, text="По-моему, эти чуваки могли бы составить тебе компанию:")
        for challenger in challengers:
            challenger_hobbies = ', '.join(challenger[1])
            challenger_topics = ', '.join(challenger[2])
            bot.send_message(chat_id,
                             text=f"""***Хобби:***\n{challenger_hobbies}\n\n***Любимые темы для разговора:***\n{challenger_topics}\n\n***О себе:***\n"{challenger[3]}"\n\n***Тэг в Телеграмме:***\n@{challenger[0]}""",
                             parse_mode="Markdown")
    else:
        bot.send_message(chat_id, text="Пока что я не могу ни с кем тебя помэтчить :(")


def make_event_match(username, chat_id, event_day=None, event_time=None):
    possible_options = get_all_events_by_day(event_day, username)
    if possible_options:
        best_options = event_match(username, event_day, event_time)
        for option in best_options:
            creator_name, suggested_time, event_description = option[:3]
            bot.send_message(chat_id,
                             text=f"""***Начало:***\n{suggested_time}\n\n***Описание:***\n{event_description}\n\n***Автор:***\n@{creator_name}""",
                             parse_mode="Markdown")
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
    user_hobbies, user_topics = extract_features(username)[:2]
    user_hobbies = ", ".join(user_hobbies)
    user_topics = ", ".join(user_topics)
    self_description = get_user_tb_column_val(username, "self_description")
    bot.send_message(chat_id,
                     text=f"""***Хобби:***\n{user_hobbies}\n\n***Любимые темы для разговора:***\n{user_topics}\n\n***О себе:***\n"{self_description}"\n\n***Тэг в Телеграмме:***\n@{username}""",
                     parse_mode="Markdown")


# КОСТЫЛИЩЕ
users = {}


# @bot.callback_query_handler(func=lambda call: True)
# def update_user_data(call):
    # if call.message:
    #
    #     answer = call.data
    #     username = call.message.chat.username
    #     if username not in users:
    #         users[username] = {"event_day": None, "event_time": None}
    #
    #     info_stage = get_user_tb_column_val(username, "info_stage")
    #     event_stage = get_user_tb_column_val(username, "event_stage")
    #     searching_stage = get_user_tb_column_val(username, "searching_stage")
    #     chat_id = call.message.chat.id
    #     now = datetime.datetime.now()
    #     day_options = [(now + datetime.timedelta(days=i)).strftime("%d.%m.%y") for i in range(8)]
    #
    #     if answer in config.genders:
    #         update_user_tb(username, "gender", answer)
    #         bot.send_message(chat_id, f'Гендер был изменен на "{answer}"')
    #
    #         keyboard = types.InlineKeyboardMarkup(row_width=2)
    #         buttons = [types.InlineKeyboardButton(text=age,
    #                                               callback_data=age)
    #                    for age in config.ages]
    #         keyboard.add(*buttons)
    #
    #         bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.id, reply_markup=None)
    #
    #         send = bot.send_message(chat_id, "Укажите возраст", reply_markup=keyboard)
    #         # bot.register_next_step_handler(send, get_age)
    #
    #     if answer in config.ages:
    #         update_user_tb(username, "age", answer)
    #         bot.send_message(chat_id, f'Возраст был изменен на "{answer}"')
    #         keyboard = types.InlineKeyboardMarkup(row_width=2)
    #         buttons = [types.InlineKeyboardButton(text=hobby,
    #                                               callback_data=hobby)
    #                    for hobby in config.common_hobbies]
    #         keyboard.add(*buttons)
    #
    #         bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.id, reply_markup=None)
    #
    #         send = bot.send_message(chat_id, "Укажи хобби", reply_markup=keyboard)
    #
    #         # bot.register_next_step_handler(send, get_age)
    #     if answer in config.common_hobbies:
    #         if answer != "DONE":
    #             update_user_hobbies_tb(username, config.hobbies_to_eng[answer])
    #             bot.send_message(chat_id, text=f'Добавил хобби "{answer}"')
    #             keyboard = types.InlineKeyboardMarkup(row_width=2)
    #             buttons = [types.InlineKeyboardButton(text=hobby,
    #                                                   callback_data=hobby)
    #                        for hobby in config.common_hobbies]
    #             keyboard.add(*buttons)
    #         elif answer == "DONE":
    #             bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.id, reply_markup=None)
    #             keyboard = types.InlineKeyboardMarkup(row_width=2)
    #             buttons = [types.InlineKeyboardButton(text=topic,
    #                                                   callback_data=topic)
    #                        for topic in config.common_conv_topics]
    #
    #             keyboard.add(*buttons)
    #             send = bot.send_message(chat_id, "Укажи интересные для тебя темы разговоров", reply_markup=keyboard)
    #     if answer in config.common_conv_topics:
    #         if answer != "FINISH":
    #             update_user_topics_tb(username, config.topics_to_eng[answer])
    #             bot.send_message(chat_id, text=f'Добавил тему "{answer}"')
    #         elif answer == "FINISH":

        # elif answer in config.ages and info_stage == 1:
        #     update_user_tb(username, "age", answer)
        #     bot.send_message(chat_id, text=f'Возраст был изменен на "{answer}"')
        #     get_hobbies(chat_id)
        #     update_user_tb(username, "info_stage", 2)
        #
        # elif answer in config.common_hobbies and answer != 'DONE' and info_stage in [2, 3]:
        #     eng_answer = config.hobbies_to_eng[answer]
        #     if get_interest_val(username, eng_answer, hobbies=True) == 0:
        #         update_user_hobbies_tb(username, config.hobbies_to_eng[answer])
        #         bot.send_message(chat_id, text=f'Добавил хобби "{answer}"')
        #         update_user_tb(username, "info_stage", 3)
        #
        # elif answer == 'DONE' and info_stage == 3:
        #     get_conv_topics(chat_id)
        #     update_user_tb(username, "info_stage", 4)
        #
        # elif answer in config.common_conv_topics and answer != 'FINISH' and info_stage in [4, 5]:
        #     eng_answer = config.topics_to_eng[answer]
        #     if get_interest_val(username, eng_answer, hobbies=False) == 0:
        #         update_user_topics_tb(username, config.topics_to_eng[answer])
        #         bot.send_message(chat_id, text=f'Добавил тему "{answer}"')
        #         update_user_tb(username, "info_stage", 5)
        #
        # elif answer == 'FINISH' and info_stage == 5:
        #     bot.send_message(chat_id,
        #                      text='Круто!\nНаконец, кратко опиши себя:')
        #     update_user_tb(username, "info_stage", 6)
        #
        # elif answer in day_options and searching_stage == 1:
        #     answer = str(datetime.datetime.strptime(answer, "%d.%m.%y"))[:10].replace('-', '.')
        #     users[username]["event_day"] = answer
        #     bot.send_message(chat_id, text=f'День: {answer}\nТеперь выбери время:')
        #     get_time_period(chat_id)
        #     update_user_tb(username, "searching_stage", 2)
        #
        # elif answer in config.time_periods and searching_stage == 2:
        #     users[username]["event_time"] = answer
        #     bot.send_message(chat_id, text=f'Принял! Думаю, эти варианты неплохи:')
        #     make_event_match(username, chat_id, users[username]["event_day"], users[username]["event_time"])
        #
        # elif answer in day_options and event_stage == 0:
        #     answer = str(datetime.datetime.strptime(answer, "%d.%m.%y"))[:10].replace('-', '.')
        #     update_event_tb(username, "day", answer)
        #     update_user_tb(username, "event_stage", 1)
        #     bot.send_message(chat_id, text=f'Отлично! День: {answer}\nТеперь введи время:')
        #     get_time_period(chat_id)
        #
        # elif answer in config.time_periods and event_stage == 1:
        #     update_event_tb(username, "time", answer)
        #     bot.send_message(chat_id, text=f'Начало: "{answer}"\nКратко опиши событие:')
        #     update_user_tb(username, "event_stage", 2)
        #
        # elif answer == "Удалить":
        #     update_user_tb(username, "event_stage", 0)
        #     delete_event(username)


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


# @bot.message_handler(content_types=['text'])
# def communicate(message):
#     message_text = message.text
#     username = message.from_user.username
#     info_stage = get_user_tb_column_val(username, "info_stage")
#     event_stage = get_user_tb_column_val(username, "event_stage")
#     chat_id = message.chat.id
#
#     if message_text == "Найти событие":
#         if info_stage == 7:
#             bot.send_message(chat_id, text="Опиши мне его!")
#             update_user_tb(username, "searching_stage", 1)
#             get_date(chat_id)
#         else:
#             bot.send_message(chat_id, text='Для начала расскажи о себе в ***Редактировать профиль***!',
#                              parse_mode="Markdown")
#
#     elif message_text == "Создать событие":
#         if info_stage == 7:
#             if event_stage != 3:
#                 insert_event(username)
#                 bot.send_message(chat_id, text="Опиши мне его!\nУкажи дату:")
#                 get_date(chat_id)
#             else:
#                 edit_event(username, chat_id)
#         else:
#             bot.send_message(chat_id, text='Для начала расскажи о себе в ***Редактировать профиль***!',
#                              parse_mode="Markdown")
#
#
#     elif message_text == "Найти похожих юзеров":
#         if info_stage == 7:
#             make_user_match(username, chat_id)
#         else:
#             bot.send_message(chat_id, text='Для начала расскажи о себе в ***Редактировать профиль***!',
#                              parse_mode="Markdown")
#
#     elif message_text == 'Редактировать профиль':
#         # clear old info
#         reset_info(username)
#         # start to getting data from user
#         bot.send_message(chat_id, "Давай начнем!")
#         get_gender(chat_id)
#
#     # now we are getting a self-description. otherwise we shall ignore a user
#     elif info_stage == 6 and message_text:
#         update_user_tb(username, "self_description", message_text)
#         bot.send_message(chat_id,
#                          text=f'Твое описание:\n"{message_text}"\n\n***Ты можешь ввести информацию о себе сначала в "Редактировать профиль", если захочешь изменить что-то***',
#                          parse_mode="Markdown")
#         update_user_tb(username, "info_stage", 7)
#
#     elif message_text == "Сменить видимость":
#         change_activity_status(username, chat_id)
#
#     elif message_text == "Мой профиль":
#         if info_stage == 7:
#             show_user_profile(username, chat_id)
#         else:
#             bot.send_message(chat_id,
#                              text='Пока что ты не указал о себе нужную информацию)\nМожешь сделать это в ***"Редактировать профиль"***',
#                              parse_mode="Markdown")
#
#     elif event_stage == 2 and message_text:
#         update_event_tb(username, "description", message_text)
#         bot.send_message(chat_id,
#                          text=f'Описание события:\n"{message_text}"\n\n***Ты можешь изменить или удалить его***',
#                          parse_mode="Markdown")
#         update_user_tb(username, "event_stage", 3)


bot.polling(none_stop=True)
