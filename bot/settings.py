import os
from httpx import Timeout
from dotenv import load_dotenv
from aioredis import Redis


load_dotenv()


redis = Redis()

DEBUG = True  # не забудь поменять конфиг алембика

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


if DEBUG:
    POSTGRES_USER=os.getenv("DEBUG_POSTGRES_USER").strip()
    POSTGRES_HOST=os.getenv("DEBUG_POSTGRES_HOST").strip()
    POSTGRES_DB=os.getenv("DEBUG_POSTGRES_DB").strip()
    POSTGRES_PORT=os.getenv("DEBUG_POSTGRES_PORT").strip()
    POSTGRES_PASSWORD=os.getenv("DEBUG_POSTGRES_PASSWORD").strip()

    DB_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    # postgresql+asyncpg://root:ubnfhf@127.0.0.1:8764/OpenAI_db

else:
    POSTGRES_USER=os.getenv("POSTGRES_USER"),
    POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
    POSTGRES_DB=os.getenv("POSTGRES_DB"),
    POSTGRES_PORT=os.getenv("POSTGRES_PORT"),
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")

    DB_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
