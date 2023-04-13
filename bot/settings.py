import os
from httpx import Timeout
from dotenv import load_dotenv
from aioredis import Redis


load_dotenv()


redis = Redis()

bot_commands = (
    ("start", "Начало работы с ботом"),
    ("cancel", "Отменить действие"),
)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TIMEOUT = Timeout(10.0, read=None)
GPT4_API_KEY = os.getenv('GPT4_API_KEY')

DEFOULT_PROMPT = 'Ты - универсальный помощник'
