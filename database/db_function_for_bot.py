from general_db_functions import open_connection, display_all_data_from_table, add_data_to_table

TABLE_USERS_NAME = 'users'
TABLE_USERS_COLUMN = ('telegram_id', 'nickname', 'observ_status')


def initialize_table(table_name=TABLE_USERS_NAME, name_of_columns=TABLE_USERS_COLUMN) -> None:
    """
    Функция создает или подключается к таблице users в БД
    """
    connect = open_connection(table_name=table_name, name_of_columns=name_of_columns)
    cursor = connect.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    if row_count == 0:
        val = ['234522', 'Иван', 'Админ']
        add_data_to_table(table_name=TABLE_USERS_NAME, column_names=TABLE_USERS_COLUMN, values=val)
    display_all_data_from_table(table_name=TABLE_USERS_NAME)
    print('Установлено подключение')


initialize_table()
