"""
Логика учёта токенов
"""
from pprint import pprint
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker
import tiktoken

from bot.db import apdate_account_tokens


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


async def check_tokens_limit(
        state: FSMContext,
        session_maker: sessionmaker,
        model: str = None
    ):
    """
    Считает и записывет постраченные токены в языковых моделях
    """
    data = await state.get_data()
    payload = data['payload']
    if not model:
        model = payload['model']
    messages: list = payload['messages']
    

    tokens_all = _num_tokens_from_messages(messages, model)
    messages.pop(-1)
    tokens_without_last = _num_tokens_from_messages(messages, model)

    spent_tokens = tokens_all - tokens_without_last
    print('spent_tokens')
    print(spent_tokens)

    await apdate_account_tokens(data['accounting_id'], spent_tokens, session_maker)


async def add_wisper_tokens(
        tokens: int,
        state: FSMContext,
        session_maker: sessionmaker,
    ):
    """
    Обновляет данные о потраченных пользователем токенах в модели whisper-1
    """
    data = await state.get_data()
    await apdate_account_tokens(data['whisper_acc'], tokens, session_maker)

