import g4f

class Ai_promt:

    def inquiry_user(inp: str) -> str:
        promt = ('сформулируй текст для навыков из списка [Frontend, GameDev, Дизайнер, Teamlead, Тестировщик, Python, Java, JavaScript, C#, C++, SQL, Мобильная разработка].'
                 ' Если навыка в тексте нет, то не пиши его. Ответ приведи в виде строки навыков пользователя через запятую, без переносов строк и тому подобное ( '
                 ' (пример) [back-end, аналитка]. Вот текст: ') + inp + '.Ответь на русском'

        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": promt}],
            stream=True,
        )

        # Собираем все сообщения в список
        result = []
        for message in response:
            result.append(message)

        # Объединяем все части в один ответ
        s = ''.join(result).split(',')
        for i in range(len(s)):
            s[i] = s[i].strip()
        return s  # Возвращаем собранный ответ

    def inquiry_project(inp: str) -> str:
        promt = ('сформулируй текст какие навыки из списка [Frontend, GameDev, Дизайнер, Teamlead, Тестировщик, Python, Java, JavaScript, C#, C++, SQL, Мобильная разработка].'
                 'понадобятся для реализации описанного проекта. Если навыка в тексте нет, то не пиши его. Ответ приведи в виде строки навыков пользователя через запятую, без переносов строк и тому подобное ( '
                 ' (пример) [back-end, аналитка]. Вот текст: ') + inp + '.Ответь на русском'

        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": promt}],
            stream=True,
        )

        # Собираем все сообщения в список
        result = []
        for message in response:
            result.append(message)

        # Объединяем все части в один ответ
        s = ''.join(result).split(',')
        for i in range(len(s)):
            s[i] = s[i].strip()
        return s  # Возвращаем собранный ответ

# print(type(Ai_promt.inquiry('верстал сайты, делал игры, разрабатывал на python')))

