__all__ = ['register_user_commands']

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import any_state

from .commands import censel_hendler, dialogue_list
from .user.dialogue import DialogueStates, new_GPT_3, dialogue, \
    new_GPT_4, open_dialogue, transcribe_to_gpt
from .user.transcribes import type_voice, type_file
from bot.handlers.keyboards.user_kb import UserDialoguesCallback, \
    SettingsCallback, TranscribeCD
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

    # хендлеры выхода из машины состояний
    router.callback_query.register(
        open_dialogue, UserDialoguesCallback.filter(F.flag == '1'))
    router.message.register(censel_hendler, Command('cancel'), any_state) 
    router.message.register(censel_hendler, F.text.casefold().lower() == 'отмена', any_state)
    router.callback_query.register(censel_hendler, F.data == 'cancel', any_state)

    router.message.register(type_voice, F.voice, DialogueStates.dialogue)
    router.message.register(type_file, F.audio, DialogueStates.dialogue)
    router.message.register(dial_settings, Command('settings'), DialogueStates.dialogue)
    router.message.register(dialogue, DialogueStates.dialogue)
    router.callback_query.register(
        settings_menu, SettingsCallback.filter(F.flag == '1'), DialogueStates.settings_menu)
    router.callback_query.register(
        transcribe_to_gpt, TranscribeCD.filter(F.flag == '1'), DialogueStates.dialogue)
    router.message.register(dial_change, DialogueStates.change_2)
    

    # router.message.register(start_dialogue, F.text == 'Начать диалог')
    # router.message.register(system_message, DialogueStates.system_message)
    # router.message.register(dialogue, DialogueStates.dialogue)
    # router.callback_query.register(clear, F.data == 'cancel', DialogueStates.dialogue)

    # router.message.register(start_transcribe, F.text == 'Сделать транскрипцию')
    # router.callback_query.register(set_type_file, F.data == 'file', TranscribesStates.sel_input_type)
    # router.message.register(type_file, TranscribesStates.type_file)
    # router.callback_query.register(set_type_voice, F.data == 'voice', TranscribesStates.sel_input_type)
    # router.message.register(type_voice, TranscribesStates.type_voice)
    


    # router.callback_query.register(censel_hendler, F.data == 'voice', any_state)
    # router.message.register(system_message, F.data == 'file', TranscribesStates.type_file)


    # # отправка очёта
    # router.message.register(start_report, IsRegisterFilter('Отправить отчёт о работе'))
    # # отчёт по работае на окладе
    # router.message.register(
    #     select_type_2, ReportStates.select_type, F.text == 'Почасовая')
    # router.callback_query.register(
    #     select_category_2, ReportStates.select_category_2, SalarysCD.filter(F.flag == '1'))
    # router.message.register(select_count_2, ReportStates.select_count_2)
    # router.message.register(send_report_2, ReportStates.select_comment_2)

    # # узнать сколько заработал сегодня
    # router.message.register(money_info_today, IsRegisterFilter('Узнать cумму на сегоденя'))
    # router.message.register(money_info_month, IsRegisterFilter('Узнать сумму в этом месяце'))

