from mysql.connector import Error, connect

from Bot.ConstantsClass import Constants


def create_connection():
    """

    Create connection to database

    """
    database_params = Constants.database_params
    connection = connect(host=database_params["host"], user=database_params["user"],
                         password=database_params["password"],
                         database=database_params["database"])
    return connection


def insert_user(age=None, gender=None, username=None, self_description="Пусто", curr_info_stage=0, curr_event_stage=0,
                curr_searching_stage=0, is_active=True):
    """

    Insert new event in database
    :param age: user's age group
    :type: string
    :param gender: user's gender
    :type: string
    :param username: user's telegram username
    :type: string
    :param self_description: user's self-description
    :type: string
    :param curr_info_stage:
    :param curr_event_stage: a stage user has filled info about themselves
    :type: int
    :param curr_searching_stage: a stage user has filled info about an event they are looking for now
    :type: int
    :param is_active: boolean variable shows if user want other people are able to see them
    :type: bool

    """
    try:
        connection = create_connection()
        cursor = connection.cursor()
        add_user = f"""
                    INSERT INTO users (age, gender, username, self_description, info_stage, event_stage, searching_stage, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
        val = (
            age, gender, username, self_description, curr_info_stage, curr_event_stage, curr_searching_stage, is_active)
        cursor.execute(add_user, val)
        connection.commit()

        user_id = get_user_tb_column_val(username, "id")
        add_user_hobbies_row(user_id)
        add_user_topics_row(user_id)
    except Error as e:
        print(e)


def add_user_hobbies_row(user_id):
    """

    Insert new user in hobbies table
    :param user_id: user's telegram id
    :type: int
    
    """
    try:
        connection = create_connection()
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
    """

    Insert new user in conversation topics table
    :param user_id: user's telegram id
    :type: int

    """
    try:
        connection = create_connection()
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
    """

    Return an exact column's value from users table
    :param username: telegram username of an author
    :type: string
    :param column: a column, which value we went to get
    :type: string

    :rtype: string
    :return: a value of the mentioned column from users table for an exact user

    """
    try:
        connection = create_connection()
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
    """

    Return user's interests: hobbies or conversation topics depends on an 'interest' variable value
    :param username: telegram username of an author
    :type: string
    :param interest: a column, which value we want to get
    :type: string

    :rtype: list
    :return: user's hobbies or preferred conversation topics

    """
    user_id = get_user_tb_column_val(username, "id")
    try:
        tb_name = "user_hobbies" if interest == "hobbies" else "user_topics"
        connection = create_connection()
        cursor = connection.cursor()
        get_topics_query = f"""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{tb_name}'
                order by ORDINAL_POSITION
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
        interest_dict = dict(zip(columns, values))
        lovely_interests = list(map(lambda x: x[0], filter(lambda x: x[1] == 1, interest_dict.items())))
        return lovely_interests
    except Error as e:
        print(e)


def reset_info(username):
    """

    Reset info about user's hobbies and preferred conversation topics
    :param username: telegram username of a user
    :type: string

    """
    update_user_tb(username, "info_stage", 0)
    for hobby in Constants.hobbies_to_eng.values():
        update_user_hobbies_tb(username, hobby, 0)
    for topic in Constants.topics_to_eng.values():
        update_user_topics_tb(username, topic, 0)


def update_user_tb(username, feature, new_value):
    """

     Update a column in users table
     :param username: telegram username of a user
     :type: string
     :param feature: column they want to change
     :type: string
     :param new_value: new value for that column
     :type: string

     """
    try:
        connection = create_connection()
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


def update_user_hobbies_tb(username, hobby, new_val=1):
    """

    Update information about user's hobbies
    :param username: telegram username of a user
    :type: string
    :param hobby: type of hobby
    :type: string
    :type: int
    :param new_val: value to update

    """
    user_id = get_user_tb_column_val(username, "id")
    try:
        connection = create_connection()
        cursor = connection.cursor()
        sql = f"""
               UPDATE user_hobbies
               SET {hobby} = {new_val}
               WHERE user_id = {user_id}
               """
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        print(e)


def update_user_topics_tb(username, topic, new_val=1):
    """

    Update information about user's preferred conversation topics
    :param username: telegram username of a user
    :type: string
    :param topic: type of conversation topic
    :type: string
    :type: int
    :param new_val: value to update

    """
    user_id = get_user_tb_column_val(username, "id")
    try:
        connection = create_connection()
        cursor = connection.cursor()
        sql = f"""
               UPDATE user_topics
               SET {topic} = {new_val}
               WHERE user_id = {user_id}
               """
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        print(e)


def check_existence(username):
    """

    Return information if an exact user exists in users table
    :param username: telegram username of a user
    :type: string

    :rtype: bool
    :return: True if user with such username exists, otherwise return False

    """
    try:
        connection = create_connection()
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


def get_interest_val(username, column, hobbies=True):
    """

    Return if an exact user has an exact interest (hobby or preferred conversation topic)
    :param username: telegram username of a user
    :type: string
    :param column: interest type
    :type: string
    :param hobbies: variable, which shows if we should check hobbies or preferred conversation topics
    :type: string

    :rtype: bool
    :return: True if user with such username has such interest, otherwise return False

    """
    try:
        connection = create_connection()
        cursor = connection.cursor()
        user_id = get_user_tb_column_val(username, "id")
        table = "user_hobbies" if hobbies else "user_topics"
        query = f"""
                 SELECT {column} FROM {table}
                 WHERE user_id = {user_id}
                 """
        cursor.execute(query)
        res = cursor.fetchall()
        return res[0][0]
    except Error as e:
        print(e)


def get_active_users(username):
    """

    Return all active users' usernames, which do not equal to an exact username
    :param username: telegram username of a user we should ignore
    :type: string

    :rtype: list
    :return: list of all active users ('is_active' = 1) with a different username

    """
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = f"""
                 SELECT username FROM users 
                 WHERE is_active = 1 AND username != '{username}'
                 """
        cursor.execute(query)
        res = cursor.fetchall()
        res = list(map(lambda x: x[0], res))
        return res
    except Error as e:
        print(e)
