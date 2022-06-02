# useless?

from mysql.connector import connect

from ConstantsClass import Constants

database_params = Constants.database_params


def create_connection():
    connection = connect(host=database_params["host"], user=database_params["user"],
                         password=database_params["password"],
                         database=database_params["database"])
    return connection
