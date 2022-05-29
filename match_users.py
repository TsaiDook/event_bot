# According to a little experiment, vectorized matching algorithm works better
# So We use it in the final version of the project
from config import age_to_num
from users_tb_iter import get_interest, get_user_tb_column_val, get_active_users
from scipy import spatial


def extract_features(username):
    age = age_to_num[get_user_tb_column_val(username, "age")]
    lovely_hobbies, hobbies_vector = get_interest(username, 'hobbies')
    lovely_topics, topics_vector = get_interest(username, 'topics')

    return lovely_hobbies, lovely_topics, [age, *hobbies_vector, *topics_vector]


def cosine_similarity(usr1, usr2):
    return spatial.distance.cosine(usr1, usr2)


# The cold start problem -- ?
def interests_match(username, top_n=3):
    user_hobbies, user_topics, user_vector = extract_features(username)
    # Structure: username, hobbies, topics, description, similarity
    challengers = []
    other_usernames = get_active_users(username)
    for name in other_usernames:
        challenger_hobbies, challenger_topics, challenger_vector = extract_features(name)
        challenger_description = get_user_tb_column_val(name, "self_description")
        similarity = cosine_similarity(user_vector, challenger_vector)
        challengers.append(tuple([name, challenger_hobbies, challenger_topics, challenger_description, similarity]))
    challengers.sort(key=lambda x: x[4], reverse=True)
    try:
        return challengers[:top_n]
    except IndexError:
        return challengers

# match("user1")
