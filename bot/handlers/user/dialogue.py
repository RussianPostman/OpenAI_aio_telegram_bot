from pprint import pprint
from httpx import Response, Timeout

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import types
from sqlalchemy.orm import sessionmaker

from bot.handlers.keyboards.user_kb import DIALOGUE_KB
from bot import settings as sett # OPENAI_API_KEY, TIMEOUT, DEFOULT_PROMPT
from bot.db import create_dialogue, get_dialogue, get_user_dialogues, \
    create_message
from bot import openai_async
from ._tools import generate_payload


class DialogueStates(StatesGroup):
    """
    Состояния для диалога с GPT
    """
    dialogue = State()


async def new_dialogue(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
        ):
    await message.answer(
        'Создаём новый диалог',
        )
    user_id = message.from_user.id
    last_dialogue = await create_dialogue(user_id, session_maker)
    await sett.redis.set(name=f'{user_id}_last', value=last_dialogue.name)
    await state.set_state(DialogueStates.dialogue)
    await generate_payload(state, last_dialogue, session_maker)
    await message.answer(
        f'Диалог {last_dialogue.name} создан.',
        )


async def resume_dialogue(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
    ):
    iser_id = message.from_user.id
    dialogue_name = await sett.redis.get(name=f'{iser_id}_last')
    if dialogue_name:
        last_dialogue = await get_dialogue(
            iser_id, dialogue_name.decode("utf-8"), session_maker)
    else:
        dial_list = await get_user_dialogues(iser_id, session_maker)
        last_dialogue = dial_list[-1]
    
    await state.set_state(DialogueStates.dialogue)
    await generate_payload(state, last_dialogue, session_maker)
    await message.answer(
        f'Последний далог {last_dialogue.name} открыт.',
        )


async def dialogue(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
        ):
    data: list = await state.get_data()
    payload: list = data['payload']
    messages = payload.pop('messages')
    messages.append({"role": "user", "content": message.text})

    await create_message(
        data['dialogue_id'],
        role='user',
        text=message.text,
        session_maker=session_maker
        )

    payload['messages'] = messages

    await SendMessage(
        text='Запрос к gpt-3.5-turbo отправлен',
        chat_id=message.from_user.id,
        reply_markup=DIALOGUE_KB
    )
    completion: Response = await openai_async.chat_complete(
        api_key=sett.OPENAI_API_KEY,
        timeout=60,
        payload=payload,
        )
    
    pprint(completion.json())

    try:
        chat_response = completion.json()["choices"][0]["message"]['content']
    except KeyError:
        message.answer('Что-то пошло не так')
        return

    messages = payload.pop('messages')
    messages.append({"role": "assistant", "content": chat_response})
    payload['messages'] = messages
 
    await state.update_data(payload=payload)
    await SendMessage(
        text=chat_response,
        chat_id=message.from_user.id,
    )

    await create_message(
        data['dialogue_id'],
        role='assistant',
        text=chat_response,
        session_maker=session_maker
        )
    pprint(messages)
