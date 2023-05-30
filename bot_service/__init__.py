# bot_service/__init__.py

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_service import config

bot = Bot(token=config.TREVOR_BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Импортирование обработчиков для активации
from bot_service import handlers
from bot_service import commands