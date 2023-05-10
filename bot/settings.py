import os
from httpx import Timeout
from dotenv import load_dotenv
from aioredis import Redis


load_dotenv()


redis = Redis()

bot_commands = (
    ("new_gpt_3", "Начать новый диалог c GPT-3.5-turbo"),
    ("new_gpt_4", "Начать новый диалог c GPT-4"),
    ("my_dialogues", "Выбрать диалог"),
    ("mode", "Выбрать тип диалога"),
    ("settings", "Параметры диалога"),
)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TIMEOUT = Timeout(10.0, read=None)
GPT4_API_KEY = os.getenv('GPT4_API_KEY')

DEFOULT_PROMPT = 'Ты - универсальный помощник'
DELTA_CHARACTERS = 30 # количество токенов в режиме стриминга 

ADMINS_ID = os.getenv('ADMIN_ID').split(', ')
