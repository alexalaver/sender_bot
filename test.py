
import logging
from aiogram import Bot, Dispatcher, types, executor
from telethon.sync import TelegramClient

# Настройки Aiogram
bot_token = 'YOUR_BOT_TOKEN'
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# Настройки Telethon
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
session_name = 'name'
telethon_client = TelegramClient(number, api_id, api_hash)

# Инициализация логгера
logging.basicConfig(level=logging.INFO)

# Обработчик команды /send_message
@dp.message_handler(commands=['send_message'])
async def send_message(message: types.Message):
    await message.answer("Введите ваш номер телефона (в формате +1234567890):")
    await dp.register_next_step_handler(message, process_phone)

async def process_phone(message: types.Message):
    phone = message.text.strip()
    await telethon_client.start()
    try:
        await telethon_client.send_code_request(phone)
        await message.answer("На ваш номер отправлен код подтверждения. Пожалуйста, введите код:")
        await dp.register_next_step_handler(message, process_code)
    except Exception as e:
        await message.answer(f"Ошибка при отправке кода подтверждения: {str(e)}")

async def process_code(message: types.Message):
    user_username = ['@alexalaver', '@developadm']
    message_text = 'Добрый вечер'
    await telethon_client.start()
    for users in user_username:
        user = await telethon_client.get_entity(users)
        await telethon_client.send_message(user, message_text)
    await telethon_client.disconnect()
    await message.answer("Сообщение успешно отправлено")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=None)
