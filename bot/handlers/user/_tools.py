import asyncio
import io
from pprint import pprint
from aiogram.fsm.context import FSMContext
import openai
from sqlalchemy.orm import sessionmaker
import tiktoken
from aiogram import types, Bot
from pydub import AudioSegment

from bot.db import Dialogue
from bot import openai_async, settings as sett
from bot.db import create_message, get_dialogue_messages, \
    delete_first_message
from bot.db.services.accounting import get_or_create_account


def _num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


async def gen_dialogue_cache(
        user_id: int,
        state: FSMContext,
        last_dialogue: Dialogue,
        session_maker: sessionmaker
    ):
    await generate_payload(
        state,
        last_dialogue,
        session_maker
    )
    await set_accounting(
        state,
        user_id,
        session_maker
    )



async def generate_payload(
        state: FSMContext,
        last_dialogue: Dialogue,
        session_maker: sessionmaker
    ):
    """
    На основе данных из БД заполняет кеш диалога данными:
        payload - данные для запроса
        dialogue_id - айди диалога в БД
    """
    payload = {
        'model': last_dialogue.model,
        'temperature': last_dialogue.temperature,
        'top_p': last_dialogue.top_p,
        'n': last_dialogue.n,
        'max_tokens': last_dialogue.max_tokens,
        'presence_penalty': last_dialogue.presence_penalty,
        'frequency_penalty': last_dialogue.frequency_penalty,
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
    return sett.DEFOULT_PROMPT


async def add_message(
        text: str,
        role: str,
        state: FSMContext
        ):
    """
    Записывает в БД сообщение к языковой модели или от неё
    """
    data = await state.get_data()
    payload: dict = data['payload']
    messages = payload.pop('messages')
    messages.append({"role": role, "content": text})
    payload['messages'] = messages
    await state.update_data(payload=payload)
    return await state.get_data()
    

async def check_tokens_buffer(
        state: FSMContext,
        session_maker: sessionmaker
    ):
    """
    Чистит кеш диалога удаляя самые старые сообщения так, чтобы количество
    токенов в запросе к языковым моделям не переполнялось.
    """
    data: dict = await state.get_data()
    payload: dict = data.get('payload')

    messages: list[dict] = payload.get('messages')
    token_limit = 8192 if payload.get('model') == 'gpt-4' else 4096
    max_tokens = payload.get('max_tokens')
    conv_history_tokens = _num_tokens_from_messages(messages)
    print(conv_history_tokens)

    while (conv_history_tokens+max_tokens >= token_limit):
        del messages[1]
        await delete_first_message(data.get('dialogue_id'), session_maker)
        conv_history_tokens = _num_tokens_from_messages(messages)

    pprint(messages)
    payload['messages'] = messages
    await state.update_data(payload=payload)


async def get_api_key(
        dialogue: Dialogue,
        state: FSMContext
        ):
    """
    Выбирает апи ключ для использования
    """
    match dialogue.model:
        case 'gpt-4':
            await state.update_data(api_key=sett.GPT4_API_KEY)
        case 'gpt-3.5-turbo':
            await state.update_data(api_key=sett.OPENAI_API_KEY)
        case _:
            raise KeyError('Неопределённая модель ГПТ')


async def validation(
        params: str,
        message: str
    ):
    """
    Валидация данных при изменении настроек языковой модели
    """
    match params:
        case 'temperature':
            dt = float(message)
            return dt if dt in range(0, 3) else None
        case 'top_p':
            dt = float(message)
            return dt if dt in range(0, 3) else None
        case 'n':
            dt = int(message)
            return dt if dt in range(0, 11) else None
        case'max_tokens':
            dt = int(message)
            return dt if dt in range(0, 3000) else None
        case 'presence_penalty':
            dt = float(message)
            return dt if dt in range(-2, 3) else None
        case 'frequency_penalty':
            dt = float(message)
            return dt if dt in range(-2, 3) else None
        case _:
            raise ValueError()


async def decoder_to_mp3(file: types.file.File, bot: Bot):
    file_id = file.file_id
    tg_file_path = file.file_path

    file_path = f'bot/docs/{file_id}.mp3'
    audio_file: io.BytesIO = await bot.download_file(tg_file_path)
    audio_file.name = 'new.ogg'
    given_audio = AudioSegment.from_file(audio_file)
    given_audio.export(file_path, format="mp3")
    return file_path


async def set_accounting(
        state: FSMContext,
        user_id: int,
        session_maker: sessionmaker
        ):
    data = await state.get_data()
    model = data['payload']['model']
    acc = await get_or_create_account(
        user_id,
        model,
        session_maker
        )
    whisper_acc = await get_or_create_account(
        user_id,
        'whisper-1',
        session_maker
        )
    
    await state.update_data(whisper_acc=whisper_acc.id)
    await state.update_data(accounting_id=acc.id)


async def send_message_stream(state: FSMContext):
    data = await state.get_data()
    payload = data.get('payload')
    model = payload.get('model')

    answer = None
    while answer is None:
        if model == "gpt-4":
            openai.api_key = sett.GPT4_API_KEY
        elif model == "gpt-3.5-turbo":
            openai.api_key = sett.OPENAI_API_KEY
        r_gen = await openai.ChatCompletion.acreate(stream=True, **payload)
        answer = ""
        async for r_item in r_gen:
            delta = r_item.choices[0].delta
            if "content" in delta:
                answer += delta.content
                yield "not_finished", answer
            answer = answer

    yield "finished", answer


async def message_handle_fn(
        state: FSMContext,
        message: types.message.Message
        ) -> str:
    gen = send_message_stream(state)
    prev_answer = ""
    async for gen_item in gen:
        status, answer = gen_item
        answer = answer[:4096]
        if abs(len(answer) - len(prev_answer)) < sett.DELTA_CHARACTERS and status != "finished":
            continue

        prev_answer = answer
        await message.edit_text(answer)
        await asyncio.sleep(0.3)
        if status == "finished":
            return answer
    await message.edit_text(answer)
    return answer
