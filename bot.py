import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, ParseMode
from handlers.solve_test import register_handlers_solve_test
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers.greet import register_handlers_greet
from handlers.add_test import register_handlers_add_test
from handlers.common import register_handlers_common
from dotenv import load_dotenv, find_dotenv


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/solve_test", description="Решить тест"),
        BotCommand(command="/add_test", description="Создать тест"),
        BotCommand(command="/help", description="Список комманд"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    load_dotenv(find_dotenv())
    NIKITA_BOT_TOKEN = os.environ.get("NIKITA_BOT_TOKEN")

    bot = Bot(NIKITA_BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_common(dp)
    register_handlers_greet(dp)
    register_handlers_solve_test(dp)
    register_handlers_add_test(dp)

    await set_commands(bot)

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
