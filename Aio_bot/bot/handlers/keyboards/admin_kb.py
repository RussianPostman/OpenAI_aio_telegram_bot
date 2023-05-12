"""
    Клавиатура для отображения постов
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class UserCD(CallbackData, prefix='user_list'):
    """
        Обработка отрисовки списка юзеров
    """
    flag: str = '1'
    user_id: str = None
    name: str = None


ADMIN_MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить пользователя'),
            KeyboardButton(text='Удалить пользователя'),
        ],
        [
            KeyboardButton(text='Информация о пользователе'),
            KeyboardButton(text='Перейти к Google таблицам'),
        ],
        [
            KeyboardButton(text='Синхронизация')
        ]
    ],
    resize_keyboard=True
)



SYNCHRONIZATION_BOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Роли', callback_data='synchronization_roles')
        ],
        [
            InlineKeyboardButton(text='Детали', callback_data='synchronization_products')
        ],
    ]
)


ADMIN_USER_ROLE = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Администратор', callback_data='admin')
        ]
    ]
)


WORKER_USER_ROLE = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рабочий', callback_data='worker')
        ]
    ]
)
