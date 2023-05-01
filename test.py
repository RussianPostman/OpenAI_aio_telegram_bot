# from sqlalchemy import URL
# import asyncio
# import os
# from bot.db import create_async_engine, get_session_maker
# from bot.db import get_or_create_account


# postgres_url = URL.create(
#         drivername="postgresql+asyncpg",
#         username=os.getenv("POSTGRES_USER"),
#         host='127.0.0.1',
#         database=os.getenv("POSTGRES_DB"),
#         port=os.getenv("POSTGRES_PORT"),
#         password=os.getenv("POSTGRES_PASSWORD")
#     )


# async_engine = create_async_engine(postgres_url)
# session_maker = get_session_maker(async_engine)


# async def main():
#     a = await get_or_create_account(2125332262,"gpt-3.5-turbo", session_maker)
#     print(a.user_id)


# asyncio.run(main())

import asyncio
import openai


def _postprocess_answer(answer):
        answer = answer.strip()
        return 


async def send_message_stream(messages, model = "gpt-4"):
    answer = None
    while answer is None:
        if model in {"gpt-3.5-turbo", "gpt-4"}:
            r_gen = await openai.ChatCompletion.acreate(
                model=model,
                messages=messages,
                stream=True,
            )
            print(r_gen)
            print(type(r_gen))
            answer = ""
            async for r_item in r_gen:
                delta = r_item.choices[0].delta
                if "content" in delta:
                    answer += delta.content
                    yield "not_finished", answer

            answer = _postprocess_answer(answer)
            # dialog_messages = dialog_messages[1:]

    yield "finished", answer


mess = ({"role": 'user', "content": 'расскажи о себе'},)
openai.api_key = "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"



async def message_handle_fn():
    gen = send_message_stream(mess)

    prev_answer = ""
    async for gen_item in gen:
        status, answer = gen_item
        answer = answer[:4096]
        if abs(len(answer) - len(prev_answer)) < 70 and status != "finished":
            continue

        prev_answer = answer
        print(answer)
        await asyncio.sleep(0.3)


asyncio.run(message_handle_fn())
