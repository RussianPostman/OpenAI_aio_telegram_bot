from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from bot.db.models import User, Role
from bot.settings import redis


async def create_user(
        user_id: int,
        role_name: str,
        session_maker: sessionmaker,
        ):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Role).where(Role.name == role_name)
            )
            role = sql_res.first()
            print('11111111111111111')
            user = User(
                user_id=int(user_id),
            )
            user.roles.append(role)
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
    if res != 1:
        async with session_maker() as session:
            async with session.begin():
                sql_res = await session.execute(
                    select(User).where(User.user_id == int(user_id))
                )
                result = sql_res.first()
                await redis.set(name=str(user_id), value=1 if result else 0)
                return bool(result)
    return bool(res)