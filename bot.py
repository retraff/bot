import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

# Загружаем токен бота и ID менеджера из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_CHAT_ID = int(os.getenv("8110796568"))  # сюда вставляем chat_id менеджера

if not BOT_TOKEN or not MANAGER_CHAT_ID:
    raise ValueError("Не найден BOT_TOKEN или MANAGER_CHAT_ID в .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Словарь для отслеживания, что пользователь написал имя
user_states = {}

# Команда /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply(
        "Привет! 👋 Ты попал туда, где труд реально ценят и оплачивают достойно.\n"
        "Напиши своё имя — менеджер свяжется с тобой с 15:00 до 21:00."
    )
    # Отмечаем, что ждем имя от пользователя
    user_states[message.from_user.id] = "waiting_name"

# Обработка сообщений (имя пользователя)
@dp.message_handler()
async def handle_name(message: types.Message):
    user_id = message.from_user.id

    if user_states.get(user_id) == "waiting_name":
        name = message.text.strip()
        username = message.from_user.username or "Не указан"

        # Отправляем менеджеру
        await bot.send_message(
            MANAGER_CHAT_ID,
            f"Новый пользователь:\nИмя: {name}\nUsername: @{username}"
        )

        # Отправляем пользователю подтверждение
        await message.reply(f"Отлично, {name}! 🚀 Жди сообщение от менеджера в ближайшее время.")

        # Убираем состояние ожидания
        user_states.pop(user_id)
    else:
        await message.reply("Чтобы начать, нажми /start")

if __name__ == "__main__":
    asyncio.run(dp.start_polling())
