"""
    Клавиатура для отображения постов
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


START_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Начать диалог')
        ],
        [
            KeyboardButton(text='Сделать транскрипцию')
        ]
    ],
    resize_keyboard=True
)


DIALOGUE_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Стереть память', callback_data='clear')
        ],
        [
            InlineKeyboardButton(text='Закончить разговор', callback_data='cancel')
        ],
    ]
)


SELECT_TYPE_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            KeyboardButton(text='Отправить файлом', callback_data='file')
        ],
        [
            KeyboardButton(text='Отправить голосовое', callback_data='voice')
        ]
    ],
)
