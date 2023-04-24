from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot.db import Dialogue


class TranscribeCD(CallbackData, prefix='to_gpt'):
    """
        Обработка отрисовки списка юзеров
    """
    flag: str = '1'
    message_id: str = None


def gen_transcribe_bt(message_id):
    BT = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Отправить GPT',
                    callback_data=TranscribeCD(message_id=str(message_id)).pack()
                )
            ]
        ]
    )
    return BT


class UserDialoguesCallback(CallbackData, prefix='user_dials'):
    """
        Обработка отрисовки списка юзеров
    """
    flag: str = '1'
    dial_id: str = None


def gen_dialogues_kb(gials: list[Dialogue]) -> InlineKeyboardMarkup:
    """
    Сгенерировать клавиатуру с ролями пользователя
    gials: список диалогов
    """

    builder = InlineKeyboardBuilder()
    for gial in gials:
        builder.button(
            text=gial.name,
            callback_data=UserDialoguesCallback(
                dial_id=gial.id,
                ).pack()
            )
    builder.adjust(1)
    return builder.as_markup()


class SettingsCallback(CallbackData, prefix='sett'):
    """
        Настройки диалога
    """
    flag: str = '1'
    param: str = None


def gen_settings_kb(payload: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    payload.pop('messages')
    keys = payload.keys()
    for key in keys:
        builder.button(
            text=key,
            callback_data=SettingsCallback(
                param=key,
                ).pack()
            )
    builder.adjust(1)
    return builder.as_markup()
