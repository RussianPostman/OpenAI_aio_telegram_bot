import asyncio
import yaml
from pprint import pprint
from sqlalchemy.orm import sessionmaker

import bot.settings as sett
import bot.db as db


async def set_users_roles(session_maker: sessionmaker):
    roles_list = ['admin', 'user']
    for role in roles_list:
        await db.role_get_or_create(role, session_maker)


async def set_admins(session_maker: sessionmaker):
    admins_list = sett.ADMINS_ID
    print(admins_list)
    for admin in admins_list:
        if not await db.is_user_exists(admin, session_maker):
            await db.create_user(admin, 'admin', session_maker)


async def set_prompts(session_maker: sessionmaker):
    with open('bot/on_start/prompts.yaml', encoding='utf-8') as f:
        prompts = yaml.safe_load(f)
        for prompt in prompts:
            admin = sett.ADMINS_ID[0]
            prompt_dict = prompts.get(prompt)
            await db.prompt_get_or_create(
                name=prompt_dict.get('name'),
                text=prompt_dict.get('prompt_start'),
                welcome_message=prompt_dict.get('welcome_message'),
                parse_mode=prompt_dict.get('parse_mode'),
                public=True,
                session_maker=session_maker,
                user_id=admin
            )


async def on_start(session_maker: sessionmaker):
    await set_users_roles(session_maker)
    print('Роли')
    await set_admins(session_maker)
    print('Админ состав')
    await set_prompts(session_maker)
    print('Промпты')
