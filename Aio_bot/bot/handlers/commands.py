"""
Хендлеры команд бота
"""
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage

from sqlalchemy.orm import sessionmaker

import bot.handlers.keyboards.user_kb as ukb
import bot.db as db


async def chat_mode(
    message: types.Message,
    session_maker: sessionmaker,
    state: FSMContext,
    ):
    """
    Хендлер для команды /mode
    """
    await state.clear()
    prompts = await db.get_public_prompts(session_maker)
    await SendMessage(
        chat_id=message.from_user.id,
        text='Выбирите модификацию чата',
        reply_markup=ukb.gen_prompts_kb(prompts)
    )


async def dialogue_list(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker,
    ):
    await state.clear()
    user_id = message.from_user.id
    dial_list = await db.get_user_dialogues(
        user_id,
        session_maker
        )
    await message.answer(
        text='Ваши диалоги',
        reply_markup=ukb.gen_dialogues_kb(dial_list)
        )
    



# функция выхода из машины состояний
async def censel_hendler(
        message: types.Message,
        state: FSMContext,
        ):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    # return await SendMessage(
    #     text='Дейстаия отменены',
    #     chat_id=message.from_user.id,
    #     reply_markup=START_BOARD)
