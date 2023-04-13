from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from bot.db.base import BaseModel


class User(BaseModel):
    """
    Класс юзера
    args:
        user_id: Mapped[int] = mapped_column(BigInteger)
        dialogues: Mapped[list["Dialogue"]] back_populates="user"
    """
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    dialogues: Mapped[list["Dialogue"]] = relationship(back_populates="user")

    def __str__(self) -> int:
        return f'User: {self.user_id}'

    def __repr__(self):
        return self.__str__()


class Dialogue(BaseModel):
    """
    Класс диалогов
    args:
        name: Mapped[str]

        model: Mapped[str]
        temperature: Mapped[float]
        top_p: Mapped[float]
        n: Mapped[int]
        max_tokens: Mapped[int]
        presence_penalty: Mapped[float]
        frequency_penalty: Mapped[float]

        user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
        messages: Mapped[list["Message"]] back_populates="dialogue"
    """
    __tablename__ = 'dialogues'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    model: Mapped[str]
    temperature: Mapped[float]
    top_p: Mapped[float]
    n: Mapped[int]
    max_tokens: Mapped[int]
    presence_penalty: Mapped[float]
    frequency_penalty: Mapped[float]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship(back_populates="dialogues")
    messages: Mapped[list["Message"]] = relationship(back_populates="dialogue")


class Message(BaseModel):
    """
    Класс сообщений в диалоге
    args:
        role: Mapped[str]
        text: Mapped[str]
        dialogue_id: Mapped[int] = mapped_column(ForeignKey("dialogues.id"))
        dialogue: Mapped["Dialogue"] = back_populates="messages"
    """
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[str]
    text: Mapped[str]

    dialogue_id: Mapped[int] = mapped_column(ForeignKey("dialogues.id"))
    dialogue: Mapped["Dialogue"] = relationship(back_populates="messages")

