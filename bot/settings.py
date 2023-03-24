import os
from httpx import Timeout
from dotenv import load_dotenv

load_dotenv()


bot_commands = (
    ("start", "Начало работы с ботом"),
    ("cancel", "Отменить действие"),
)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TIMEOUT = Timeout(10.0, read=None)
