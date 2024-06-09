from general_db_functions import open_connection, display_all_data_from_table, add_data_to_table

DATABASE_NAME = 'bot_database.sql'
TABLE_USERS_NAME = 'users'
TABLE_USERS_COLUMN = ('telegram_id', 'nickname', 'observ_status')

conn = open_connection(table_name=TABLE_USERS_NAME, name_of_columns=TABLE_USERS_COLUMN)
display_all_data_from_table(table_name=TABLE_USERS_NAME)

val = ['234522', 'Иван', 'Админ']
add_data_to_table(table_name=TABLE_USERS_NAME, column_names=TABLE_USERS_COLUMN, values=val)

