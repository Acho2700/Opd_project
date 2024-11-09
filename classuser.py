class User:
    def __init__(self, name, skills=None, search_job=False, in_active=True):
        self.name = name
        self.skills = skills if skills is not None else []
        self.search_job = search_job
        self.in_active = in_active
    def add_skill(self, skill):
        """Добавляет новый навык в список навыков."""
        if skill is not self.skills:
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
    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return (f"Имя пользователя: {self.name}\n"
                f"Навыки пользователя: {', '.join(self.skills) if self.skills else 'Нет навыков'}\n"
                f"В поиске работы: {'Да' if self.search_job else 'Нет'}\n"
                f"Статус активности: {'Активен' if self.in_active else 'Неактивен'}")

#Пример
user = User(name="Иван", skills=["Python", "JavaScript"], search_job=True)
print(user)
user.add_skill("Java")
user.delete_skill("Python")
user.activ_status()
print(user)