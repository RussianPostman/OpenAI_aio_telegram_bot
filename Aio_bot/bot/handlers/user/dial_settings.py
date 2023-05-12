from pprint import pprint
from httpx import Response, Timeout

from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import types
from sqlalchemy.orm import sessionmaker
from bot.db.db_services.dialogues import update_dial_field

from bot.handlers.states import DialogueStates
from bot.handlers.keyboards.user_kb import gen_settings_kb, SettingsCallback
from bot.handlers.user._tools import validation


PARAMS_MESSAGES = {
    'temperature': '<b>Введите число от 0.1 до 2</b>',
    'top_p': '<b>Введите число от 0 до 2</b>',
    'n': '<b>Введите целое число от 1 до 10</b>',
    'presence_penalty': '<b>Введите число от -2.0 до 2.0</b>',
    'frequency_penalty': '<b>Введите число от -2.0 до 2.0</b>',
    'max_tokens': '<b>Введите целое число от 50 до 3000</b>'
}


async def dial_settings(
        message: types.Message,
        state: FSMContext,
        ):
    data: dict = await state.get_data()
    payload: dict = data.get('payload')
    text = (
        f"На данный момент в диалоге задействованна модель {payload.get('model')}"
        + " с параметрами: \n"
        + f"    temperature: {payload.get('temperature')}\n"
        + f"    top_p: {payload.get('top_p')}\n"
        + f"    n: {payload.get('n')}\n"
        + f"    max_tokens: {payload.get('max_tokens')}\n"
        + f"    presence_penalty: {payload.get('presence_penalty')}\n"
        + f"    frequency_penalty: {payload.get('frequency_penalty')}\n"
        + "Для внесения изменений используйте меню снизу\n"
        )

    await SendMessage(
        text=text,
        chat_id=message.from_user.id,
        reply_markup=gen_settings_kb(payload)
        )
    await state.set_state(DialogueStates.settings_menu)


async def settings_menu(
        query: types.CallbackQuery,
        callback_data: SettingsCallback,
        state: FSMContext,
        ):
    param = callback_data.param
    await state.set_state(DialogueStates.change_2)
    await state.update_data(param=param)
    await SendMessage(
        text=PARAMS_MESSAGES.get(param),
        chat_id=query.from_user.id,
        parse_mode="html"
        )


async def dial_change(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
        ):
    user_imput = message.text.strip()
    data = await state.get_data()
    payload = data.get('payload')
    param = data.get('param')
    valid_dt = None

    
    valid_dt = await validation(param, user_imput)
    print(valid_dt)

    if valid_dt:
        payload[param] = valid_dt
        await state.update_data(payload=payload)
        await update_dial_field(
            data.get('dialogue_id'),
            param,
            valid_dt,
            session_maker
            )
        await state.set_state(DialogueStates.settings_menu)
        await SendMessage(
            text='Данные изменены',
            chat_id=message.from_user.id,
            reply_markup=gen_settings_kb(payload)
            )
        pprint(payload)

    else:
        message.answer(
            'Не валидные данные, попробуйте ещё раз'
        )

