import os
import openai
import audioread
from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import types, Bot
from sqlalchemy.orm import sessionmaker

from bot.handlers.keyboards.user_kb import gen_transcribe_bt
from bot.handlers.user._tools import decoder_to_mp3
from bot.handlers._accounting import add_wisper_tokens


async def type_file(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker,
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
    with audioread.audio_open(file_path) as f:
        totalsec = f.duration
        duration = int(totalsec)
        await add_wisper_tokens(duration, state, session_maker)
    
    os.remove(file_path)


async def type_voice(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker,
        **data: dict[str, Any],
    ):
    mess = await SendMessage(
        text='Обработка...',
        chat_id=message.from_user.id,
    )
    file_id = message.voice.file_id
    bot: Bot = data['bot']

    file = await bot.get_file(file_id)
    file_path = await decoder_to_mp3(file, bot)

    with open(file_path, "rb") as file:
        ansver: str = openai.Audio.transcribe(
            "whisper-1",
            file,
            response_format='text'
            )
        len_ans = len(ansver)
        if len_ans >= 4000:
            start = 0
            finish = 4000
            while len_ans > finish:
                await SendMessage(
                    text=ansver[start:finish],
                    chat_id=message.from_user.id,
                )
                start += 4000
                finish += 4000
            
                finish = finish if finish < len_ans else len_ans
            return

        await mess.edit_text(
            text=ansver,
            reply_markup=gen_transcribe_bt(mess.message_id)
        )
    
    with audioread.audio_open(file_path) as f:
        totalsec = f.duration
        duration = int(totalsec)
        await add_wisper_tokens(duration, state, session_maker)
    os.remove(file_path)
