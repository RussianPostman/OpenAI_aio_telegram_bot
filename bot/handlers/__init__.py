__all__ = ['register_user_commands']

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import any_state

from .commands import censel_hendler, dialogue_list, chat_mode
from .user.dialogue import DialogueStates, new_GPT_3, dialogue, \
    new_GPT_4, open_dialogue, transcribe_to_gpt, new_dial_with_prompt
from .user.transcribes import type_voice, type_file
from bot.handlers.keyboards.user_kb import UserDialoguesCallback, \
    SettingsCallback, TranscribeCD, SelectPromptCD
from bot.handlers.user.dial_settings import dial_settings, settings_menu, \
    dial_change


def register_user_commands(router: Router) -> Router:
    """
    Зарегистрировать хендлеры пользователя
    :param router:
    """
    router.message.register(new_GPT_3, CommandStart())
    router.message.register(new_GPT_3, Command('new_gpt_3'), any_state)
    router.message.register(new_GPT_4, Command('new_gpt_4'), any_state)
    router.message.register(dialogue_list, Command('my_dialogues'), any_state)
    router.message.register(chat_mode, Command('mode'), any_state)
    router.callback_query.register(
        open_dialogue, UserDialoguesCallback.filter(F.flag == '1'))
    router.callback_query.register(
        new_dial_with_prompt, SelectPromptCD.filter(F.flag == '1'))

    # хендлеры выхода из машины состояний
    router.message.register(censel_hendler, Command('cancel'), any_state) 
    router.message.register(censel_hendler, F.text.casefold().lower() == 'отмена', any_state)
    router.callback_query.register(censel_hendler, F.data == 'cancel', any_state)

    # хендлеры диалога
    router.message.register(type_voice, F.voice, DialogueStates.dialogue)
    router.message.register(type_file, F.audio, DialogueStates.dialogue)
    router.message.register(dial_settings, Command('settings'), DialogueStates.dialogue)
    router.message.register(dialogue, DialogueStates.dialogue)
    router.callback_query.register(
        settings_menu, SettingsCallback.filter(F.flag == '1'), DialogueStates.settings_menu)
    router.callback_query.register(
        transcribe_to_gpt, TranscribeCD.filter(F.flag == '1'), DialogueStates.dialogue)
    router.message.register(dial_change, DialogueStates.change_2)
