from config import ages, age_to_num, common_conv_topics, common_hobbies
from scipy import spatial
import random
from sklearn.metrics import ndcg_score

random.seed(42)


# let's make 12 random users. 4 people per 3 cases:
def generate_random_user():
    user_age = random.choice(ages)
    n_hobbies = random.randint(1, len(common_hobbies))
    user_hobbies = []
    while len(user_hobbies) < n_hobbies:
        hobby = random.choice(common_hobbies)
        if hobby not in user_hobbies:
            user_hobbies.append(hobby)
    n_topics = random.randint(1, len(common_conv_topics))
    user_conv_topics = []
    while len(user_conv_topics) < n_topics:
        topic = random.choice(common_conv_topics)
        if topic not in user_conv_topics:
            user_conv_topics.append(topic)

    return {'age': user_age, 'username': None, 'conv_topics': user_conv_topics,
            'hobbies': user_hobbies, 'is_active': 1}


users = []
for num in range(12):
    random_user = generate_random_user()
    random_user['username'] = f'user{num + 1}'
    users.append(random_user)


def count_feature_similarity(usr1: dict, usr2: dict, feature: str) -> int:
    if feature in ['hobbies', 'conv_topics'] and usr1['is_active'] and usr2['is_active']:
        data = common_hobbies if feature == 'hobbies' else common_conv_topics
        same_hobbies = 0
        for sample in data:
            if sample in usr1[feature] and sample in usr2[feature]:
                same_hobbies += 1
            elif sample not in usr1[feature] and not usr2[feature]:
                same_hobbies += 0.1
            else:
                same_hobbies -= 0.2
        return same_hobbies


def sum_user_similarity(usr1: dict, usr2: dict) -> int:
    same_hobbies = count_feature_similarity(usr1, usr2, 'hobbies')
    same_topics = count_feature_similarity(usr1, usr2, 'conv_topics')
    # 11 -- max age diff
    age_diff = abs(age_to_num[usr1['age']] - age_to_num[usr2['age']]) / 11
    return same_topics + same_hobbies - age_diff


# make return top n massiv
def sum_matching(user: dict, group: list) -> None:
    similarities = [(other_user['username'], sum_user_similarity(user, other_user)) for other_user in group if
                    other_user['username'] != user['username']]
    similarities.sort(key=lambda x: x[1], reverse=True)
    ranged_users = []
    for person in similarities:
        ranged_users.append(int(person[0][4:]))
    return ranged_users


def make_vector(user: dict, feature: str) -> list:
    if feature in ['hobbies', 'conv_topics']:
        data = common_hobbies if feature == 'hobbies' else common_conv_topics
        feature_vector = []
        for sample in data:
            if sample in user[feature]:
                feature_vector.append(1)
            else:
                feature_vector.append(0)
        return feature_vector


def cosine_similarity(usr1: dict, usr2: dict) -> int:
    usr1_vector = [age_to_num[usr1['age']], *make_vector(usr1, 'hobbies'), *make_vector(usr1, 'conv_topics')]
    usr2_vector = [age_to_num[usr2['age']], *make_vector(usr2, 'hobbies'), *make_vector(usr2, 'conv_topics')]
    return spatial.distance.cosine(usr1_vector, usr2_vector)


# make return top n array
def vector_matching(user: dict, group: list) -> None:
    similarities = [(other_user['username'], cosine_similarity(user, other_user)) for other_user in group if
                    other_user['username'] != user['username']]
    similarities.sort(key=lambda x: x[1])
    ranged_users = []
    for person in similarities:
        ranged_users.append(int(person[0][4:]))
    return ranged_users



groups = [users[:4], users[4:8], users[8:]]

human_right = [[2, 4, 3], [7, 8, 6], [12, 11, 10]]

results = []

sum_results = 0
vector_results = 0

for num, group in enumerate(groups):
    sum_matching_res = sum_matching(group[0], group)
    vector_matching_res = vector_matching(group[0], group)

    sum_results += ndcg_score([sum_matching_res], [human_right[num]], k=3)
    vector_results += ndcg_score([vector_matching_res], [human_right[num]], k=3)

    print(human_right[num], sum_matching_res, vector_matching_res)

    print(f"1. Sum matching result: {ndcg_score([sum_matching_res], [human_right[num]], k=3)}")
    print(f"2. Vector matching result: {ndcg_score([vector_matching_res], [human_right[num]])}")

print(f"Sum algorithm mean NDCG score: {sum_results / 3}")
print(f"Vector algorithm mean NDCG score: {vector_results / 3}")
