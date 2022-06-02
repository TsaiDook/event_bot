class User:
    """

    A special class storing specific dynamic user attributes, which is not supposed to be stored in a database

    """

    def __init__(self, user_id, username):
        self._id = user_id
        self.name = username
        self.match_users_row = 0
        self.match_events_row = 0
        self.event_day = None
        self.event_time = None


class Users:
    """

    A parent class, which stores objects of class User

    """
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        """

        Add user in a special storage
        :param user: username of a user we add in a storage
        :type: string

        """
        self.users[user._id] = user

    def get_user(self, user_id):
        """

        Return on object of class User by its telegram id
        :param user_id: user's telegram id
        :type: int

        :return: object of class User, which has such id
        :rtype: User

        """
        return self.users[user_id]
