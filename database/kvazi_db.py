from hidden.tokenfile import OWNER_CHAT_ID

user_id = str(OWNER_CHAT_ID)
room_name = 'Базовая комната'


users = {'111666', user_id}  # "111666" - моделирование заполненности БД


configurate = user_id + '_in_' + room_name
users_and_roles = {
    configurate: {
        'telegram_id': user_id,
        'nickname': 'OWNER',
        'room': room_name,
        'role': 'admin'
    }
}


rooms_settings = {
    room_name: {
        'name': room_name,
        'owner': user_id,
        'admins': [user_id],
        'members': [user_id],
        'password': 'пароль',
        'rights_to_create_task': 'admins'  # один из ['owner', 'admins', 'members']
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
        'execution_level': 0.45,
        'accept_by_author': False,
        'accept_in_time': '2023-12-10 15:30',
        'livetime_after_ending': '12:00',
        'list_of_recipients': 'telegram_id тех, кто получает уведомление'
    }
}


