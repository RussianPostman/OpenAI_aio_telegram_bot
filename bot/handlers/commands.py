from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage

from bot.handlers.keyboards.user_kb import START_BOARD


async def start(message: types.Message):
    """
    Хендлер для команды /start
    :param message:
    """
    return await message.answer(
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
