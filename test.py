import asyncio
from datetime import date
from pprint import pprint
from bot import openai_async
from httpx import Response

from bot.settings import OPENAI_API_KEY, GPT4_API_KEY


async def main():
    completion: Response = await openai_async.chat_complete(
        api_key=OPENAI_API_KEY,
        timeout=60,
        payload={
            'model': "gpt-3.5-turbo",
            'messages': [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"}
            ]
        },
    )
    pprint(completion)
    chat_response = completion.json()["choices"][0]["message"]['content']
    print(chat_response)


asyncio.run(main())
