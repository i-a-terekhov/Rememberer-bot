
class RegularSchedule:
    def __init__(self):
        pass


class ListOfTasks:
    def __init__(self):
        self.list_of_tasks = list()

    def check_empty(self):
        if len(self.list_of_tasks) == 0:
            return False
        else:
            return True

    def add_task(self, describe: str):
        self.list_of_tasks.append(describe)


class RoomsTasks:
    default_list_of_tasks = [
            'Не забыть сделать',
            'Не забыть купить',
            'Не забыть посетить',
            'Обновить пароли на сервисы'
        ]

    def __init__(self):
        self.list_of_tasks = self.default_list_of_tasks

    def add_new_category(self, new_category: str) -> bool:
        if new_category in self.list_of_tasks:
            print('такая категория уже существует')
            return False
        else:
            self.list_of_tasks.append(new_category)
            return True

    def del_category(self, category: str) -> None:
        self.list_of_tasks.remove(category)

    def return_to_default(self) -> None:
        self.__init__()


class Task:
    def __init__(self, room, text, category, reminder_time):
        self.room = room  # уник. имя комнаты - ключ в словаре, значения для которого - лист с ID участников комнаты
        self.text = text  # текст задачи - ключ в словаре, значения для которого - подзадачи
        self.reminder_time = reminder_time

    def __str__(self):
        return f"Task: {self.text}, Text: {self.text}, Reminder Time: {self.reminder_time}"


class Group:
    def __init__(self, group_id):
        self.group_id = group_id
        self.members = []
        self.categories = Categories()
        self.tasks = []

    def add_member(self, user_id):
        self.members.append(user_id)

    def create_task(self, text, category, reminder_time):
        task = Task(text, category, reminder_time)
        self.tasks.append(task)
        return task

