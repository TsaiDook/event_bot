class ConstantsClass:
    def __init__(self):
        """

        A special class for storing different constants: basic messages, available time periods, most common hobbies and so on

        """
        self.token = '5333257168:AAH4yP3U7ze2IIBGfCLZmpzG93VIfu_qzys'

        self.intro_text = """
        
Я помогаю людям заводить знакомства, находить и создавать возможности для совместного досуга)
        
Сейчас тебе доступны опции:

1. "Перейти в профиль"

Создай или редактируй информацию о себе. Ты можешь скрыть себя из предложений для других юзеров, чтобы тебя не беспокоили, или снова активизировать свой аккаунт)

2. "Посмотреть события"

Создай, удали или отредактируй свое собственное предложение для других пользователей: укажи дату, ориентировочное время и описание события, а я помогу схожим по интересам людям выйти на тебя)

Не хочешь становиться автором события? Укажи дату и время, в которые ты свободен, а я выведу тебя на схожих по интересам пользователей, свободных в это время)

3. "Найти похожих пользователей"

Не уверен в своих планах? Я могу помочь тебе найти единомышленников, с которыми вы договоритесь о встрече в свободной форме в личных сообщениях)

Важно❗❗❗

Если я перестал отвечать, просто пропиши /start, чтобы пробудить меня)
        
        """

        self.common_conv_topics = ['Учеба', 'Работа', 'Искусство', 'Спорт', 'Переживания', 'Мысли',
                                   'Путешествия', 'Юмор', 'Будущее', 'Бизнес', 'Жизненные истории', 'Политика',
                                   'FINISH']

        self.topics_to_eng = {"Учеба": "Education", "Работа": "Work", "Искусство": "Art",
                              "Спорт": "Sport", "Переживания": "Anxiety", "Мысли": "Thoughts",
                              "Путешествия": "Travels", "Юмор": "Humour", "Бизнес": "Busyness",
                              "Жизненные истории": "Experiences", "Политика": "Politics", "Будущее": "Future"}

        self.common_hobbies = ['Спорт', 'Искусство', 'Учеба', 'Наука', 'Настольные игры', 'Домашние животные',
                               'Саморазвитие', 'Бизнес', 'Компьютерные игры', 'Блоггинг', 'DONE']

        self.hobbies_to_eng = {"Учеба": "Education", "Искусство": "Art", "Настольные игры": "Table_games",
                               "Домашние животные": "Pets", "Блоггинг": "Blogging",
                               "Спорт": "Sport", "Бизнес": "Busyness", "Наука": "Science", "Саморазвитие": "Improving",
                               "Компьютерные игры": "Computer_games"}

        self.ages = [
            "< 14", "14 - 17", "18 - 24",
            "25 - 30", "31 - 40", "41 - 50",
            "51 - 60", "> 60"
        ]

        self.age_to_num = {
            "< 14": 1, "14 - 17": 3, "18 - 24": 5,
            "25 - 30": 6, "31 - 40": 7, "41 - 50": 8,
            "51 - 60": 10, "> 60": 12
        }

        self.genders = [
            "М", "Ж", "Другое", "Неважно"
        ]

        self.time_periods = [
            "До 10:00", "10:00 - 12:00", "12:00 - 14:00", "14:00 - 16:00",
            "16:00 - 18:00", "18:00 - 21:00", "21:00 - 23:00"
        ]

        self.time_periods_to_num = {
            "До 10:00": 1, "10:00 - 12:00": 2, "12:00 - 14:00": 3,
            "14:00 - 16:00": 4, "16:00 - 18:00": 5, "18:00 - 21:00": 6, "21:00 - 23:00": 7
        }

        self.start = 0
        self.top_n = 3

        self.delete_notification = \
            """Добрый день, {}! Созданное вами событие было автоматически удалено, так как оно уже не актуально по времени)
            Вы можете создать новое уже сегодня!"""

        self.sample_user_description = "Круто!\nНаконец, кратко опиши себя\n\nНапример:\nМеня зовут Артем, я люблю качаться и есть курочку"

        self.sample_event_description = '\nКратко опиши событие\n\nНапример:\nПойдем качаться и есть курочку'

        self.database_params = {"host": "localhost",
                                "user": "root",
                                "password": "Password",
                                "database": "coffee_bot"}


Constants = ConstantsClass()