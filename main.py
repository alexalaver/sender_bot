from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from databasa import Data
from telethon.sync import TelegramClient
import config as cfg
import logging
import functions as fnc

bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Data("192.168.1.37", "5432", "sender", "sender_user", "sender_pass")

logging.basicConfig(level=logging.INFO)

class AddNumberPhone(StatesGroup):
    addnumber_1 = State()
    addnumber_2 = State()
    addnumber_3 = State()
    addnumber_4 = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        username = message.from_user.username
        if(not db.check_user(user_id)):
            db.add_user(user_id, first_name, username)
        await message.answer("Добро пожаловать!")

@dp.message_handler(commands=['addadmin'])
async def add_admin_user(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if db.select_admin(user_id) > 0:
            select_adm_id = int(message.text.split()[1])
            if(not db.check_user(select_adm_id)):
                await message.answer("Пользователь не найден!")
            elif db.check_user(select_adm_id):
                db.add_admin(select_adm_id)
                await message.answer(f"Вы успешно назначили нового {fnc.nick_with_link('администратора' ,select_adm_id)}")
                await dp.bot.send_message(select_adm_id, "Вас назначили администратором.")
            else:
                await message.answer("Вы неправильно ввели команду, формат команды - /addadmin id")
        else:
            await message.answer("Вам не доступна данная команда!")

@dp.message_handler(commands=['addaccount'])
async def addaccount(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        print("Hello")
        if db.select_admin(user_id) > 0:
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            markup.add("Отменить")
            await message.answer("Для начала введите api_id: ", reply_markup=markup)
            await AddNumberPhone.addnumber_1.set()
            db.delete_cashe_create(user_id)

@dp.message_handler(state=AddNumberPhone.addnumber_1)
async def addnumber_1_text(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        api_id = message.text
        if message.text == "Отменить":
            db.delete_cashe_create(user_id)
            await state.reset_state()
            await message.answer("Вы отменили добавление аккаунта.", reply_markup=types.ReplyKeyboardRemove())
        else:
            db.add_cashe_create(user_id, api_id)
            await message.answer("Информация получена, введите api_hash: ")
            await AddNumberPhone.addnumber_2.set()

@dp.message_handler(state=AddNumberPhone.addnumber_2)
async def addnumber_2_text(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        api_hash = message.text
        if message.text == "Отменить":
            db.delete_cashe_create(user_id)
            await state.reset_state()
            await message.answer("Вы отменили добавление аккаунта.", reply_markup=types.ReplyKeyboardRemove())
        else:
            db.update_cashe_create_hash(user_id, api_hash)
            await message.answer("Информация получена, введите номер телефона: ")
            await AddNumberPhone.addnumber_3.set()

@dp.message_handler(state=AddNumberPhone.addnumber_3)
async def addnumber_3_text(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        number_phone = message.text
        if message.text == "Отменить":
            db.delete_cashe_create(user_id)
            await state.reset_state()
            await message.answer("Вы отменили добавление аккаунта.", reply_markup=types.ReplyKeyboardRemove())
        else:
            try:
                db.update_cashe_create_number_phone(user_id, number_phone)
                cashe_create = db.select_cashe_create(user_id)
                api_id = cashe_create[0]
                api_hash = cashe_create[1]
                number = cashe_create[2]
                telethon_client = TelegramClient(number, api_id, api_hash)
                await telethon_client.send_code_request(number)
                await message.answer("На ваш телеграмм аккаунт отправлен код, введите: ")
                await state.finish()
            except Exception as es:
                await message.answer("Произошла ошибка, номер ведён неверно, либо на данный номер не зарегестрирован аккаунт в телеграмме!", reply_markup=types.ReplyKeyboardRemove())
                db.delete_cashe_create(user_id)
                await state.reset_state()

@dp.message_handler()
async def texts(message: types.Message):
    if message.text == 't':
        await message.answer(db.select_cashe_create(3424))

if __name__ == "__main__":
    executor.start_polling(dp)
