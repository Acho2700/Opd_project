from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, InlineKeyboardButton, CallbackQuery
from aiogram.types import KeyboardButton, InlineKeyboardButton, CallbackQuery
from users_dict import Dict_users
from user_class import User
from group_class import Group
from project_dict import Dict_project
import random


bot = Bot(token="7855213389:AAFdmLy9DS1HJ39MuPaO48XKogYtvuKihOw")
dp = Dispatcher(bot, storage=MemoryStorage())


menu_main_text = "1. Добавить навык\n 2.Удалить навык\n 3. Выключить\Включить анкету\n 4. Моя анкета\n 5. Искать проект/участника"


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



def menu_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["1", "2", "3", "4", "5"]
    markup.add(*buttons)
    return markup

def reaction_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Лайк", "Дизлайк", "Вернуться назад"]
    markup.add(*buttons)
    return markup


#F обработчик команды старт, приветствие и выбор действия
@dp.message_handler(commands='start', state= '*')
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Вступить в комманду", "Найти комманду"]
    markup.add(*buttons)
    await bot.send_message(message.chat.id, 'Привет, я бот для поиска IT команды \n Выбери что хочешь сделать:', reply_markup=markup)
    await Wait.group_or_user.set()

@dp.message_handler(state= Wait.group_or_user)
async def group_or_user(message: types.Message, state: FSMContext):
    if message.text == "Вступить в комманду":
        await state.update_data(join_team=True)
        await bot.send_message(message.chat.id, 'Отлично! \n Введи свое ФИО')
        await Wait.name.set()
    elif message.text == "Найти комманду":
        await state.update_data(join_team=False)
        await bot.send_message(message.chat.id, 'Отлично! \n Введи Название проекта')
        await Wait.name_project.set()



