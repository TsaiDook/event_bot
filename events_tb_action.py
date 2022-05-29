from mysql.connector import connect, Error

connection = connect(
    host="localhost",
    user="root",
    password="Password",
    database="coffee_bot")


def insert_event(creator_username, day, time, participant_username=None, event_description="Пусто"):
    try:
        cursor = connection.cursor()
        add_event = f"""
                    INSERT INTO events (creator, day, time, description)
                    VALUES (%s, %s, %s, %s)
                    """
        val = (creator_username, participant_username, day, time, event_description)
        cursor.execute(add_event, val)
        connection.commit()
    except Error as e:
        print(e)


def update_event_tb(creator_username, feature, new_value):
    try:
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
    try:
        cursor = connection.cursor()
        sql = f""" DELETE FROM events WHERE creator = {creator_username}"""
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        print(e)


def get_all_events_by_day(day):
    try:
        cursor = connection.cursor()
        sql = f"""
        SELECT * FROM events where day = '{day}'
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Error as e:
        print(e)
