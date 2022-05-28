import config
from match_users_experiments import generate_random_user
from users_tb_iter import insert_user, update_user_topics_tb, update_user_hobbies_tb
import random

users = []

for i in range(200):
    user = generate_random_user()
    user['username'] = f"user{i}"
    user['stage'] = 6
    user['gender'] = random.choice(config.genders)

    insert_user(age=user['age'], gender=user['gender'], username=user['username'], curr_stage=user['stage'])
    for hobby in user['hobbies']:
        update_user_hobbies_tb(user['username'], hobby)

    for topic in user['conv_topics']:
        update_user_topics_tb(user['username'], topic)
