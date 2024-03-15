

users = {'111666'}  # "111666" - моделирование заполненности БД


configurate = 'user_id' + '_in_' + 'room_name'
users_and_roles = {
    configurate: {
        'telegram_id': '1111111',
        'nickname': 'vasoyk',
        'room_name': 'first_room',
        'role': 'admin'
    }
}


rooms_settings = {
    'комната_1': {
        'name': 'комната_1',
        'owner': 'telegram_id',
        'admins': ['telegram_id', 'telegram_id', 'telegram_id'],
        'members': ['telegram_id', 'telegram_id', 'telegram_id'],
        'password': 'пароль111',
        'rights_to_create_task': 'all_users'
    }
}





task = {
    'random_number': {
        'number': 'random_number',
        'room': 'комната_1',
        'text': 'текст задачи',
        'author': 'telegram_id автора',
        'executor': 'telegram_id исполнителя',
        'period_of_remind': '30:00',
        'execution_level': 'уровень выполнения',
        'accept_by_author': False,
        'accept_in_time': '2023-12-10 15:30:00',
        'livetime_after_ending': '12:00:00',
        'list of recipients': 'telegram_id тех, кто получает уведомление'
    }
}
