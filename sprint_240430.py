


# 1) В модуле kvazi_db определяем заново структуры all_tasks и rooms_settings по новым стандартам:
#V - дублирование одной задачи, если отслеживающих несколько
#V - вместо 'telegram_id исполнителя' ник исполнителя при регистрации в боте
# - в модуле main_objects параллельно изменить классы. В частности, класс Tasks - под работу со словарем, формируемом в
# модуле kvazi_db
# - 'list_of_recipients' лишнее (будет определяться через структуру)
# 2) В модуле kvazi_db создаем генераторы для формирования all_tasks и rooms_settings
# 3) В модуле  kvazi_db определить необходимость переменных configurate и users ввиду нового стандарта

# В дальнейшем kvazi_db переформатируется в модуль работы с БД с функциями чтения, записи, удаления записей в БД

# 4) Модуль main_objects содержит классы главных объектов: all_tasks и rooms_settings
# Экземпляры данных классов по сути являются кэшем, получая сохраненные данные в БД,
# изменяя их согласно запросам пользователей и сохраняя в БД.
# Необходимо переписать классы исходя из структурных изменений в БД, добавляя описание к функциям
