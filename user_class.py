class User:
    def __init__(self, name, age, skills=None, in_active=True):
        self.name = name
        self.age = age
        self.skills = skills if skills is not None else []
        self.in_active = in_active

    def add_skill(self, skill):
        """Добавляет новый навык в список навыков."""
        if skill not in self.skills:
            self.skills.append(skill)
            print(f"Навык {skill} добавлен")
        else:
            print(f"Навык {skill} уже существует")

    def delete_skill(self, skill):
        """Удаляет навык из списка навыков."""
        if skill in self.skills:
            self.skills.remove(skill)
            print(f"Навык {skill} удален")
        else:
            print(f"Навык {skill} на найден")

    def activ_status(self):
        """Переключает статус активности пользователя."""
        self.in_active = not self.in_active
        status = "Активен" if self.in_active else "Неактивен"
        print(f"Пользователь {self.name} {status}")

    def show_anketa(self):
        """Возвращает строковое представление пользователя."""
        return (f"Имя пользователя: {self.name}\n"
                f"Возраст пользователя: {self.age}\n"
                f"Навыки пользователя: {', '.join(self.skills) if self.skills else 'Нет навыков'}\n"
                f"В поиске работы: {'Да' if self.in_active else 'Нет'}\n")

