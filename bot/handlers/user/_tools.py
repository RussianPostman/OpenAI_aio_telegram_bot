from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.db import Dialogue
from bot import settings as sett
from bot.db import create_message, get_dialogue_messages


async def generate_payload(
        state: FSMContext,
        last_dialogue: Dialogue,
        session_maker: sessionmaker
    ):
    payload = {
        'model': last_dialogue.model,
        'temperature': last_dialogue.temperature,
        'top_p': last_dialogue.top_p,
        'n': last_dialogue.n,
        # 'max_tokens': last_dialogue.max_tokens,
        'presence_penalty': last_dialogue.presence_penalty,
        'frequency_penalty': last_dialogue.frequency_penalty,
        # 'messages': [{"role": "system", "content": sett.DEFOULT_PROMPT}]
    }
    messages_list = await get_dialogue_messages(
        last_dialogue.id,
        session_maker=session_maker
        )
    if len(messages_list) == 0:
        payload['messages'] =[{"role": "system", "content": sett.DEFOULT_PROMPT}]
        await create_message(
            last_dialogue.id,
            role='system',
            text=sett.DEFOULT_PROMPT,
            session_maker=session_maker
            )
    else:
        inlist = []
        for i in messages_list:
            inlist.append({"role": i.role, "content": i.text})
        payload['messages'] = inlist

    await state.update_data(payload=payload)
    await state.update_data(dialogue_id=last_dialogue.id)