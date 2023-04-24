from aiogram.fsm.state import StatesGroup, State


class DialogueStates(StatesGroup):
    """
    Состояния для диалога с GPT
    """
    dialogue = State()
    settings_menu = State()
    change_2 = State()
