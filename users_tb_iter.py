from mysql.connector import connect, Error

API_TOKEN = '5254469397:AAE_DNDM81MOVbFMc_sHB_4EH_qqUbXbIko'

connection = connect(
    host="localhost",
    user="root",
    password="Password",
    database="coffee_bot")


def insert_user(age=None, gender=None, username=None, self_description="Пусто", curr_stage=0,
                is_active=True):
    try:
        cursor = connection.cursor()
        add_user = f"""
                    INSERT INTO users (age, gender, username, self_description, stage, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
        val = (age, gender, username, self_description, curr_stage, is_active)
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
                            INSERT INTO user_hobbies (user_id, Table_games, Education, Art, Science, Pets,
                                                      Busyness, Improving, Sport, Computer_games, Blogging)
                                                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
        val = (user_id, False, False, False, False, False, False, False, False, False, False)
        cursor.execute(add_user_hobbies, val)
        connection.commit()
    except Error as e:
        print(e)


def add_user_topics_row(user_id):
    try:
        cursor = connection.cursor()
        add_user_hobbies = f"""
                           INSERT INTO user_topics (user_id, Thoughts, Education, Art, Experiences, Work, Busyness,
                                                    Anxiety, Sport, Travels, Humour, Future, Politics)
                                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                           """
        val = (user_id, False, False, False, False, False, False, False, False, False, False, False, False)
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


def get_interest(username, interest):
    user_id = get_user_tb_column_val(username, "id")
    try:
        tb_name = "user_hobbies" if interest == "hobbies" else "user_topics"

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
                    WHERE user_id = {user_id}
                    """
        cursor.execute(get_topics_values_query)
        values = cursor.fetchall()[0][2:]
        return dict(zip(columns, values))
    except Error as e:
        print(e)


def reset_interests(username, interest):
    user_id = get_user_tb_column_val(username, "id")
    try:
        cursor = connection.cursor()
        reset_interests_query = f"""
                        UPDATE user_hobbies
                        SET Table_games = 0,
                            Education = 0,
                            Art = 0,
                            Science = 0,
                            Pets = 0,
                            Busyness = 0,
                            Improving = 0,
                            Sport = 0,
                            Blogging = 0,
                            Computer_games = 0
                        WHERE user_id = '{user_id}'
                        """ if interest == "hobbies" else f"""
                        UPDATE user_topics
                        SET Thoughts = 0,
                            Education = 0,
                            Art = 0,
                            Experiences = 0,
                            Busyness = 0,
                            Work = 0,
                            Sport = 0,
                            Anxiety = 0,
                            Travels = 0,
                            Politics = 0,
                            Humour = 0,
                            Future = 0
                        WHERE user_id = '{user_id}'
                        """
        cursor.execute(reset_interests_query)
        connection.commit()
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
               WHERE user_id = {user_id}
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
               WHERE user_id = {user_id}
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
                SELECT * FROM users
                WHERE username = '{username}' 
                AND age > '' AND gender > '' AND is_active = 1
                """
        cursor.execute(sql)
        user_info = cursor.fetchall()

        is_almost_one_hobby = is_almost_one_interest(username, "hobbies")
        is_almost_one_topic = is_almost_one_interest(username, "topics")
        return True if (user_info and is_almost_one_hobby and is_almost_one_topic) else False
    except Error as e:
        print(e)


def is_almost_one_interest(username, interest):
    for i in get_interest(username, interest).values():
        if i:
            return True
    return False

print(is_not_empty_match_info("slashenaya_nechist"))
