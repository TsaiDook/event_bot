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
    try:
        cursor = connection.cursor()
        add_user = f"""
        INSERT INTO users (age, gender, username, self_description, is_active)
         VALUES (%s, %s, %s,%s,%s)"""
        val = (age, gender, username, self_description, is_active)
        cursor.execute(add_user, val)
        connection.commit()

        user_id = get_user_tb_column_val(username, "id")
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


###
def get_interest(username, interest):
    user_id = get_user_tb_column_val(username, "id")
    try:
        tb_name = ""
        if interest == "hobbies":
            tb_name = "user_hobbies"
        elif interest == "topics":
            tb_name = "user_topics"

        cursor = connection.cursor()
        get_topics_query = f"""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{tb_name}'
            """
        cursor.execute(get_topics_query)
        columns = tuple(i[0] for i in cursor.fetchall()[2:])

        cursor = connection.cursor()
        get_topics_values_query = f"""
                    SELECT *
                    FROM {tb_name}
                    WHERE user_id = '{user_id}'
                    """
        cursor.execute(get_topics_values_query)
        values = cursor.fetchall()[0][2:]
        return dict(zip(columns, values))
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
    print(username, hobby)
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


def is_not_empty_match_info(username):
    try:
        cursor = connection.cursor()
        sql = f"""
                SELECT *
                FROM users
                WHERE username = '{username}' 
                AND age > ''
                AND gender > '' 
                AND is_active = 1
                """
        cursor.execute(sql)
        user_info = cursor.fetchall()
        is_almost_one_hobby = False
        is_almost_one_topic = False
        for i in get_interest(username, "hobbies").values():
            if i:
                is_almost_one_hobby = True
                break
        for i in get_interest(username, "topics").values():
            if i:
                is_almost_one_topic = True
                break
        return True if (user_info and is_almost_one_hobby and is_almost_one_topic) else False
    except Error as e:
        print(e)


# update_user_hobbies_tb("slashenaya_nechist", "Учеба")
# def show_columns():
#     try:
#         cursor = connection.cursor()
#         create_table = f"""
#         SELECT COLUMN_NAME
#         FROM INFORMATION_SCHEMA.COLUMNS
#         WHERE TABLE_NAME = 'user_topics'
#         """
#         cursor.execute(create_table)
#         res = cursor.fetchall()
#         print(res)
#     except Error as e:
#         print(e)


# for row in cursor.fetchall():
# print(get_interest("slashenaya_nechist", "hobbies"))
# bot = telebot.TeleBot(API_TOKEN)
# insert_user(username="aca", conv_topics=("123, 1234"))
# print(is_user_info_filled("Alex"))
# update_user("slashenaya_nechist","conv_topics", "123")
# print(is_user_info_filled("slashenaya_nechist"))
#
# show_columns()
# def send_welcome(message):
#     print(f"Hello {message}")
#
#
# bot.infinity_polling()