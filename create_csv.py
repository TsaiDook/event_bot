import pandas as pd

# базовые версии
users_columns = ['age', 'gender', 'username', 'hobbies', 'about_me', 'conv_topics', 'is_active']
users = pd.DataFrame(columns=users_columns)
users.to_csv('users.csv')

events_columns = ['author_id', 'day', 'month', 'year', 'time']
events = pd.DataFrame(columns=events_columns)
events.to_csv('events.csv')
