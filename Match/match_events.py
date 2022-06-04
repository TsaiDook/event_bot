from Database.events_tb_action import get_all_events_by_day
from Match.match_users import sum_user_similarity
from ConstantsClass import Constants


def count_events_similarity(user1, time1, user2, time2):
    """

    Count similarity of 2 events
    :param user1: username of the 1st user
    :type: string
    :param time1: period of time for a meeting 1st user suggests
    :type: string
    :param user2: username of the 2cd user
    :type: string
    :param time2: period of time for a meeting 2cs user suggests
    :type: string

    :return: a similarity of 2 events
    :rtype: int

    """
    users_similarity = sum_user_similarity(user1, user2)
    time_periods_to_num = Constants.time_periods_to_num
    if users_similarity > 0:
        events_similarity = users_similarity / (abs(time_periods_to_num[time1] - time_periods_to_num[time2]) + 1)**2
    else:
        events_similarity = users_similarity * (abs(time_periods_to_num[time1] - time_periods_to_num[time2]) + 1)**2
    return events_similarity


def event_match(username, event_day, event_time):
    """

    Sort users by their similarity on an exact person
    :param username: username of the user who is finding an event
    :type: string
    :param event_day: day user suggests
    :type: timestamp
    :param event_time: time period user suggests
    :type: string

    :rtype: list
    :return: a vector of events descending by a similarity on the event user suggests
    """
    potential_events = get_all_events_by_day(event_day, username)

    best_events = []
    for potential_event in potential_events:
        creator_name = potential_event[0]
        time_suggestion = potential_event[1]
        similarity = count_events_similarity(username, event_time, creator_name, time_suggestion)
        best_events.append(tuple([*potential_event, similarity]))
    best_events.sort(key=lambda x: x[3], reverse=True)

    return best_events
