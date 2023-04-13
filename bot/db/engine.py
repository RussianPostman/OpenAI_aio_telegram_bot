import sqlalchemy.ext.asyncio
from typing import Union
from sqlalchemy import MetaData
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker


def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
    """
    :param url:
    :return:
    """
    return _create_async_engine(
        url=url,
        echo=True,
        #  encoding='utf-8',
        pool_pre_ping=True
    )


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    """
    :param engine:
    :return:
    """
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
