from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from bot.db import User
from bot.settings import redis


async def create_user(user_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
            )
            session.add(user)


async def get_user(user_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(User).where(User.user_id  == user_id)
            )
            return sql_res.first()


async def get_all_users(session_maker: sessionmaker) -> list[User]:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(User)
            )
            result = sql_res.all()
            return result


async def is_user_exists(user_id: int, session_maker: sessionmaker) -> bool:
    res = await redis.get(name=str(user_id))
    if not res:
        async with session_maker() as session:
            async with session.begin():
                sql_res = await session.execute(
                    select(User).where(User.user_id == user_id)
                )
                result = sql_res.first()
                await redis.set(name=str(user_id), value=1 if result else 0)
                return bool(result)
    return bool(res)