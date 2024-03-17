# for example:
user_id = str(5180054391)
room_name = 'пробная комната'


users = {'111666', user_id}  # "111666" - моделирование заполненности БД


configurate = user_id + '_in_' + room_name
users_and_roles = {
    configurate: {
        'telegram_id': user_id,
        'nickname': 'vasoyk',
        'room': room_name,
        'role': 'admin'
    }
}


rooms_settings = {
    'комната_1': {
        'name': room_name,
        'owner': user_id,
        'admins': [user_id, 'telegram_id', 'telegram_id'],
        'members': [user_id, 'telegram_id', 'telegram_id'],
        'password': 'пароль',
        'rights_to_create_task': 'all_users'
    }
}


all_tasks = {
    'random_number': {
        'room': room_name,
        'text': 'текст задачи',
        'author': user_id,
        'executor': 'telegram_id исполнителя',
        'create_time': '2023-12-10 14:30',
        'period_of_remind': '30:00',
        'execution_level': 'уровень выполнения',
        'accept_by_author': False,
        'accept_in_time': '2023-12-10 15:30',
        'livetime_after_ending': '12:00',
        'list of recipients': 'telegram_id тех, кто получает уведомление'
    }
}
