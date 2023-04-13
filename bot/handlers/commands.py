from typing import Any
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage

from sqlalchemy.orm import sessionmaker

from bot.handlers.keyboards.user_kb import START_BOARD, START_BOARD_LITE
from bot.db import get_user_dialogues


async def start(
    message: types.Message,
    session_maker: sessionmaker, 
    **data: dict[str, Any],
    ):
    """
    Хендлер для команды /start
    :param message:
    """
    user_id = message.from_user.id
    if len(await get_user_dialogues(user_id, session_maker)) < 1:
        return await message.answer(
            'Started',
            reply_markup=START_BOARD_LITE)


    await message.answer(
        'Started', reply_markup=START_BOARD)


# функция выхода из машины состояний
async def censel_hendler(
        message: types.Message,
        state: FSMContext,
        ):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    return await SendMessage(
        text='Дейстаия отменены',
        chat_id=message.from_user.id,
        reply_markup=START_BOARD)
