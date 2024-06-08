from pprint import pprint
from general_db_functions import open_connection, update_data_in_column, display_all_data_from_table, add_data_to_table

from hidden.tokenfile import OWNER_CHAT_ID

user_id = OWNER_CHAT_ID
room_name = 'base_room_' + str(user_id)


# users = {'111666', user_id}  # "111666" - моделирование заполненности БД


# configurate = user_id + '_in_' + room_name
# users_and_roles = {
#     configurate: {
#         'telegram_id': user_id,
#         'nickname': 'OWNER',
#         'room': room_name,
#         'role': 'admin'
#     }
# }


# rooms_settings = {
#     room_name: {
#         'name': room_name,
#         'owner': user_id,
#         'admins': [user_id],
#         'members': [user_id],
#         'password': 'пароль',
#         'rights_to_create_task': 'admins',  # один из ['owner', 'admins', 'members']
#         'period_of_remind': '30:00',  # значение, которое будут получать каждая task по умолчанию
#         'execution_level': 0.0,  # значение, которое будут получать каждая task по умолчанию
#         'accept_by_author': False,  # значение, которое будут получать каждая task по умолчанию
#         'livetime_after_ending': '12:00',  # значение, которое будут получать каждая task по умолчанию
#     }
# }

# Словарь в timestamps_for_standard_mailings в будущем будет формироваться путем запроса к БД,
# с этим же словарем будет работать класс TimeToMail.
timestamps_for_standard_mailings = {
    '2023.12.10 14:30': [user_id],
    '2025.10.05 14:30': [user_id],
    '2023.11.06 14:35': [231423, 231425],
    '2023.12.10 14:15': [231423, 231425],
}

open_connection(table_name='timestamps', name_of_columns=('time', 'user'))
add_data_to_table(table_name='timestamps', column_names=['time', 'user'], values=['2023.12.10 14:16', '231426'])
display_all_data_from_table(table_name='timestamps')
update_data_in_column(
    table_name='timestamps', base_column_name='time', base_column_value='2023.12.10 14:16',
    target_column_name='user', new_value='231424'
)
display_all_data_from_table(table_name='timestamps')


