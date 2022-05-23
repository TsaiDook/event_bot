from mysql.connector import connect, Error

API_TOKEN = '5254469397:AAE_DNDM81MOVbFMc_sHB_4EH_qqUbXbIko'

# def connect_to_users_table():
connection = connect(
    host="localhost",
    user="root",
    password="Password",
    database="coffee_bot")


# )

def get_user_feature_val(name, feature):
    try:
        cursor = connection.cursor()
        sql = f"""
        SELECT {feature}
        FROM users
        WHERE username = '{name}'
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        return res[0][0]
    except Error as e:
        print(e)


def insert_user(age=None, gender=None, username=None, self_description=None,
                is_active=True):
    try:
        cursor = connection.cursor()
        add_user = f"""
        INSERT INTO users (age, gender, username, self_description, is_active)
         VALUES (%s, %s, %s,%s,%s)"""
        val = (age, gender, username, self_description, is_active)
        cursor.execute(add_user, val)
        connection.commit()

        cursor = connection.cursor()
        user_id = get_user_feature_val(username, "id")
        add_user_hobbies = f"""
        INSERT INTO user_hobbies (user_id, `Настольные игры`, Учеба, Искусство, Наука, `Домашние животные`, Бизнес,
         Саморазвитие, Спорт, `Компьютерные игры`)
         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        val = (user_id, False, False, False, False, False, False, False, False, False)
        cursor.execute(add_user_hobbies, val)
        connection.commit()

    except Error as e:
        print(e)


def check_existence(name):
    try:
        cursor = connection.cursor()
        query = f"""
            SELECT EXISTS(SELECT * FROM users
                          WHERE username = '{name}')
        """
        cursor.execute(query)
        res = cursor.fetchall()
        return res[0][0]
    except Error as e:
        print(e)


def update_user(name, feature, new_value):
    try:
        cursor = connection.cursor()
        sql = f"""
            UPDATE users
            SET {feature} = '{new_value}'
            WHERE username = '{name}'
            """
        cursor.execute(sql)
        connection.commit()
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
                AND self_description > '' 
                AND is_active = 1
                """
        cursor.execute(sql)
        user_info = cursor.fetchall()
        return True if user_info else False
    except Error as e:
        print(e)


def show_users():
    try:
        cursor = connection.cursor()
        create_table = f"""CREATE TABLE users(
        id INT AUTO_INCREMENT PRIMARY KEY,
        age VARCHAR(7),
        gender VARCHAR(7),
        username VARCHAR(32),
        self_description TEXT,
        is_active BOOl)"""
        cursor.execute(create_table)
    except Error as e:
        print(e)
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
