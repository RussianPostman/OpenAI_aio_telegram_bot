# import tiktoken
# import openai
# import os


# openai.api_type = "azure"
# openai.api_version = "2023-03-15-preview" 
# openai.api_base = os.getenv("OPENAI_API_BASE")  # Your Azure OpenAI resource's endpoint value .
# openai.api_key = os.getenv("OPENAI_API_KEY")

# system_message = {"role": "system", "content": "You are a helpful assistant."}
# max_response_tokens = 250
# token_limit= 4096
# conversation=[]
# conversation.append(system_message)


# def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
#     encoding = tiktoken.encoding_for_model(model)
#     num_tokens = 0
#     for message in messages:
#         num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
#         for key, value in message.items():
#             num_tokens += len(encoding.encode(value))
#             if key == "name":  # if there's a name, the role is omitted
#                 num_tokens += -1  # role is always required and always 1 token
#     num_tokens += 2  # every reply is primed with <im_start>assistant
#     return num_tokens

# while(True):
#     user_input = input("")     
#     conversation.append({"role": "user", "content": user_input})
#     conv_history_tokens = num_tokens_from_messages(conversation)
#     while (conv_history_tokens+max_response_tokens >= token_limit):
#         del conversation[1] 
#         conv_history_tokens = num_tokens_from_messages(conversation)
        
#     response = openai.ChatCompletion.create(
#         engine="gpt-35-turbo", # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
#         messages = conversation,
#         temperature=.7,
#         max_tokens=max_response_tokens,
#     )
#     conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
#     print("\n" + response['choices'][0]['message']['content'] + "\n")


from sqlalchemy import URL
import asyncio
import os
from bot.db import create_async_engine, get_session_maker
from bot.db import delete_first_message


postgres_url = URL.create(
        drivername="postgresql+asyncpg",
        username=os.getenv("POSTGRES_USER"),
        host='127.0.0.1',
        database=os.getenv("POSTGRES_DB"),
        port=os.getenv("POSTGRES_PORT"),
        password=os.getenv("POSTGRES_PASSWORD")
    )


async_engine = create_async_engine(postgres_url)
session_maker = get_session_maker(async_engine)


async def main():
    a = await delete_first_message(20, session_maker)


asyncio.run(main())