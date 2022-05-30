import config
from users_tb_action import insert_user, update_user_topics_tb, update_user_hobbies_tb
import random

random.seed(12345)


def generate_random_user():
    user_age = random.choice(config.ages)
    n_hobbies = random.randint(1, len(config.hobbies_to_eng) - 1)
    user_hobbies = []
    while len(user_hobbies) < n_hobbies:
        hobby = random.choice(list(config.hobbies_to_eng.values()))
        if hobby not in user_hobbies:
            user_hobbies.append(hobby)
    n_topics = random.randint(1, len(config.topics_to_eng) - 1)
    user_conv_topics = []
    while len(user_conv_topics) < n_topics:
        topic = random.choice(list(config.topics_to_eng.values()))
        if topic not in user_conv_topics:
            user_conv_topics.append(topic)

    return {'age': user_age, 'username': None, 'conv_topics': user_conv_topics,
            'hobbies': user_hobbies, 'is_active': 1}


for i in range(200):
    user = generate_random_user()
    user['username'] = f"user{i}"
    user['stage'] = 7
    user['gender'] = random.choice(config.genders)
    # Which event_stage is correct?
    user['info_stage'] = 6
    user['event_stage'] = 6

    insert_user(age=user['age'], gender=user['gender'], username=user['username'], curr_info_stage=user['info_stage'],
                is_searching_event=False, curr_event_stage=user['event_stage'])
    for hobby in user['hobbies']:
        update_user_hobbies_tb(user['username'], hobby)

    for topic in user['conv_topics']:
        update_user_topics_tb(user['username'], topic)
