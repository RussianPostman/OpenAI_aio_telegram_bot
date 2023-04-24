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

from bot.handlers.keyboards.user_kb import gen_transcribe_bt
from bot.settings import OPENAI_API_KEY, TIMEOUT
from bot import openai_async
from bot.handlers.user._tools import decoder_to_mp3

async def type_file(
        message: types.Message,
        **data: dict[str, Any],
        ):

    file_id = message.audio.file_id
    bot: Bot = data['bot']

    file = await bot.get_file(file_id)
    file_path = await decoder_to_mp3(file, bot)
    mess = await SendMessage(
        text='Обработка...',
        chat_id=message.from_user.id,
    )

    with open(file_path, "rb") as file:
        ansver = openai.Audio.transcribe(
            "whisper-1",
            file,
            response_format='text'
            )
        await mess.edit_text(
            text=ansver,
            reply_markup=gen_transcribe_bt(mess.message_id)
        )
    os.remove(file_path)


async def type_voice(
        message: types.Message,
        state: FSMContext,
        **data: dict[str, Any],
    ):
    mess = await SendMessage(
        text='Обработка...',
        chat_id=message.from_user.id,
    )

    file_id = message.voice.file_id
    bot: Bot = data['bot']
    file = await bot.get_file(file_id)
    tg_file_path = file.file_path
    file_path = f'bot/docs/{file_id}.mp3'
    audio_file: io.BytesIO = await bot.download_file(tg_file_path)
    audio_file.name = 'new.ogg'
    given_audio = AudioSegment.from_file(audio_file)
    given_audio.export(file_path, format="mp3")

    with open(file_path, "rb") as file:
        ansver = openai.Audio.transcribe(
            "whisper-1",
            file,
            response_format='text'
            )
        await mess.edit_text(
            text=ansver,
            reply_markup=gen_transcribe_bt(mess.message_id)
        )
        
    os.remove(file_path)
