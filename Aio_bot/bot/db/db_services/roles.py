from datetime import date
from typing import Any
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select

from bot.db.models import User, Role


async def role_get_or_create(
        name: str,
        session_maker: sessionmaker,
    ) -> Role:
    """
    Вернуть или создать и вернуть экземпляр Role 
    """
    async with session_maker() as session:
        async with session.begin():
            get_roles = await session.scalars(
                select(Role)
                .where(Role.name == name)
            )
            if role := get_roles.first():
                return role # если учётка с такой моделью уже есть, возвращаем её

            role = Role(
                name=name,
            )
            session.add(role)
        return role