from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, InlineKeyboardButton, CallbackQuery
from users_dict import Dict_users
from user_class import User
from group_class import Group
from project_dict import Dict_project
from random import choice
from AI import Ai_promt

bot = Bot(token="7855213389:AAFdmLy9DS1HJ39MuPaO48XKogYtvuKihOw")
dp = Dispatcher(bot, storage=MemoryStorage())


menu_main_text = "1. Добавить навык\n 2.Удалить навык\n 3. Выключить\Включить анкету\n 4. Моя анкета\n 5. Искать проект/участника"

#класс состояний пользвателя
class Wait(StatesGroup):
    join_team = State()
    group_or_user = State()
    name = State()
    name_project = State()
    age = State()
    text = State()
    text_project = State()
    recommendations = State()
    menu_answer = State()
    add_skill = State()
    del_skill = State()
    anketa_activ = State()



#вывод кнопок меню
def menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["1", "2", "3", "4", "5"]
    markup.add(*buttons)
    return markup

#вывод кнопок реакций
def reaction_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Лайк", "Дизлайк", "Вернуться назад"]
    markup.add(*buttons)
    return markup

# Функция для создания инлайн-клавиатуры с навыками программирования (для добавления)
def skill_keyboard():
    markup = types.InlineKeyboardMarkup()
    skills = ['Frontend',
              'Дизайнер',
              'Teamlead',
              'Тестировщик',
              'Python',
              'Java',
              'JavaScript',
              'C#',
              'C++',
              'SQL',
              'Мобильная разработка',
              'GameDev'] # Список навыков
    # Добавляем кнопки по 3 в ряд
    for i in range(0, len(skills), 3):
        row = []
        for j in range(3):
            if i + j < len(skills):
                row.append(InlineKeyboardButton(skills[i + j], callback_data=skills[i + j]))
        markup.add(*row)
    return markup


# Функция для создания инлайн-клавиатуры с навыками программирования (для удаления)
def del_skill_keyboard(user):
    markup = types.InlineKeyboardMarkup()
    if len(user.skills) == 0:
        return None
    for i in range(0, len(user.skills), 3):
        row = []
        for j in range(3):
            if i + j < len(user.skills):
                row.append(InlineKeyboardButton(user.skills[i + j], callback_data=f"del_{user.skills[i + j]}"))
        markup.add(*row)  # Добавляем ряд кнопок в клавиатуру

    return markup



#обработчик команды старт, приветствие и выбор действия
@dp.message_handler(commands='start', state= '*')
async def start(message: types.Message):
    user = None
    chat_id = message.chat.id

    #Проверка зарегистрирован ли пользователь (если нет - регистрируемся, если да - меню)
    if chat_id not in Dict_project.dict_project and chat_id not in Dict_users.dict_users:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True)
        buttons = ["Вступить в комманду",
                   "Найти комманду"]
        markup.add(*buttons)
        await bot.send_message(message.chat.id,
                               'Привет, я бот для поиска IT команды \n '
                               'Выбери что хочешь сделать:',
                               reply_markup=markup
                               )
        await Wait.group_or_user.set()
    else:
        markup = menu_keyboard()
        await bot.send_message(message.chat.id, menu_main_text, reply_markup=markup)
        await Wait.menu_answer.set()

#функция выборка что регистрирует пользователь (анкету участника \ анкету проекта)
@dp.message_handler(state= Wait.group_or_user)
async def group_or_user(message: types.Message, state: FSMContext):
    if message.text == "Вступить в комманду":
        await state.update_data(join_team=True)
        await bot.send_message(message.chat.id, 'Отлично!'
                                                ' \n Введи свое ФИО'
                               )
        await Wait.name.set()

    elif message.text == "Найти комманду":
        await state.update_data(join_team=False)
        await bot.send_message(message.chat.id, 'Отлично!'
                                                ' \n Введи Название проекта'
                               )
        await Wait.name_project.set()



