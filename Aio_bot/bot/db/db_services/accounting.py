"""
Запросы для модели Accounting
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select

from bot.db import User, Accounting


async def get_or_create_account(
        user_id: int,
        model: str,
        session_maker: sessionmaker,
        spent: int = 0,
        paid: int = 0,
    ) -> Accounting:
    """
    Вернуть или создать и вернуть экземпляр Accounting 
    """
    async with session_maker() as session:
        async with session.begin():
            get_account = await session.scalars(
                select(Accounting)
                .where(
                    (Accounting.user_id == int(user_id)) &
                    (Accounting.model == model)
                )
            )
            if account := get_account.first():
                return account # если учётка с такой моделью уже есть, возвращаем её
            
            user_res = await session.scalars(
                select(User)
                .options(selectinload(User.account))
                .where(User.user_id == int(user_id))
            )
            user: User = user_res.first()
            account = Accounting(
                model = model,
                spent = spent,
                paid = paid,
                user_id = user_id
            )
            user.account.append(account)
            session.add(account)
            session.add(user)
        return account


async def get_user_account(
        user_id: int,
        model: str,
        session_maker: sessionmaker
    ) -> list[Accounting]:
    """
    Вернуть все модели учета токенов пользователя
    """
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Accounting)
                .where(
                    (Accounting.user_id == int(user_id)) &
                    (Accounting.model == model) 
                )
            )
        return sql_res.first()


async def apdate_account_tokens(
        account_id: int,
        torens: int,
        session_maker: sessionmaker
    ) -> list[Accounting]:
    """
    Обновить инфу о токенах
    """
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Accounting)
                .where(Accounting.id == int(account_id))
            )
            acc: Accounting = sql_res.first()
            acc.spent += torens
            session.add(acc)
