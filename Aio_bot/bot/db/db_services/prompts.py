"""
Запросы для модели Prompt
"""
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select

from bot.db.models import Prompt


async def prompt_get_or_create(
        user_id: int,
        name: str,
        text: str,
        session_maker: sessionmaker,
        welcome_message: str,
        parse_mode: str = 'markdown',
        public: bool = False,
    ) -> Prompt:
    """
    Вернуть или создать и вернуть экземпляр Prompt 
    """
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Prompt)
                .where(
                    (Prompt.user_id == int(user_id)) &
                    (Prompt.name == name)
                )
            )

            if prompt := sql_res.first():
                return prompt, False

            prompt = Prompt(
                name=name,
                text=text,
                parse_mode=parse_mode,
                welcome_message=welcome_message,
                public=public,
                user_id=int(user_id)
            )
            session.add(prompt)
        return prompt
    

async def prompt_create(
        user_id: int,
        name: str,
        text: str,
        session_maker: sessionmaker,
        welcome_message: str,
        parse_mode: str = 'markdown',
        public: bool = False,
    ) -> Prompt:
    """
    Создать новый промпт
    """
    async with session_maker() as session:
        async with session.begin():
            prompt = Prompt(
                name=name,
                text=text,
                parse_mode=parse_mode,
                welcome_message=welcome_message,
                public=public,
                user_id=user_id
            )
            session.add(prompt)
        return prompt


async def get_public_prompts(
        session_maker: sessionmaker,
    ) -> list[Prompt]:
    """
    Выдать все public == Trye промпты
    """ 
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Prompt)
                .where(Prompt.public == True)
            )
            return sql_res.all()


async def prompt_get_by_id(
        prompt_id: int,
        session_maker: sessionmaker,
    ) -> Prompt:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Prompt)
                .where(Prompt.id == int(prompt_id))
            )
            return sql_res.first()
