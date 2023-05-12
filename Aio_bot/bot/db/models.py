"""
Ну тут просто модели в базе данных
"""
from sqlalchemy import BigInteger, Column, ForeignKey, String, Table
from sqlalchemy.orm import mapped_column, Mapped, relationship

from bot.db.base import BaseModel


association_table = Table(
    "association_table",
    BaseModel.metadata,
    Column("user_id", ForeignKey("users.user_id")),
    Column("role_id", ForeignKey("roles.id")),
)


class User(BaseModel):
    """Класс пользователя"""
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(100), nullable=True)

    dialogues: Mapped[list["Dialogue"]] = relationship(back_populates="user")
    account: Mapped[list["Accounting"]] = relationship( back_populates="user")
    prompts: Mapped[list["Prompt"]] = relationship(back_populates="user")
    roles: Mapped[list["Role"]] = relationship(
        secondary=association_table, back_populates="users"
    )
    

    def __str__(self) -> int:
        return f'User: {self.name}'

    def __repr__(self):
        return self.__str__()


class Role(BaseModel):
    """
    Класс ролей пользователей
    args:
        name: Mapped[int] = mapped_column(String(100))
        users: Mapped[list[User]]
    """
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(100))
    users: Mapped[list[User]] = relationship(
        secondary=association_table, back_populates="roles"
    )

    def __str__(self) -> int:
        return f'Role: {self.name}'

    def __repr__(self):
        return self.__str__()


class Accounting(BaseModel):
    """
    Класс учёта токенов
    args:
        model: Mapped[str] - модель ГПТ
        spent: Mapped[int] - потраченно токенов
        paid: Mapped[int] - доступно токенов
    """
    __tablename__ = 'accounting'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    model: Mapped[str]
    spent: Mapped[int]
    paid: Mapped[int]

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship(back_populates="account")

    def __str__(self) -> int:
        return f'Модель: {self.model}'

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
    parse_mode: Mapped[str] = mapped_column(default='markdown')

    model: Mapped[str]
    temperature: Mapped[float]
    top_p: Mapped[float]
    n: Mapped[int]
    max_tokens: Mapped[int]
    presence_penalty: Mapped[float]
    frequency_penalty: Mapped[float]

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship(back_populates="dialogues")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="dialogue", cascade="all, delete")


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


class Prompt(BaseModel): 
    """
    Класс заранее заготовленных промптов к языковой модели
    args:
        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        name: Mapped[str]
        text: Mapped[str]
        parse_mode: Mapped[str]
        welcome_message: Mapped[str]
        public: Mapped[bool]
    """

    __tablename__ = 'prompts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    text: Mapped[str]
    parse_mode: Mapped[str]
    welcome_message: Mapped[str] = mapped_column(nullable=True)
    public: Mapped[bool]

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship(back_populates="prompts")


