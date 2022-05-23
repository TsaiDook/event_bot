from mysql.connector import connect, Error

API_TOKEN = '5254469397:AAE_DNDM81MOVbFMc_sHB_4EH_qqUbXbIko'

# def connect_to_users_table():
connection = connect(
    host="localhost",
    user="root",
    password="Password",
    database="coffee_bot")
# )


def insert_user(age=None, gender=None, username=None, self_description="Пусто",
                is_active=True):
    user_id = get_user_tb_column_val(username, "id")
    try:
        cursor = connection.cursor()
        add_user = f"""
        INSERT INTO users (age, gender, username, self_description, is_active)
         VALUES (%s, %s, %s,%s,%s)"""
        val = (age, gender, username, self_description, is_active)
        cursor.execute(add_user, val)
        connection.commit()

        add_user_hobbies_row(user_id)
        add_user_topics_row(user_id)
    except Error as e:
        print(e)


def add_user_hobbies_row(user_id):
    try:
        cursor = connection.cursor()
        add_user_hobbies = f"""
                INSERT INTO user_hobbies (user_id, `Настольные игры`, Учеба, Искусство, Наука, `Домашние животные`, 
                Бизнес, Саморазвитие, Спорт, `Компьютерные игры`)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        val = (user_id, False, False, False, False, False, False, False, False, False)
        cursor.execute(add_user_hobbies, val)
        connection.commit()
    except Error as e:
        print(e)


def add_user_topics_row(user_id):
    try:
        cursor = connection.cursor()
        add_user_hobbies = f"""
                INSERT INTO user_topics (user_id, Мысли, Учеба, Искусство, `Жизненные истории`, Работа, Бизнес,
                Переживания, Спорт, Путешествия, Юмор, Будущее)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)"""
        val = (user_id, False, False, False, False, False, False, False, False, False, False, False)
        cursor.execute(add_user_hobbies, val)
        connection.commit()
    except Error as e:
        print(e)


def get_user_tb_column_val(username, column):
    try:
        cursor = connection.cursor()
        sql = f"""
        SELECT {column}
        FROM users
        WHERE username = '{username}'
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        return res[0][0]
    except Error as e:
        print(e)


def get_user_hobbies(username):
    user_id = get_user_tb_column_val(username, "id")
    try:
        cursor = connection.cursor()
        sql = f"""
                SELECT *
                FROM user_hobbies
                WHERE id = '{user_id}'
                """
        cursor.execute(sql)
        res = cursor.fetchall()
        return res[0]
    except Error as e:
        print(e)


def get_user_topics(username):
    user_id = get_user_tb_column_val(username, "id")
    try:
        cursor = connection.cursor()
        sql = f"""
                SELECT *
                FROM user_topics
                WHERE id = '{user_id}'
                """
        cursor.execute(sql)
        res = cursor.fetchall()
        return res[0]
    except Error as e:
        print(e)


def update_user_tb(username, feature, new_value):
    try:
        cursor = connection.cursor()
        sql = f"""
            UPDATE users
            SET {feature} = '{new_value}'
            WHERE username = '{username}'
            """
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        print(e)


def update_user_hobbies_tb(username, hobby):
    user_id = get_user_tb_column_val(username, "id")
    try:
        cursor = connection.cursor()
        sql = f"""
               UPDATE user_hobbies
               SET {hobby} = 1
               WHERE user_id = '{user_id}'
               """
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        print(e)


def update_user_topics_tb(username, topic):
    user_id = get_user_tb_column_val(username, "id")
    try:
        cursor = connection.cursor()
        sql = f"""
               UPDATE user_topics
               SET {topic} = 1
               WHERE user_id = '{user_id}'
               """
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        print(e)


def check_existence(username):
    try:
        cursor = connection.cursor()
        query = f"""
            SELECT EXISTS(SELECT * FROM users
                          WHERE username = '{username}')
        """
        cursor.execute(query)
        res = cursor.fetchall()
        return True if res[0][0] else False
    except Error as e:
        print(e)


def is_user_info_filled(name):
    try:
        cursor = connection.cursor()
        sql = f"""
                SELECT *
                FROM users
                WHERE username = '{name}' 
                AND age > ''
                AND gender > '' 
                AND is_active = 1
                """
        cursor.execute(sql)
        user_info = cursor.fetchall()
        return True if user_info else False
    except Error as e:
        print(e)

# def show_users():
#     try:
#         cursor = connection.cursor()
#         create_table = f"""CREATE TABLE user_topics(
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         user_id INT,
#         Мысли BOOL,
#         Учеба BOOL,
#         Искусство BOOL,
#         `Жизненные истории` BOOL,
#         Бизнес BOOL,
#         Работа BOOL,
#         Спорт BOOL,
#         Переживания BOOL,
#         Путешествия BOOL,
#         Юмор BOOL,
#         Будущее BOOL)"""
#         cursor.execute(create_table)
#     except Error as e:
#         print(e)
# for row in cursor.fetchall():
#     print(row)

# bot = telebot.TeleBot(API_TOKEN)
# insert_user(username="aca", conv_topics=("123, 1234"))
# print(is_user_info_filled("Alex"))
# update_user("slashenaya_nechist","conv_topics", "123")
# print(is_user_info_filled("slashenaya_nechist"))
#
# show_users()
# def send_welcome(message):
#     print(f"Hello {message}")
#
#
# bot.infinity_polling()
