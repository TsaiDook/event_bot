class User:
    def __init__(self, user_id, username):
        self._id = user_id
        self.name = username
        self.match_users_row = 0
        self.match_events_row = 0
        self.event_day = None
        self.event_time = None


class Users:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user._id] = user

    def get_user(self, user_id):
        return self.users[user_id]