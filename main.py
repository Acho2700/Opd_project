from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from users_dict import Dict_users
from user_class import User


bot = Bot(token="7855213389:AAFdmLy9DS1HJ39MuPaO48XKogYtvuKihOw")
dp = Dispatcher(bot, storage=MemoryStorage())


menu_main_text = "1. Добавить навык\n 2.Удалить навык\n 3. Выключить\Включить анкету\n 4. Моя анкета\n 5. Искать проект"


class Wait(StatesGroup):
    join_team = State()
    name = State()
    age = State()
    text = State()
    yes_no = State()
    edit_anket = State()
    menu_answer = State()
    add_skill = State()
    del_skill = State()
    anketa_activ = State()
    no_activ = State()



def menu_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["1", "2", "3", "4", "5"]
    markup.add(*buttons)
    return markup


#F обработчик команды старт, приветствие и выбор действия
@dp.message_handler(commands='start', state= '*')
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Вступить в комманду", "Найти комманду"]
    markup.add(*buttons)
    await bot.send_message(message.chat.id, 'Привет, я бот для поиска IT команды \n Выбери что хочешь сделать:', reply_markup=markup)
    await Wait.join_team.set()

#F Ввод и занесение статуса поиска в анкету ( в будущем в бд )
@dp.message_handler(state= Wait.join_team)
async def join_team(message: types.Message, state: FSMContext):
    await state.update_data(join_team = True)
    await bot.send_message(message.chat.id, 'Отлично! \n ВВеди свое ФИО')
    await Wait.name.set()


#F Ввод и занесение имени в анкету ( в будущем в бд )
@dp.message_handler(state= Wait.name)
async def name(message: types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    await bot.send_message(message.chat.id, 'Отлично! \n Теперь введи возраст')
    await Wait.age.set()

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
    skills = data["text"].split(',')
    chat_id = message.chat.id
    if join_team:
        user = User(name, age, skills, True)
    Dict_users.dict_users[chat_id] = user
    caption = user.show_anketa()
    await message.answer(f"Вот твоя анкета")
    await message.answer(f"{caption}")
    markup = menu_keyboard(message)
    await message.answer(menu_main_text, reply_markup=markup)
    await Wait.menu_answer.set()



#F ответ на выбранный пользователем пункт меню ( ответ менюшки ) (менюшки пока нет))))
@dp.message_handler(state= Wait.menu_answer)
async def menu_answer(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = Dict_users.dict_users[chat_id]

    if message.text == '1':
        await message.answer('Введи навык для добавления')
        await Wait.add_skill.set()


    if message.text == '2':
        await message.answer('Введи навык для удаления')
        await Wait.del_skill.set()


    if message.text == '3':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = ["Нет", "Да"]
        markup.add(*buttons)
        chat_id = message.chat.id
        user = Dict_users.dict_users[chat_id]
        if user.in_active:
            await message.answer('Вы уверены что хотите выключить анкету?', reply_markup=markup)
            await Wait.anketa_activ.set()
        else:
            await message.answer('Вы уверены что хотите включить анкету?', reply_markup=markup)
            await Wait.anketa_activ.set()


    if message.text == '4':
        caption = user.show_anketa()
        await message.answer(f"Вот твоя анкета")
        await message.answer(f"{caption}")


    if message.text == '5':
        await message.answer("Подбираем проекты для вас...")
        pass
@dp.message_handler(state= Wait.add_skill)
async def add_skill(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = Dict_users.dict_users[chat_id]
    user.add_skill(message.text)
    await message.answer('Навык успешно добавлен!')
    await message.answer(menu_main_text)
    await Wait.menu_answer.set()

@dp.message_handler(state= Wait.del_skill)
async def del_skill(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = Dict_users.dict_users[chat_id]
    user.delete_skill(message.text)
    await message.answer('Навык успешно удалён!')
    await message.answer(menu_main_text)
    await Wait.menu_answer.set()

@dp.message_handler(state= Wait.anketa_activ)
async def anketa_activ(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = Dict_users.dict_users[chat_id]

    if message.text == 'Да' and user.in_active:
        user.activ_status()
        await message.answer('Ваша анкета больше не активна')
        markup = menu_keyboard(message)
        await message.answer(menu_main_text, reply_markup=markup)
        await Wait.menu_answer.set()
    elif message.text == 'Да' and user.in_active == False:
        user.activ_status()
        await message.answer('Ваша анкета снова активна')
        markup = menu_keyboard(message)
        await message.answer(menu_main_text, reply_markup=markup)
        await Wait.menu_answer.set()
    elif message.text == 'Нет':
        markup = menu_keyboard(message)
        await message.answer(menu_main_text, reply_markup=markup)
        await Wait.menu_answer.set()


executor.start_polling(dp)


