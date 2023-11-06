from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import logging
import asyncio
import config as cfg

bot = Bot(token=cfg.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

telethon_client = TelegramClient(StringSession(), cfg.API_ID,
                                 cfg.API_HASH)  # Обратите внимание, что StringSession должен быть пустым

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Username чата для отслеживания
CHAT_USERNAME = "avitologpro1"  # Используйте username чата без "@"

# Словарь для отслеживания уже отправленных сообщений
sent_messages_users = set()

# Флаг для контроля состояния отслеживания
is_tracking = False


@dp.message_handler(commands=['start_tracking'])
async def start_tracking_command(message: types.Message):
    global is_tracking
    if not is_tracking:
        is_tracking = True
        await message.answer("Отслеживание сообщений активировано.")
    else:
        await message.answer("Отслеживание сообщений уже активировано.")


@dp.message_handler(commands=['stop_tracking'])
async def stop_tracking_command(message: types.Message):
    global is_tracking
    if is_tracking:
        is_tracking = False
        await message.answer("Отслеживание сообщений остановлено.")
    else:
        await message.answer("Отслеживание сообщений уже остановлено.")


# Обработка новых сообщений через Telethon
@telethon_client.on(events.NewMessage(chats=[CHAT_USERNAME]))
async def handle_new_message(event):
    if not is_tracking:
        return

    sender = await event.get_sender()
    user_id = sender.id

    if user_id not in sent_messages_users:
        sent_messages_users.add(user_id)  # Добавляем пользователя в множество

    for user_id in list(sent_messages_users):  # Перебираем множество пользователей
        try:
            # Отправляем сообщение от аккаунта пользователя через Telethon
            await telethon_client.send_message(user_id, "Привет.")
            await asyncio.sleep(5)  # Небольшая задержка для предотвращения ограничения скорости
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
        finally:
            sent_messages_users.remove(user_id)  # Удаляем пользователя из множества после попытки отправки


async def main():
    await telethon_client.start()
    # Запускаем polling в отдельной задаче
    dp_task = asyncio.ensure_future(dp.start_polling())
    # Ждем завершения обеих задач
    await asyncio.gather(dp_task, telethon_client.run_until_disconnected())


if __name__ == "__main__":
    asyncio.run(main())
