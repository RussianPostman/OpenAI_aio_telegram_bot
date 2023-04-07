from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import any_state

from .commands import censel_hendler, start
from .user.dialogue import start_dialogue, system_message, dialogue, clear, \
    DialogueStates
from .user.transcribes import TranscribesStates, start_transcribe, \
    set_type_file, type_file, set_type_voice, type_voice
__all__ = ['register_user_commands']


def register_user_commands(router: Router) -> Router:
    """
    Зарегистрировать хендлеры пользователя
    :param router:
    """
    router.message.register(start, CommandStart())

    # хендлеры выхода из машины состояний
    router.message.register(censel_hendler, Command('cancel'), any_state)
    router.message.register(censel_hendler, F.text.casefold().lower() == 'отмена', any_state)
    router.callback_query.register(censel_hendler, F.data == 'cancel', any_state)

    router.message.register(start_dialogue, F.text == 'Начать диалог')
    router.message.register(system_message, DialogueStates.system_message)
    router.message.register(dialogue, DialogueStates.dialogue)
    router.callback_query.register(clear, F.data == 'cancel', DialogueStates.dialogue)

    router.message.register(start_transcribe, F.text == 'Сделать транскрипцию')
    router.callback_query.register(set_type_file, F.data == 'file', TranscribesStates.sel_input_type)
    router.message.register(type_file, TranscribesStates.type_file)
    router.callback_query.register(set_type_voice, F.data == 'voice', TranscribesStates.sel_input_type)
    router.message.register(type_voice, TranscribesStates.type_voice)
    


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

