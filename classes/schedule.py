
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


class Categories:
    def __init__(self):
        self.list_of_categories = [
            'Не забыть сделать',
            'Не забыть купить',
            'Не забыть посетить',
            'Обновить пароли на сервисы'
        ]

    def add_new_category(self, new_category: str) -> bool:
        if new_category in self.list_of_categories:
            print('такая категория уже существует')
            return False
        else:
            self.list_of_categories.append(new_category)
            return True

    def del_category(self, category: str) -> None:
        self.list_of_categories.remove(category)

    def return_to_default(self) -> None:
        Categories.__init__(self)


class Task:
    def __init__(self, text, category, reminder_time):
        self.text = text
        self.category = category
        self.reminder_time = reminder_time

    def __str__(self):
        return f"Task: {self.text}, Category: {self.category}, Reminder Time: {self.reminder_time}"


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

