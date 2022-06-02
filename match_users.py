# According to a little experiment, summarizing matching algorithm works better
# So We use it in the final version of the project
import config
from users_tb_action import get_interest, get_user_tb_column_val, get_active_users


def count_feature_similarity(usr1, usr2, feature) -> int:
    usr1_values = get_interest(usr1, feature)
    usr2_values = get_interest(usr2, feature)
    data = config.hobbies_to_eng.values() if feature == "hobbies" else config.topics_to_eng.values()
    summa = 0
    for sample in data:
        if sample in usr1_values and sample in usr2_values:
            summa += 1
        elif sample not in usr1_values and not usr2_values:
            summa += 0.1
        else:
            summa -= 0.2
    return summa


def sum_user_similarity(usr1, usr2):
    same_hobbies = count_feature_similarity(usr1, usr2, 'hobbies')
    same_topics = count_feature_similarity(usr1, usr2, 'conv_topics')
    usr1_age = config.age_to_num[get_user_tb_column_val(usr1, 'age')]
    usr2_age = config.age_to_num[get_user_tb_column_val(usr2, 'age')]
    # 11 -- max age diff
    age_diff = abs(usr1_age - usr2_age) / 11
    return same_topics + same_hobbies - age_diff


# make return top n massiv
def interests_match(user):
    # Structure: similarity, username
    other_usernames = get_active_users(user)
    challengers = []
    for challenger in other_usernames:
        try:
            similarity = sum_user_similarity(user, challenger)
            challengers.append(tuple([similarity, challenger]))
        except KeyError as e:
            print(e)

    challengers.sort(key=lambda x: x[0], reverse=True)
    return challengers
