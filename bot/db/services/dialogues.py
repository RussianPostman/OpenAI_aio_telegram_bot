from datetime import date
from typing import Any
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select

from bot.db import User, Dialogue
from bot.settings import redis


async def create_dialogue(
        user_id: int,
        session_maker: sessionmaker, 
        model: str,
        temperature: float = 1.0,
        top_p: float = 1.0,
        n: int = 1,
        max_tokens: int = 1500,
        presence_penalty: float = 0,
        frequency_penalty: float = 0,
    ) -> Dialogue:
    async with session_maker() as session:
        async with session.begin():
            tuday = date.today()
            year_minth = tuday.strftime(' %d.%m.%Y')
            user_res = await session.scalars(
                select(User)
                .options(selectinload(User.dialogues))
                .where(User.user_id == int(user_id))
            )
            user: User = user_res.first()
            name = model + year_minth
            dialogue = Dialogue(
                name = name,
                model = model,
                temperature = temperature,
                top_p = top_p,
                n = n,
                max_tokens = max_tokens,
                presence_penalty = presence_penalty,
                frequency_penalty = frequency_penalty,
                user_id = user_id
            )
            user.dialogues.append(dialogue)
            session.add(dialogue)
            session.add(user)
            return dialogue


async def get_user_dialogues(
        user_id: int,
        session_maker: sessionmaker
    ) -> list[Dialogue]:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Dialogue)
                .where(Dialogue.user_id == int(user_id))
            )
        return sql_res.all()


async def get_dialogue(
        user_id: int,
        dialogue_name: str,
        session_maker: sessionmaker,
    ) -> Dialogue:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Dialogue)
                .where(
                    (Dialogue.user_id == int(user_id)) &
                    (Dialogue.name == dialogue_name)
                )
            )
        return sql_res.first()


async def get_dial_by_id(
        dial_id: int,
        session_maker: sessionmaker,
    ) -> Dialogue:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Dialogue)
                .where(Dialogue.id == int(dial_id))
            )
            return sql_res.first()


async def update_dial_field(
        dial_id: int,
        field_name: int,
        value: Any,
        session_maker: sessionmaker,
    ):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Dialogue)
                .where(Dialogue.id == int(dial_id))
            )
            dial: Dialogue = sql_res.first()
            print(dial.temperature)
            setattr(dial, field_name, value)
            print(dial.temperature)
            session.add(dial)
