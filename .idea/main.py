from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token="7855213389:AAFdmLy9DS1HJ39MuPaO48XKogYtvuKihOw")
dp = Dispatcher(bot, storage=MemoryStorage())

dict_users = dict()

menu_main_text = "1. Заполнить анкету заново\n 2. Выключить анкету\n 3. Моя анкета\n 4. Искать проект"


class Wait(StatesGroup):
    join_team = State()
    find_team = State()
    name = State()
    age = State()
    city = State()
    text = State()
    yes_no = State()
    edit_anket = State()
    menu_answer = State()
    my_anketa_answer = State()
    change_text = State()
    change_photo = State()
    delete_confirm = State()
    anketa_reaction = State()

def show_anketa(sost, name, age, city, text):
    if sost == True:
        return f'{name}\n{age}\n{city}\n{text}\nИщет проект'
    else:
        return f'{name}\n{age}\n{city}\n{text}\nИщет команду'

@dp.message_handler(commands='start', state= '*')
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Вступить в комманду", "Найти комманду"]
    markup.add(*buttons)
    await bot.send_message(message.chat.id, 'Привет, я бот для поиска IT команды \n Выбери что хочешь сделать:', reply_markup=markup)
    await Wait.join_team.set()

@dp.message_handler(state= Wait.join_team)
async def start(message: types.Message, state: FSMContext):
    await state.update_data(join_team = True)
    await state.update_data(find_team=False)
    await bot.send_message(message.chat.id, 'Отлично! \n ВВеди свое ФИО')
    await Wait.name.set()



@dp.message_handler(state= Wait.name)
async def start(message: types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    await bot.send_message(message.chat.id, 'Отлично! \n Теперь введи возраст')
    await Wait.age.set()

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
    await message.answer("Напишите свой город")
    await Wait.city.set()

@dp.message_handler(state = Wait.city)
async def city(message: types.Message, state: FSMContext):
    if len(message.text) > 30:
        await message.answer("Слишком длинный город")
        return

    await state.update_data(city = message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Оставить пустым")

    await message.answer("Расскажи о своих навыках и опыте в проектах", reply_markup = keyboard)
    await Wait.text.set()

@dp.message_handler(state = Wait.text)
async def text(message: types.Message, state: FSMContext):
    global dict_users
    await state.update_data(text = message.text)

    data = await state.get_data()
    d = list(data.values())
    dict_users[message.from_user.id] = [d[0], d[1], d[2], d[3]]

    caption = show_anketa(d[0], d[2], d[3], d[4], d[5])
    await message.answer(f"Вот твоя анкета")
    await message.answer(f"{caption}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, )
    buttons = ["Заполнить анкету заново", "Выключить анкету", "Моя анкета", "Искать проект"]
    markup.add(*buttons)
    await message.answer(menu_main_text, reply_markup=markup)
    print(dict_users)
    await Wait.menu_answer.set()


@dp.message_handler(state= Wait.menu_answer)
async def menu_answer(message: types.Message, state: FSMContext):
    if message.text == '1':
        pass
    if message.text == '2':
        pass
    if message.text == '3':
        global dict_users
        data = await state.get_data()
        d = list(data.values())
        caption = show_anketa(d[0], d[2], d[3], d[4], d[5])
        await message.answer(f"Вот твоя анкета")
        await message.answer(f"{caption}")
        await Wait.menu_answer.set()






executor.start_polling(dp)