#функция для получения имени анкеты участника
@dp.message_handler(state= Wait.name)
async def name(message: types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    await bot.send_message(message.chat.id, 'Отлично! \n'
                                            ' Теперь введи возраст'
                           )
    await Wait.age.set()

#функция для получения имени анкеты проекта
@dp.message_handler(state= Wait.name_project)
async def name_project(message: types.Message, state: FSMContext):
    await state.update_data(name_project = message.text)
    await bot.send_message(message.chat.id, 'Отлично! \n'
                                            ' Теперь расскажи о проекте'
                           )
    await Wait.text_project.set()


#функция для получения возраста (если анкета участника)
@dp.message_handler(state = Wait.age)
async def age(message: types.Message, state: FSMContext):
    #проверка на корректность ввода возраста
    try:
        if 10 > int(message.text) or int(message.text) > 100:
            await message.answer("Какой-то странный возраст")
            return
    except(TypeError, ValueError):
        await message.answer("Какой-то странный возраст")
        return
    await state.update_data(age = message.text)
    await message.answer("Расскажи о своих навыках и опыте в проектах")
    await Wait.text.set()


#функция Ввод и занесение описания в анкету участника
@dp.message_handler(state = Wait.text)
async def text(message: types.Message, state: FSMContext):
    await state.update_data(text = message.text)
    data = await state.get_data()

    join_team = data["join_team"]
    name = data["name"]
    age = data["age"]
    text = data["text"]
    skills = Ai_promt.inquiry_user(data["text"])
    chat_id = message.chat.id

    user = User(name, age, text, skills, True)
    Dict_users.dict_users[chat_id] = user
    caption = user.show_anketa()

    await message.answer(f"Вот твоя анкета")
    await message.answer(f"{caption}")
    markup = menu_keyboard()
    await message.answer(menu_main_text,
                         reply_markup=markup
                         )
    await Wait.menu_answer.set()

#функция ввод и занесения описания в анкету проекта
@dp.message_handler(state = Wait.text_project)
async def text_project(message: types.Message, state: FSMContext):
    await state.update_data(text_project = message.text)

    data = await state.get_data()
    join_team = data["join_team"]
    name_project = data["name_project"]
    text = data["text_project"]
    skills = Ai_promt.inquiry_project(data["text_project"])
    chat_id = message.chat.id

    project = Group(name_project, text, skills, True)
    Dict_project.dict_project[chat_id] = project
    caption = project.show_anketa()

    await message.answer(f"Вот анкета твоего проекта")
    await message.answer(f"{caption}")
    markup = menu_keyboard()
    await message.answer(menu_main_text,
                         reply_markup=markup
                         )
    await Wait.menu_answer.set()


#функция меню
@dp.message_handler(state= Wait.menu_answer)
async def menu_answer(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    #Добавление навыка в анкету
    if message.text == '1':
        await message.answer('Выбери навык для добавления:', reply_markup=skill_keyboard())
        await Wait.add_skill.set()

    #Удаление навыка из анкеты
    if message.text == '2':
        user = None
        if chat_id in Dict_users.dict_users:
            user = Dict_users.dict_users[chat_id]

        if chat_id in Dict_project.dict_project:
            user = Dict_project.dict_project[chat_id]

        if user:
            markup = del_skill_keyboard(user)
            #если нет навыков ливает с f
            if markup == None:
                markup = menu_keyboard()
                await message.answer('У вас нет навыков!')
                await message.answer(menu_main_text, reply_markup=markup)
                await Wait.menu_answer.set()
                return
            await message.answer('Выбери навык для удаления:', reply_markup=markup)
            await Wait.del_skill.set()

    #переключение активности анкеты (напомните задействовать это в системе рекомендаций мне!!!!)
    if message.text == '3':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True)
        buttons = ["Нет", "Да"]
        markup.add(*buttons)
        chat_id = message.chat.id
        if chat_id in Dict_users.dict_users:
            user = Dict_users.dict_users[chat_id]
            if user.in_active:
                await message.answer('Вы уверены что хотите выключить анкету?',
                                     reply_markup=markup
                                     )
                await Wait.anketa_activ.set()
            else:
                await message.answer('Вы уверены что хотите включить анкету?',
                                     reply_markup=markup
                                     )
                await Wait.anketa_activ.set()

        if chat_id in Dict_project.dict_project:
            project = Dict_project.dict_project[chat_id]
            if project.in_active:
                await message.answer('Вы уверены что хотите выключить анкету проекта?',
                                     reply_markup=markup
                                     )
                await Wait.anketa_activ.set()
            else:
                await message.answer('Вы уверены что хотите включить анкету проекта?',
                                     reply_markup=markup
                                     )
                await Wait.anketa_activ.set()

    # просто просмотр своей анкеты)))
    if message.text == '4':
        if chat_id in Dict_users.dict_users:
            user = Dict_users.dict_users[chat_id]
            caption = user.show_anketa()
            markup = menu_keyboard()
            await message.answer(f"Вот твоя анкета")
            await message.answer(f"{caption}",
                                 reply_markup=markup
                                 )
            await message.answer(menu_main_text)

        if chat_id in Dict_project.dict_project:
            user = Dict_project.dict_project[chat_id]
            caption = user.show_project()
            markup = menu_keyboard()
            await message.answer(f"Вот твой проект")
            await message.answer(f"{caption}",
                                 reply_markup=markup
                                 )
            await message.answer(menu_main_text)

    #поиск анкет других участников
    if message.text == '5':
        markup = reaction_keyboard()
        await message.answer('Подбираем анкеты для вас...',
                             reply_markup=markup
                             )

        #если анкета участника то подбитрает проекты, иначе участников
        if chat_id in Dict_users.dict_users:
            user = Dict_users.dict_users[chat_id]
            result = get_random_user_with_matching_skill(Dict_project.dict_project, user.skills, user.last_users)

            #если не нашлось подходящих проектов ливает в меню
            if result == None:
                markup = menu_keyboard()
                await message.answer('Никого нет для вас',
                                     reply_markup=markup
                                     )
                await message.answer(menu_main_text)
                await Wait.menu_answer.set()

            #выплевывает анкету
            else:
                key = result[0]
                value = result[1]
                user.last_users.append(key)
                project = Dict_project.dict_project[key]
                caption = project.show_anketa()
                await message.answer(f'{caption}')
                await state.update_data(liked_id=key)
                await Wait.recommendations.set()

        elif chat_id in Dict_project.dict_project:
            project = Dict_project.dict_project[chat_id]
            result = get_random_user_with_matching_skill(Dict_users.dict_users, project.skills, project.last_users)

            # если не нашлось подходящих проектов ливает в меню
            if result == None:
                markup = menu_keyboard()
                await message.answer('Никого нет для вас',
                                     reply_markup=markup
                                     )
                await message.answer(menu_main_text)
                await Wait.menu_answer.set()

            #выплевывает анкету
            else:
                key = result[0]
                value = result[1]
                project.last_users.append(key)
                user = Dict_users.dict_users[key]
                caption = user.show_anketa()
                await message.answer(f'{caption}')
                await state.update_data(liked_id = key)
                await Wait.recommendations.set()



# Обработка нажатия на инлайн-кнопки добавления навыка
@dp.callback_query_handler(state=Wait.add_skill)
async def handle_skill_selection(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    skill = callback_query.data  # Получаем навык из callback_data

    user = None
    if chat_id in Dict_users.dict_users:
        user = Dict_users.dict_users[chat_id]

    if chat_id in Dict_project.dict_project:
        user = Dict_project.dict_project[chat_id]

    user.add_skill(skill)  # Добавляем выбранный навык
    await callback_query.answer('Навык успешно добавлен!')
    markup = menu_keyboard()
    await callback_query.message.answer(menu_main_text, reply_markup=markup)  # Отправляем главное меню
    await Wait.menu_answer.set()  # Завершаем состояние



# Обработка нажатия на инлайн-кнопки удаления навыка
@dp.callback_query_handler(state=Wait.del_skill)
async def handle_del_skill_selection(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    skill = callback_query.data[4:]  # Получаем навык из callback_data, удаляя префикс "del_"

    user = None
    if chat_id in Dict_users.dict_users:
        user = Dict_users.dict_users[chat_id]

    if chat_id in Dict_project.dict_project:
        user = Dict_project.dict_project[chat_id]

    user.delete_skill(skill)  # Удаляем выбранный навык
    await callback_query.answer('Навык успешно удален!')
    markup = menu_keyboard()
    await callback_query.message.answer(menu_main_text, reply_markup=markup)  # Отправляем главное меню
    await Wait.menu_answer.set()  # Завершаем состояние


#функция переключения активности анкеты
@dp.message_handler(state= Wait.anketa_activ)
async def anketa_activ(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = None
    if chat_id in Dict_users.dict_users:
        user = Dict_users.dict_users[chat_id]


    if chat_id in Dict_project.dict_project:
        user = Dict_project.dict_project[chat_id]

    check = user.in_active
    #бот выводит 'Вы уверены что хотите выключить\включить анкету?'

    #если анкета юзера включена и он нажимает да
    if message.text == 'Да' and check:
        user.activ_status()
        await message.answer('Ваша анкета больше не активна')
        markup = menu_keyboard()
        await message.answer(menu_main_text,
                             reply_markup=markup
                             )
        await Wait.menu_answer.set()

    #если анкета юзера выключена и он нажимает да
    elif message.text == 'Да' and check == False:
        user.activ_status()
        await message.answer('Ваша анкета снова активна')
        markup = menu_keyboard()
        await message.answer(menu_main_text,
                             reply_markup=markup
                             )
        await Wait.menu_answer.set()

    #если юзер передумал и возращается в меню ( нажимает 'нет')
    elif message.text == 'Нет':
        markup = menu_keyboard()
        await message.answer(menu_main_text,
                             reply_markup=markup
                             )
        await Wait.menu_answer.set()





#функция получения подходящего рекомендованного пользователя
def get_random_user_with_matching_skill(user_dict, skill_list, last_users):
    """Возвращает случайного пользователя с хотя бы одним совпадающим навыком из заданного списка,
    избегая повторного выбора последних 5 пользователей."""



    # Фильтруем пользователей, у которых есть хотя бы один навык из skill_list
    matching_users = {}
    for key, user in user_dict.items():
        flag = any(skill == skill2 for skill in skill_list for skill2 in user.skills)
        if flag:
            matching_users[key] = user

    # Если есть совпадения, выбираем случайного пользователя, избегая последних 5
    if matching_users:
        while True:
            random_key = choice(list(matching_users.keys()))
            if random_key not in last_users[-5:]:
                return random_key, matching_users[random_key]
            else:
                return None




# функция рекомендаций
@dp.message_handler(state= Wait.recommendations)
async def recommendations(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    data = await state.get_data()
    d = list(data.values())
    user = None
    # получение лайкнутого пользователя если первая анкета которая попалась после меню была лайкнута
    key = data["liked_id"]
    # проверка анкеты юзера (является она участником или проектом)
    if chat_id in Dict_users.dict_users:
        user = Dict_users.dict_users[chat_id]
    elif chat_id in Dict_project.dict_project:
        user = Dict_project.dict_project[chat_id]


    if message.text == 'Дизлайк' or message.text == 'Лайк':
        if message.text == 'Лайк':
            markup = menu_keyboard()
            # отправка уведомления пользователю котрого лайнкули
            await bot.send_message(chat_id= key,
                                   text= f'Вы понравились данному пользователю: @{message.from_user.username}'
                                   )

            await bot.send_message(chat_id= key,
                                   text= f'{user.show_anketa()} \n',
                                   reply_markup=markup
                                   )
            await Wait.recommendations.set()

        if chat_id in Dict_users.dict_users:
            user = Dict_users.dict_users[chat_id]
            caption_flag = user.show_anketa()
            result = get_random_user_with_matching_skill(Dict_project.dict_project, user.skills, user.last_users)

            # если функция подбора не нашла подходящих проектов, она возвращает юзера в меню
            if result == None:
                markup = menu_keyboard()
                await message.answer('Никого нет для вас',
                                     reply_markup=markup
                                     )
                await message.answer(menu_main_text)
                await Wait.menu_answer.set()

            # показывает подобранную анкету проекта
            else:
                key = result[0]
                value = result[1]
                user.last_users.append(key)
                project = Dict_project.dict_project[key]
                caption = project.show_anketa()
                markup = reaction_keyboard()
                await message.answer(f'{caption}',
                                     reply_markup=markup
                                     )
                await Wait.recommendations.set()


        elif chat_id in Dict_project.dict_project:

            project = Dict_project.dict_project[chat_id]
            caption_flag = project.show_anketa()
            word_to_find = project.skills
            result = get_random_user_with_matching_skill(Dict_users.dict_users, project.skills, project.last_users)

            # если функция подбора не нашла подходящих участников, она возвращает юзера в меню
            if result == None:
                markup = menu_keyboard()
                await message.answer('Никого нет для вас',
                                     reply_markup=markup
                                     )

                await message.answer(menu_main_text)
                await Wait.menu_answer.set()

            # показывает подобранную анкету участника
            else:
                key = result[0]
                value = result[1]
                project.last_users.append(key)

                user = Dict_users.dict_users[key]
                caption = user.show_anketa()
                markup = reaction_keyboard()
                await message.answer(f'{caption}',
                                     reply_markup=markup
                                     )
                await Wait.recommendations.set()

    # возвращение в меню
    if message.text == 'Вернуться назад':
        markup = menu_keyboard()
        await message.answer(menu_main_text,
                             reply_markup=markup
                             )
        await Wait.menu_answer.set()


executor.start_polling(dp)