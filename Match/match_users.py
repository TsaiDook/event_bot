from ConstantsClass import Constants
from Database.users_tb_action import get_interest, get_user_tb_column_val, get_active_users


def count_feature_similarity(usr1, usr2, feature):
    """

    Return a similarity of 2 users for an exact feature
    :param usr1: username of the 1st user
    :type usr1: string
    :param usr2: username of the 2cd user
    :type usr2: string
    :param feature: type of feature we count similarity for (hobbies or conversation topics)
    :type feature: string

    :rtype: int
    :return: a measure of similarity of 2 users for this feature (int)

    """
    usr1_values = get_interest(usr1, feature)
    usr2_values = get_interest(usr2, feature)
    data = Constants.hobbies_to_eng.values() if feature == "hobbies" else Constants.topics_to_eng.values()
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
    """

    Return a similarity of 2 users depending on their age, hobbies and favorite conversation topics
    :param usr1:  username of the 1st user
    :type usr1: string
    :param usr2:  username of the 2cd user
    :type usr2: string

    :rtype: int
    :return: a measure of similarity of 2 users depending on their age, hobbies and favorite conversation topics

    """
    same_hobbies = count_feature_similarity(usr1, usr2, 'hobbies')
    same_topics = count_feature_similarity(usr1, usr2, 'conv_topics')
    usr1_age = Constants.age_to_num[get_user_tb_column_val(usr1, 'age')]
    usr2_age = Constants.age_to_num[get_user_tb_column_val(usr2, 'age')]
    age_diff = abs(usr1_age - usr2_age) / 11
    return same_topics + same_hobbies - age_diff


def interests_match(user):
    """

    Sort users by their similarity on an exact person
    :param user:  username of the 1st user
    :type user: string

    :rtype: list
    :return: a vector of users descending by a similarity on this user
    """
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
