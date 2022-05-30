import random
import datetime
from events_tb_action import insert_event

import config

for i in range(200):
    author = f"user{i}"
    delta = random.randint(1, 8)
    date = (datetime.datetime.now() + datetime.timedelta(days=delta)).strftime("%y.%m.%d")
    time = random.choice(config.time_periods)
    description = "Пусто"
    insert_event(author, date, time, description)
