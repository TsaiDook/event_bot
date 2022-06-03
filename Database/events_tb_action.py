import datetime

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


def insert_event(creator_username, day=None, time=None, event_description="Пусто"):
    """

    Insert new event in a database
    :param creator_username: telegram username of an author
    :type: string
    :param day: day, which user suggests
    :type: timestamp
    :param time: time period, which user suggests
    :type: string
    :param event_description: little description of an event
    :type: string

    """
    try:
        connection = create_connection()
        cursor = connection.cursor()
        add_event = f"""
                    INSERT INTO events (creator, day, time, description)
                    VALUES (%s, %s, %s, %s)
                    """
        val = (creator_username, day, time, event_description)
        cursor.execute(add_event, val)
        connection.commit()
    except Error as e:
        print(e)


def update_event_tb(creator_username, feature, new_value):
    """

    Update a column in events table
    :param creator_username: telegram username of an author
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
              UPDATE events
              SET {feature} = '{new_value}'
              WHERE creator = '{creator_username}'
              """
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        print(e)


def delete_event(creator_username):
    """

    Delete an event from events table
    :param creator_username: telegram username of an author
    :type: string

    """
    try:
        connection = create_connection()
        cursor = connection.cursor()
        sql = f""" 
               DELETE FROM events 
               WHERE creator = '{creator_username}'
               """
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        print(e)


def get_all_events_by_day(day, creator_username):
    """

    Return all events on an exact day from events table
    :param day: a day we want to get event on
    :type: string
    :param creator_username: telegram username of an author
    :type: string

    :return: list of events on that day
    :type: list

    """
    try:
        connection = create_connection()
        cursor = connection.cursor()
        sql = f"""
              SELECT * FROM events 
              WHERE day = '{day}' and creator != '{creator_username}'
              """
        cursor.execute(sql)
        data = cursor.fetchall()
        data = list(map(lambda x: tuple([x[1], x[3], x[4]]), data))
        return data
    except Error as e:
        print(e)


def get_event_tb_column_val(username, column):
    """

    Return an exact column's value from user's created event
    :param username: telegram username of an author
    :type: string
    :param column: a column, which value we went to get
    :type: string

    :return: a value of the mentioned column from events table
    :rtype: string

    """
    try:
        connection = create_connection()
        cursor = connection.cursor()
        sql = f"""
               SELECT {column}
               FROM events
               WHERE creator = '{username}'
               """
        cursor.execute(sql)
        res = cursor.fetchall()
        return res[0][0]
    except Error as e:
        print(e)


def get_event_by_creator(username):
    """

    Return an information about event by author telegram username
    :param username: telegram username of an author
    :type: string

    :return: information about event or False if such event does not exist now
    :rtype: list or bool

    """
    try:
        connection = create_connection()
        cursor = connection.cursor()
        sql = f"""SELECT * FROM events WHERE creator = '{username}'"""
        cursor.execute(sql)
        res = cursor.fetchall()
        return res[0] if res else False
    except Error as e:
        print(e)


def find_old_events():
    """

    Return all events, which beginning time is outdated now
    :return: list of authors' usernames of outdated events
    :rtype: list
    """
    try:
        connection = create_connection()
        cursor = connection.cursor()
        now = datetime.datetime.now()
        curr_date = str(datetime.date(year=now.year, month=now.month, day=now.day))
        curr_time = str(datetime.time(hour=now.hour))

        query = f"""SELECT creator FROM events
                 WHERE (day < '{curr_date}') OR (day = '{curr_date}' AND LEFT(RIGHT(time, 5), 2) < '{curr_time}');
                 """

        cursor.execute(query)
        users_to_notify = cursor.fetchall()
        return users_to_notify
    except Error as e:
        print(e)
