class Group:
    def __init__(self,name, text, skills=None,in_active=True):
        self.name = name
        self.text = text
        self.skills = skills if skills is not None else []
        self.in_active = in_active

    def add_skill(self,skill):
        '''Добавляет в список навыков новый навык'''
        if skill is not self.skills:
            self.skills.append(skill)
            print(f'Навык {skill} добавлен в список требуемых навыков')
        else:
            print(f'Навык {skill} уже присутствует в списке требуемых навыков')

    def delete_skill(self, skill):
        '''Удаляет навык из списка требуемых навыков для проекта'''
        if skill in self.skills:
            self.skills.remove(skill)
            print(f"Навык {skill} удален из списка требуемых проекту навыков ")
        else:
            print(f"Навык {skill} на найден в списке требуемых проекту навыков")

    def activ_status(self):
        '''Показывает набирает проект участников или нет'''
        self.in_active = not self.in_active
        status = 'набирает участников' if self.in_active else 'прекратил набор'
        print(f'Проект {self.name} {status}')

    def show_project(self):
        '''Возвращает карточку проекта'''
        return (f'Проект: {self.name}\n'
                f'Описание: {self.text}\n'
                f'Статус проекта: {'Идёт набор' if self.in_active else 'Набор прекращён'}\n'
                f'Список навыков/специалистов необходимых для проекта {self.skills}')
