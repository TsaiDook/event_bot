from events_tb_action import get_all_events_by_day, get_event_tb_column_val
from match_users import cosine_similarity, extract_features
from config import time_periods_to_num


def count_events_similarity(user1, time1, user2, time2):
    user1_vec = extract_features(user1)[2]
    user2_vec = extract_features(user2)[2]
    users_similarity = cosine_similarity(user1_vec, user2_vec)
    events_similarity = users_similarity / (abs(time_periods_to_num[time1] - time_periods_to_num[time2]) + 1)
    return events_similarity


def event_match(username, event_day, event_time, top_n=3):
    potential_events = get_all_events_by_day(event_day)

    best_events = []
    for potential_event in potential_events:
        creator_name = potential_event[0]
        time_suggestion = potential_event[1]
        similarity = count_events_similarity(username, event_time, creator_name, time_suggestion)
        best_events.append(tuple([*potential_event, similarity]))
    best_events.sort(key=lambda x: x[3], reverse=True)

    if len(best_events) >= top_n:
        return best_events[:top_n]

    return best_events