#F Ввод и занесение имени в анкету ( в будущем в бд )
@dp.message_handler(state= Wait.name)
async def name(message: types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    await bot.send_message(message.chat.id, 'Отлично! \n Теперь введи возраст')
    await Wait.age.set()

@dp.message_handler(state= Wait.name_project)
async def name_project(message: types.Message, state: FSMContext):
    await state.update_data(name_project = message.text)
    await bot.send_message(message.chat.id, 'Отлично! \n Теперь расскажи о проекте')
    await Wait.text_project.set()


#F Ввод и занесение возраста в анкету ( в будущем в бд )
@dp.message_handler(state = Wait.age)
async def age(message: types.Message, state: FSMContext):
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


#F Ввод и занесение описания в анкету ( в будущем в бд )
@dp.message_handler(state = Wait.text)
async def text(message: types.Message, state: FSMContext):
    await state.update_data(text = message.text)

    data = await state.get_data()
    print(data)
    join_team = data["join_team"]
    name = data["name"]
    age = data["age"]
    skills = data["text"].replace(' ', '').split(',')
    chat_id = message.chat.id

    user = User(name, age, skills, True)
    Dict_users.dict_users[chat_id] = user
    caption = user.show_anketa()
    print(user.__dict__)
    await message.answer(f"Вот твоя анкета")
    await message.answer(f"{caption}")
    markup = menu_keyboard(message)
    await message.answer(menu_main_text, reply_markup=markup)
    await Wait.menu_answer.set()


@dp.message_handler(state = Wait.text_project)
async def text_project(message: types.Message, state: FSMContext):
    await state.update_data(text_project = message.text)

    data = await state.get_data()
    join_team = data["join_team"]
    name_project = data["name_project"]
    text = data["text_project"]
    #тут должны еще быть скиллы которые нейронка определяет
    chat_id = message.chat.id

    project = Group(name_project, text, None, True)
    Dict_project.dict_project[chat_id] = project
    caption = project.show_project()
    print(project.__dict__)
    await message.answer(f"Вот анкета твоего проекта")
    await message.answer(f"{caption}")
    markup = menu_keyboard(message)
    await message.answer(menu_main_text, reply_markup=markup)
    await Wait.menu_answer.set()


@dp.callback_query_handler(text='btn1')
async def process_callback_button1(call: types.CallbackQuery):
    print('1')
    await call.message.answer('Нажата первая кнопка!')
    print(call.message.message_id)
    await call.answer()




#F ответ на выбранный пользователем пункт меню ( ответ менюшки ) (менюшки пока нет))))
@dp.message_handler(state= Wait.menu_answer)
async def menu_answer(message: types.Message, state: FSMContext):
    chat_id = message.chat.id


    if message.text == '1':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="btn1"))
        await message.answer('Введи навык для добавления', reply_markup=keyboard)
        # await Wait.add_skill.set()


    if message.text == '2':
        await message.answer('Введи навык для удаления')
        await Wait.del_skill.set()


    if message.text == '3':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = ["Нет", "Да"]
        markup.add(*buttons)
        chat_id = message.chat.id
        if chat_id in Dict_users.dict_users:
            user = Dict_users.dict_users[chat_id]
            if user.in_active:
                await message.answer('Вы уверены что хотите выключить анкету?', reply_markup=markup)
                await Wait.anketa_activ.set()
            else:
                await message.answer('Вы уверены что хотите включить анкету?', reply_markup=markup)
                await Wait.anketa_activ.set()

        if chat_id in Dict_project.dict_project:
            project = Dict_project.dict_project[chat_id]
            if project.in_active:
                await message.answer('Вы уверены что хотите выключить анкету проекта?', reply_markup=markup)
                await Wait.anketa_activ.set()
            else:
                await message.answer('Вы уверены что хотите включить анкету проекта?', reply_markup=markup)
                await Wait.anketa_activ.set()

    if message.text == '4':
        if chat_id in Dict_users.dict_users:
            user = Dict_users.dict_users[chat_id]
            caption = user.show_anketa()
            markup = menu_keyboard(message)
            await message.answer(f"Вот твоя анкета")
            print(user.__dict__)
            await message.answer(f"{caption}", reply_markup=markup)
            await message.answer(menu_main_text)

        if chat_id in Dict_project.dict_project:
            user = Dict_project.dict_project[chat_id]
            caption = user.show_project()
            markup = menu_keyboard(message)
            await message.answer(f"Вот твой проект")
            print(user.__dict__)
            await message.answer(f"{caption}", reply_markup=markup)
            await message.answer(menu_main_text)

    if message.text == '5':
        markup = reaction_keyboard(message)
        await message.answer('Подбираем анкеты для вас...', reply_markup=markup)

        if chat_id in Dict_users.dict_users:
            user = Dict_users.dict_users[chat_id]
            result = get_random_user_with_matching_skill(Dict_project.dict_project, user.skills)
            if result == None:
                markup = menu_keyboard(message)
                await message.answer('Никого нет для вас', reply_markup=markup)
                await message.answer(menu_main_text)
                await Wait.menu_answer.set()
                return
            key = result[0]
            value = result[1]

            project = Dict_project.dict_project[key]
            caption = project.show_project()
            await message.answer(f'{caption}')

        if chat_id in Dict_project.dict_project:
            project = Dict_project.dict_project[chat_id]
            result = get_random_user_with_matching_skill(Dict_users.dict_users, project.skills)
            if result == None:
                markup = menu_keyboard(message)
                await message.answer('Никого нет для вас', reply_markup=markup)
                await message.answer(menu_main_text)
                await Wait.menu_answer.set()
                return
            key = result[0]
            value = result[1]

            user = Dict_users.dict_users[key]
            caption = user.show_anketa()
            await message.answer(f'{caption}')

        await Wait.recommendations.set()


