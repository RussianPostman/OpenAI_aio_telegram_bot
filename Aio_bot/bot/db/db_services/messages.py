"""
Запросы для модели Message
"""
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select

from bot.db import Message, Dialogue
from bot.settings import redis


async def create_message(
        dialogue_id: str,
        role: str,
        text: str,
        session_maker: sessionmaker
    ):
    """
    Создать Message
    """
    async with session_maker() as session:
        async with session.begin():
            dialogue_res = await session.scalars(
                select(Dialogue)
                .options(selectinload(Dialogue.messages))
                .where(Dialogue.id == int(dialogue_id))
            )
            dialogue: Dialogue = dialogue_res.first()
            message = Message(
                role=role,
                text=text
            )
            dialogue.messages.append(message)
            session.add(message)
            session.add(dialogue)


async def get_dialogue_messages(
        dialogue_id: str,
        session_maker: sessionmaker
    ) -> list[Message]:
    """
    вернуть все сообщения в диалоге
    """
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Message)
                .where(Message.dialogue_id == int(dialogue_id))
            )
            return sql_res.all()


async def delete_first_message(
        dialogue_id: str,
        session_maker: sessionmaker
    ) -> Message:
    """
    Удалить самое старое не системное сообщение
    """
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Message)
                .where(Message.dialogue_id == int(dialogue_id))
            )
            result = sql_res.all()
            first = result[1]
            print(first.text)
            await session.delete(first)

