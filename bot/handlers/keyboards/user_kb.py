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