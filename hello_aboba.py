import telebot
from telebot import types
from mysql.connector import connect, Error

API_TOKEN = '5254469397:AAE_DNDM81MOVbFMc_sHB_4EH_qqUbXbIko'


def connect_to_users_table():
    connection = connect(
        host="localhost",
        user="root",
        password="Password",
        database="coffee_bot"
    )
    return connection


def insert_user(age=None, gender=None, username=None, hobbies=None, self_description=None, conv_topics=None,
                is_active=True):
    try:
        connection = connect_to_users_table()
        # create_db = "CREATE DATABASE coffee_bot"
        create_table = "CREATE TABLE users(id INT AUTO_INCREMENT PRIMARY KEY, age INT, gender VARCHAR(7), username VARCHAR(32), hobbies VARCHAR(50), self_description TEXT, conv_topics VARCHAR(30), is_active BOOl)"
        cursor = connection.cursor()
        sql = "INSERT INTO users (age, gender, username, hobbies, self_description, conv_topics, is_active) VALUES (%s, %s, %s,%s,%s,%s,%s)"
        val = tuple([age, gender, username, hobbies, self_description, conv_topics, is_active])
        cursor.execute(sql, val)
        connection.commit()


        show_table = "SELECT * FROM users"
        cursor.execute(show_table)
        for row in cursor.fetchall():
            print(row)

    except Error as e:
        print(e)


# bot = telebot.TeleBot(API_TOKEN)

insert_user()
# def send_welcome(message):
#     print(f"Hello {message}")
#
#
# bot.infinity_polling()
