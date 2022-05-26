from mysql.connector import connect, Error

import config

connection = connect(
    host="localhost",
    user="root",
    password="Password",
    database="coffee_bot")


def insert_user(age=None, gender=None, username=None, hobbies=None, self_description=None, conv_topics=None,
                user_id=None, is_active=True):
    try:
        cursor = connection.cursor()
        add_user_query = f"""
        INSERT INTO users (age, gender, username, hobbies, self_description, conv_topics, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        val = (age, gender, username, hobbies, self_description, conv_topics, is_active)
        cursor.execute(add_user_query, val)

        add_hobbies_query = f"""
        INSERT INTO user_hobbies (user_id)
        VALUES (%s)
        """
        cursor.execute(add_hobbies_query, [user_id])

        add_hobbies_query = f"""
                INSERT INTO user_topics (user_id)
                VALUES (%s)
                """
        cursor.execute(add_hobbies_query, [user_id])
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


def update_hobby(user_id, hobby_type):
    print('updating hobby!')
    print(user_id, hobby_type)
    cursor = connection.cursor()
    update_query = f"""
        UPDATE user_hobbies 
        SET `{hobby_type}` = 1
        WHERE user_id = {user_id}
        """
    cursor.execute(update_query)
    connection.commit()


def update_conv_topic(user_id, topic_type):
    cursor = connection.cursor()
    update_query = f"""
        UPDATE user_topics 
        SET `{topic_type}` = 1
        WHERE user_id = {user_id}
        """
    cursor.execute(update_query)
    connection.commit()


# CODE DOUBLING!!
# I'D LIKE TO WRITE 'CONNECTION.COMMIT()' ONLY ONCE
def update_user(message, feature, new_value=None):
    name = message.from_user.username
    user_id = message.chat.id
    try:
        cursor = connection.cursor()
        if feature in config.common_hobbies:
            update_hobby(user_id, feature)
        elif feature in config.common_conv_topics:
            update_conv_topic(user_id, feature)
        else:
            update_query = f"""
                UPDATE users 
                SET {feature} = '{new_value}'
                WHERE username = '{name}'
                """
            cursor.execute(update_query)
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
                AND hobbies > '' 
                AND self_description > '' 
                AND conv_topics > '' 
                AND is_active = 1
                """
        cursor.execute(sql)
        user_info = cursor.fetchall()
        return True if user_info else False
    except Error as e:
        print(e)


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
