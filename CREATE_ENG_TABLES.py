USERS = """CREATE TABLE users(
id INT AUTO_INCREMENT PRIMARY KEY,
age VARCHAR(7),
gender VARCHAR(7),
username VARCHAR(32),
self_description TEXT,
info_stage INT,
event_stage INT,
is_active BOOl)"""

HOBBIES = """CREATE TABLE user_hobbies(
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
Table_games BOOL,
Education BOOL,
Art BOOL,
Science BOOL,
Pets BOOL,
Busyness BOOL,
Improving BOOL,
Sport BOOL,
Blogging BOOL,
Computer_games BOOL)"""

TOPICS = """CREATE TABLE user_topics(
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
Thoughts BOOL,
Education BOOL,
Art BOOL,
Experiences BOOL,
Busyness BOOL,
Work BOOL,
Sport BOOL,
Anxiety BOOL,
Travels BOOL,
Politics BOOL,
Humour BOOL,
Future BOOL)"""

EVENTS = """CREATE TABLE events(
id INT AUTO_INCREMENT PRIMARY KEY,
creator VARCHAR(32),
participant VARCHAR(32),
day TIMESTAMP,
time VARCHAR(11),
description TEXT)"""
