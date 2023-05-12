"""
Файл запуска бота
"""
import os
import asyncio
import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy import URL

from bot.handlers import register_user_commands
from bot.middleweres.register_check import RegisterCheck
import bot.settings as sett
from bot.db import create_async_engine, get_session_maker
from bot.on_start.set_db_info import on_start


load_dotenv()


TELEGRAM_TOKEN = os.getenv('TOKEN')


async def main():
    logging.basicConfig(level=logging.DEBUG)
    commands_for_bot = []

    # устанавливаем комманды
    for cmd in sett.bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    dp = Dispatcher(storage=RedisStorage(redis=sett.redis))
    bot = Bot(TELEGRAM_TOKEN)
    await bot.set_my_commands(commands=commands_for_bot)

    # регистрируем БД
    postgres_url = URL.create(
        drivername="postgresql+asyncpg",
        username=sett.POSTGRES_USER,
        host=sett.POSTGRES_HOST,
        database=sett.POSTGRES_DB,
        port=sett.POSTGRES_PORT,
        password=sett.POSTGRES_PASSWORD
    )

    # оегистрируем мидлвари
    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    register_user_commands(dp)

    # выполняем ф-цию при старте
    await on_start(session_maker)

    #### вот это интересная штука, нужна при дебаге, но не всегда. 
    # await redis.flushdb() # если это разкомментировать, чистит редис при каждом перезапуске, иногда полезно

    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt,):
        print('Bot stoped')
