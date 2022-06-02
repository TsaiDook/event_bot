from events_tb_action import get_all_events_by_day, get_event_tb_column_val
from match_users import sum_user_similarity
from config import time_periods_to_num


def count_events_similarity(user1, time1, user2, time2):
    users_similarity = sum_user_similarity(user1, user2)
    if users_similarity > 0:
        events_similarity = users_similarity / (abs(time_periods_to_num[time1] - time_periods_to_num[time2]) + 1)**2
    else:
        events_similarity = users_similarity * (abs(time_periods_to_num[time1] - time_periods_to_num[time2]) + 1)**2
    return events_similarity


def event_match(username, event_day, event_time):
    potential_events = get_all_events_by_day(event_day, username)

    best_events = []
    for potential_event in potential_events:
        creator_name = potential_event[0]
        time_suggestion = potential_event[1]
        similarity = count_events_similarity(username, event_time, creator_name, time_suggestion)
        best_events.append(tuple([*potential_event, similarity]))
    best_events.sort(key=lambda x: x[3], reverse=True)

    return best_events