# Словарь в all_tasks в будущем будет формироваться путем запроса к БД, с этим же словарем будет работать
# класс TasksCash.
all_tasks = {
    '29': {'accept_by_author': False, 'accept_in_time': '2023-12-10 15:30', 'author': 'Петя',
                    'create_time': '2023-12-10 14:30', 'execution_level': 0.01, 'executor': user_id,
                    'livetime_after_ending': '12:00', 'nickname': 'Толя', 'number': '29', 'period_of_remind': '30:00',
                    'recipient_id': user_id, 'room': 'Тайная комната', 'text': 'Постирать носки'},
             '104': {'accept_by_author': False, 'accept_in_time': '2023-12-10 15:30', 'author': 'Петя',
                     'create_time': '2023-12-10 14:30', 'execution_level': 0.39, 'executor': user_id,
                     'livetime_after_ending': '12:00', 'nickname': 'Толя', 'number': '104', 'period_of_remind': '30:00',
                     'recipient_id': user_id, 'room': 'Красная комната', 'text': 'Купить хлеб'},
             '255': {'accept_by_author': False, 'accept_in_time': '2023-12-10 15:30', 'author': 'Петя',
                     'create_time': '2023-12-10 14:30', 'execution_level': 0.55, 'executor': user_id,
                     'livetime_after_ending': '12:00', 'nickname': 'Ваня', 'number': '255', 'period_of_remind': '30:00',
                     'recipient_id': user_id, 'room': 'Первая комната', 'text': 'Постирать носки'},
             '512': {'number': '512', 'recipient_id': user_id, 'nickname': 'Петя', 'room': 'Первая комната',
                     'text': 'Принять душ', 'author': 'Петя', 'executor': user_id, 'create_time': '2023-12-10 14:30',
                     'period_of_remind': '30:00', 'execution_level': 0.7, 'accept_by_author': False,
                     'accept_in_time': '2023-12-10 15:30', 'livetime_after_ending': '12:00'},
             '566': {'accept_by_author': False, 'accept_in_time': '2023-12-10 15:30', 'author': 'Ваня',
                     'create_time': '2023-12-10 14:30', 'execution_level': 0.39, 'executor': user_id,
                     'livetime_after_ending': '12:00', 'nickname': 'Вася', 'number': '566', 'period_of_remind': '30:00',
                     'recipient_id': user_id, 'room': 'Секретная комната', 'text': 'Пройти курс Python'},
             '691': {'accept_by_author': False, 'accept_in_time': '2023-12-10 15:30', 'author': 'Вася',
                     'create_time': '2023-12-10 14:30', 'execution_level': 0.75, 'executor': user_id,
                     'livetime_after_ending': '12:00', 'nickname': 'Вася', 'number': '691', 'period_of_remind': '30:00',
                     'recipient_id': user_id, 'room': 'Комната 101', 'text': 'Скачать торрент'},
             '707': {'accept_by_author': False, 'accept_in_time': '2023-12-10 15:30', 'author': 'Толя',
                     'create_time': '2023-12-10 14:30', 'execution_level': 0.03, 'executor': 231424,
                     'livetime_after_ending': '12:00', 'nickname': 'Вася', 'number': '707', 'period_of_remind': '30:00',
                     'recipient_id': 231423, 'room': 'Красная комната', 'text': 'Постирать носки'},
             '853': {'accept_by_author': False, 'accept_in_time': '2023-12-10 15:30', 'author': 'Толя',
                     'create_time': '2023-12-10 14:30', 'execution_level': 0.76, 'executor': 231425,
                     'livetime_after_ending': '12:00', 'nickname': 'Петя', 'number': '853', 'period_of_remind': '30:00',
                     'recipient_id': 231424, 'room': 'Первая комната', 'text': 'Постирать носки'},
             '858': {'accept_by_author': False, 'accept_in_time': '2023-12-10 15:30', 'author': 'Толя',
                     'create_time': '2023-12-10 14:30', 'execution_level': 0.99, 'executor': 231423,
                     'livetime_after_ending': '12:00', 'nickname': 'Петя', 'number': '858', 'period_of_remind': '30:00',
                     'recipient_id': 231424, 'room': 'Пятая комната', 'text': 'Постирать носки'},
             '950': {'accept_by_author': False, 'accept_in_time': '2023-12-10 15:30', 'author': 'Петя',
                     'create_time': '2023-12-10 14:30', 'execution_level': 0.3, 'executor': 231423,
                     'livetime_after_ending': '12:00', 'nickname': 'Ваня', 'number': '950', 'period_of_remind': '30:00',
                     'recipient_id': 231425, 'room': 'Красная комната', 'text': 'Скачать торрент'},
             '270': {'number': '270', 'recipient_id': 231424, 'nickname': 'Петя', 'room': 'Комната 101',
                     'text': 'Скачать торрент', 'author': 'Толя', 'executor': 231425, 'create_time': '2023-12-10 14:30',
                     'period_of_remind': '30:00', 'execution_level': 0.12, 'accept_by_author': False,
                     'accept_in_time': '2023-12-10 15:30', 'livetime_after_ending': '12:00'},
             '661': {'number': '661', 'recipient_id': 231424, 'nickname': 'Петя', 'room': 'Красная комната',
                     'text': 'Купить хлеб', 'author': 'Толя', 'executor': 231425, 'create_time': '2023-12-10 14:30',
                     'period_of_remind': '30:00', 'execution_level': 0.58, 'accept_by_author': False,
                     'accept_in_time': '2023-12-10 15:30', 'livetime_after_ending': '12:00'},
             '353': {'number': '353', 'recipient_id': 231423, 'nickname': 'Вася', 'room': 'Тайная комната',
                     'text': 'Принять душ', 'author': 'Вася', 'executor': 231424, 'create_time': '2023-12-10 14:30',
                     'period_of_remind': '30:00', 'execution_level': 0.7, 'accept_by_author': False,
                     'accept_in_time': '2023-12-10 15:30', 'livetime_after_ending': '12:00'},
             '464': {'number': '464', 'recipient_id': 231423, 'nickname': 'Вася', 'room': 'Секретная комната',
                     'text': 'Скачать торрент', 'author': 'Петя', 'executor': 231424, 'create_time': '2023-12-10 14:30',
                     'period_of_remind': '30:00', 'execution_level': 0.43, 'accept_by_author': False,
                     'accept_in_time': '2023-12-10 15:30', 'livetime_after_ending': '12:00'},
             '425': {'number': '425', 'recipient_id': 231423, 'nickname': 'Вася', 'room': 'Первая комната',
                     'text': 'Пройти курс Python', 'author': 'Петя', 'executor': 231423,
                     'create_time': '2023-12-10 14:30', 'period_of_remind': '30:00', 'execution_level': 0.82,
                     'accept_by_author': False, 'accept_in_time': '2023-12-10 15:30', 'livetime_after_ending': '12:00'},
             '66': {'number': '66', 'recipient_id': 231424, 'nickname': 'Петя', 'room': 'Красная комната',
                    'text': 'Пройти курс Python', 'author': 'Петя', 'executor': 231424,
                    'create_time': '2023-12-10 14:30',
                    'period_of_remind': '30:00', 'execution_level': 0.65, 'accept_by_author': False,
                    'accept_in_time': '2023-12-10 15:30', 'livetime_after_ending': '12:00'},
             '237': {'number': '237', 'recipient_id': 231423, 'nickname': 'Вася', 'room': 'Комната 101',
                     'text': 'Принять душ', 'author': 'Вася', 'executor': 231426, 'create_time': '2023-12-10 14:30',
                     'period_of_remind': '30:00', 'execution_level': 0.78, 'accept_by_author': False,
                     'accept_in_time': '2023-12-10 15:30', 'livetime_after_ending': '12:00'},
             '928': {'number': '928', 'recipient_id': 231426, 'nickname': 'Толя', 'room': 'Комната 101',
                     'text': 'Принять душ', 'author': 'Ваня', 'executor': 231424, 'create_time': '2023-12-10 14:30',
                     'period_of_remind': '30:00', 'execution_level': 0.99, 'accept_by_author': False,
                     'accept_in_time': '2023-12-10 15:30', 'livetime_after_ending': '12:00'},
             '929': {'number': '929', 'recipient_id': 231423, 'nickname': 'Вася', 'room': 'Секретная комната',
                     'text': 'Принять душ', 'author': 'Толя', 'executor': 231426, 'create_time': '2023-12-10 14:30',
                     'period_of_remind': '30:00', 'execution_level': 0.06, 'accept_by_author': False,
                     'accept_in_time': '2023-12-10 15:30', 'livetime_after_ending': '12:00'}
    }
