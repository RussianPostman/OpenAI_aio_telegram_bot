import io
import os
import aiofiles
from pprint import pprint
from typing import Any
from httpx import Response, Timeout
import openai
from pydub import AudioSegment

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import types, Bot

from bot.handlers.keyboards.user_kb import SELECT_TYPE_KB
from bot.settings import OPENAI_API_KEY, TIMEOUT
from bot import openai_async


class TranscribesStates(StatesGroup):
    """
    Состояния для диалога с GPT
    """
    sel_input_type = State()
    type_file = State()
    type_voice = State()


async def start_transcribe(
        message: types.Message,
        state: FSMContext,
        ):
    await state.set_state(TranscribesStates.sel_input_type)
    await message.answer(
        'В каком виде передадите аудиио?',
        reply_markup=SELECT_TYPE_KB
        )


async def set_type_file(
        query: types.CallbackQuery,
        state: FSMContext,
        ):
    await state.set_state(TranscribesStates.type_file)
    await SendMessage(
        text='Пришлите aудиофайл',
        chat_id=query.from_user.id,
    )


async def type_file(
        message: types.Message,
        **data: dict[str, Any],
        ):

    file_id = message.audio.file_id
    bot: Bot = data['bot']

    file = await bot.get_file(file_id)
    file_path = file.file_path
    audio_file: io.BytesIO = await bot.download_file(file_path)
    audio_file.name = 'new.mp3'
    ansver = openai.Audio.transcribe("whisper-1", audio_file, response_format='text')

    print(ansver)

    await SendMessage(
        text=ansver,
        chat_id=message.from_user.id,
    )


async def set_type_voice(
        query: types.CallbackQuery,
        state: FSMContext,
        ):
    await state.set_state(TranscribesStates.type_voice)
    await SendMessage(
        text='Перешлите голосовое сообщение',
        chat_id=query.from_user.id,
    )


async def type_voice(
        message: types.Message,
        **data: dict[str, Any],
    ):
    
    file_id = message.voice.file_id
    bot: Bot = data['bot']
    file = await bot.get_file(file_id)

    tg_file_path = file.file_path
    file_path = f'bot/docs/{file_id}.mp3'

    audio_file: io.BytesIO = await bot.download_file(tg_file_path)
    audio_file.name = 'new.ogg'

    given_audio = AudioSegment.from_ogg(audio_file)
    given_audio.export(file_path, format="mp3")

    with open(file_path, "rb") as file:
        ansver = openai.Audio.transcribe(
            "whisper-1",
            file,
            response_format='text'
            )
        await SendMessage(
            text=ansver,
            chat_id=message.from_user.id,
        )
    os.remove(file_path)
