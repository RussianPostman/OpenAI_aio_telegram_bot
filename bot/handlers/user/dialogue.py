from pprint import pprint
from typing import Any
from httpx import Response, Timeout

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import Bot, types
from sqlalchemy.orm import sessionmaker

# from bot.handlers.keyboards.user_kb import DIALOGUE_KB
from bot import settings as sett
from bot.db import create_dialogue, get_dialogue, get_dial_by_id, \
    create_message
from bot import openai_async
from ._tools import generate_payload, get_api_key, check_tokens_buffer, \
    add_message
from bot.handlers.states import DialogueStates
from bot.handlers.keyboards.user_kb import UserDialoguesCallback, TranscribeCD


async def new_GPT_3(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
        ):
    await state.clear()
    msg = await message.answer(
        'Секунду...',
        )
    user_id = message.from_user.id
    last_dialogue = await create_dialogue(user_id, session_maker, 'gpt-3.5-turbo')
    await state.set_state(DialogueStates.dialogue)
    await generate_payload(state, last_dialogue, session_maker)
    await state.update_data(api_key=sett.OPENAI_API_KEY)
    await msg.edit_text(
        f'Диалог {last_dialogue.name} создан.',
        )
    

async def new_GPT_4(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
        ):
    await state.clear()
    msg = await message.answer(
        'Секунду...',
        )
    user_id = message.from_user.id
    last_dialogue = await create_dialogue(user_id, session_maker, 'gpt-4')
    # await sett.redis.set(name=f'{user_id}_last', value=last_dialogue.name)
    await state.set_state(DialogueStates.dialogue)
    await generate_payload(state, last_dialogue, session_maker)
    await state.update_data(api_key=sett.GPT4_API_KEY)
    await msg.edit_text(
        f'Диалог {last_dialogue.name} создан.',
        )


async def open_dialogue(
        query: types.CallbackQuery,
        callback_data: UserDialoguesCallback,
        state: FSMContext,
        session_maker: sessionmaker
    ):
    dial = await get_dial_by_id(callback_data.dial_id, session_maker)
    await state.set_state(DialogueStates.dialogue)
    await generate_payload(state, dial, session_maker)
    await get_api_key(dial, state)
    return await SendMessage(
        text=f'Диалог {dial.name} открыт',
        chat_id=query.from_user.id,
        )


async def dialogue(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
        ):
    data = await add_message(message.text, "user", state)
    await create_message(
        data['dialogue_id'],
        role='user',
        text=message.text,
        session_maker=session_maker
        )
    await check_tokens_buffer(state, session_maker)

    payload = data.get('payload')
    msg = await SendMessage(
        text=f'Запрос к {payload.get("model")} отправлен',
        chat_id=message.from_user.id,
    )
    completion: Response = await openai_async.chat_complete(
        api_key=data.get('api_key'),
        timeout=60,
        payload=payload,
        )
    try:
        chat_response = completion.json()["choices"][0]["message"]['content']
    except KeyError:
        return await msg.edit_text('Что-то пошло не так')

    data = await add_message(chat_response, "assistant", state)
    await msg.edit_text(chat_response)
    await create_message(
        data['dialogue_id'],
        role='assistant',
        text=chat_response,
        session_maker=session_maker
        )
    await check_tokens_buffer(state, session_maker)
    payload = data.get('payload')
    msg = await SendMessage(
        text=f'Запрос к {payload.get("model")} отправлен',
        chat_id=message.from_user.id,
    )


async def transcribe_to_gpt(
        query: types.CallbackQuery,
        callback_data: TranscribeCD,
        state: FSMContext,
        session_maker: sessionmaker,
        **data: dict[str, Any],
    ):
    mess_id = callback_data.message_id
    chat_id = query.from_user.id
    bot: Bot = data['bot']

    mess = await bot.forward_message(chat_id, chat_id, mess_id)
    cache_data = await add_message(mess.text, "user", state)
    payload = cache_data.get('payload')
    await create_message(
        cache_data['dialogue_id'],
        role='user',
        text=mess.text,
        session_maker=session_maker
        )
    await mess.delete()
    await check_tokens_buffer(state, session_maker)
    msg = await SendMessage(
        text=f'Запрос к {payload.get("model")} отправлен',
        chat_id=query.from_user.id,
    )
    completion: Response = await openai_async.chat_complete(
        api_key=cache_data.get('api_key'),
        timeout=60,
        payload=payload,
        )
    try:
        chat_response = completion.json()["choices"][0]["message"]['content']
    except KeyError:
        return await msg.edit_text('Что-то пошло не так')
    
    cache_data = await add_message(chat_response, "assistant", state)
    await msg.edit_text(chat_response)
    await create_message(
        cache_data['dialogue_id'],
        role='assistant',
        text=chat_response,
        session_maker=session_maker
        )
    await check_tokens_buffer(state, session_maker)
    payload = cache_data.get('payload')
    # msg = await SendMessage(
    #     text=f'Запрос к {payload.get("model")} отправлен',
    #     chat_id=query.from_user.id,
    # )

    