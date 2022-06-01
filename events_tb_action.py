from mysql.connector import connect, Error

connection = connect(
    host="localhost",
    user="root",
    password="Password",
    database="coffee_bot")


def insert_event(creator_username, day=None, time=None, event_description="Пусто"):
    try:
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
        sql = f""" 
               DELETE FROM events 
               WHERE creator = '{creator_username}'
               """
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        print(e)


def get_all_events_by_day(day, creator_username):
    try:
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
    try:
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
    try:
        cursor = connection.cursor()
        sql = f"""SELECT * FROM events WHERE creator = '{username}'"""
        cursor.execute(sql)
        res = cursor.fetchall()
        return res[0] if res else False
    except Error as e:
        print(e)