"""
Тут все клавиатуры хендлеров
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot.db import Dialogue
from bot.db.models import Prompt

class TranscribeCD(CallbackData, prefix='to_gpt'):
    """
        Обработка отрисовки списка юзеров
    """
    flag: str = '1'
    message_id: str = None


def gen_transcribe_bt(message_id):
    """Кнопка для отправки текта сообщения в гпт"""
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
    Генерирует клавиатуру для выбора диалога
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
    """
    Генерирует клаву для настройки диалога
    """
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


class SelectPromptCD(CallbackData, prefix='sel_prompt'):
    """
    Выбор предустановленной модификации диалога
    """
    flag: str = '1'
    id: str = None


def gen_prompts_kb(prompts: list[Prompt]) -> InlineKeyboardMarkup:
    """
    Генерирует клавиатуру для выбора предустановленного промпта
    """
    builder = InlineKeyboardBuilder()
    for prompt in prompts:
        builder.button(
            text=prompt.name,
            callback_data=SelectPromptCD(
                id=prompt.id,
                ).pack()
            )
    builder.adjust(1)
    return builder.as_markup()
