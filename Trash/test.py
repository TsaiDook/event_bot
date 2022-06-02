class User:
    def __init__(self, id):
        self.id = id
        self.event_stage = 0
        self.search_stage = 0

class Users:
    def __init__(self):
        self.users = {}

    def add_user(self, user: User):
        self.users[user.id] = user

    def show_dict(self):
        for id in self.users:
            print(id, self.users[id])