@dp.message_handler(state= Wait.add_skill)
async def add_skill(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = None
    if chat_id in Dict_users.dict_users:
        user = Dict_users.dict_users[chat_id]

    if chat_id in Dict_project.dict_project:
        user = Dict_project.dict_project[chat_id]

    user.add_skill(message.text)
    await message.answer('Навык успешно добавлен!')
    markup = menu_keyboard(message)
    await message.answer(menu_main_text, reply_markup=markup)
    await Wait.menu_answer.set()

@dp.message_handler(state= Wait.del_skill)
async def del_skill(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = None
    if chat_id in Dict_users.dict_users:
        user = Dict_users.dict_users[chat_id]

    if chat_id in Dict_project.dict_project:
        user = Dict_project.dict_project[chat_id]

    user.delete_skill(message.text)
    markup = menu_keyboard(message)
    await message.answer('Навык успешно удалён!')
    await message.answer(menu_main_text, reply_markup=markup)
    await Wait.menu_answer.set()

@dp.message_handler(state= Wait.anketa_activ)
async def anketa_activ(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = None
    if chat_id in Dict_users.dict_users:
        user = Dict_users.dict_users[chat_id]


    if chat_id in Dict_project.dict_project:
        user = Dict_project.dict_project[chat_id]

    check = user.in_active

    if message.text == 'Да' and check:
        user.activ_status()
        await message.answer('Ваша анкета больше не активна')
        markup = menu_keyboard(message)
        await message.answer(menu_main_text, reply_markup=markup)
        await Wait.menu_answer.set()
    elif message.text == 'Да' and check == False:
        user.activ_status()
        await message.answer('Ваша анкета снова активна')
        markup = menu_keyboard(message)
        await message.answer(menu_main_text, reply_markup=markup)
        await Wait.menu_answer.set()
    elif message.text == 'Нет':
        markup = menu_keyboard(message)
        await message.answer(menu_main_text, reply_markup=markup)
        await Wait.menu_answer.set()




def get_random_user_with_matching_skill(user_dict, skill_list):
    # Фильтруем ключи, у которых хотя бы одна строка совпадает с skills
    # matching_users = {key: user for key, user in user_dict.items() if any(skill in user.skills for skill in skill_list)}
    matching_users = {}
    for key, user in user_dict.items():
        flag = any(skill == skill2 for skill in skill_list for skill2 in user.skills)
        if flag:
            matching_users[key] = user
    # Если есть совпадения, выбираем случайный ключ и значение
    if matching_users:
        random_key = random.choice(list(matching_users.keys()))
        return random_key, matching_users[random_key]
    return None




@dp.message_handler(state= Wait.recommendations)
async def recommendations(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == 'Дизлайк' or message.text == 'Лайк':
        if chat_id in Dict_users.dict_users:
            user = Dict_users.dict_users[chat_id]
            caption_flag = user.show_anketa()
            result = get_random_user_with_matching_skill(Dict_project.dict_project, user.skills)
            if result == None:
                markup = menu_keyboard(message)
                await message.answer('Никого нет для вас', reply_markup=markup)
                await message.answer(menu_main_text)
                await Wait.menu_answer.set()
                return
            key = result[0]
            value = result[1]

            project = Dict_project.dict_project[key]
            caption = project.show_project()
            markup = reaction_keyboard(message)
            await message.answer(f'{caption}', reply_markup=markup)
            await Wait.recommendations.set()


        if chat_id in Dict_project.dict_project:

            project = Dict_project.dict_project[chat_id]
            caption_flag = project.show_project()
            word_to_find = project.skills
            result = get_random_user_with_matching_skill(Dict_users.dict_users, project.skills)
            if result == None:
                markup = menu_keyboard(message)
                await message.answer('Никого нет для вас', reply_markup=markup)
                await message.answer(menu_main_text)
                await Wait.menu_answer.set()
                return

            key = result[0]
            value = result[1]

            user = Dict_users.dict_users[key]
            caption = user.show_anketa()
            markup = reaction_keyboard(message)
            await message.answer(f'{caption}', reply_markup=markup)
            await Wait.recommendations.set()

        if message.text == 'Лайк':
            markup = reaction_keyboard(message)
            await bot.send_message(chat_id= key, text= 'Вы понравились данному пользователю:', reply_markup=markup)
            await bot.send_message(chat_id= key, text= f'{caption_flag}', reply_markup=markup)
            await Wait.recommendations.set()


    if message.text == 'Вернуться назад':
        markup = menu_keyboard(message)
        await message.answer(menu_main_text, reply_markup=markup)
        await Wait.menu_answer.set()





executor.start_polling(dp)


