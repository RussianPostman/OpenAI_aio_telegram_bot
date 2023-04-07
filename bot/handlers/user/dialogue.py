import os
from pprint import pprint
from httpx import Response, Timeout

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import types

from bot.handlers.keyboards.user_kb import DIALOGUE_KB
from bot.settings import OPENAI_API_KEY, TIMEOUT
from bot import openai_async


class DialogueStates(StatesGroup):
    """
    Состояния для диалога с GPT
    """
    system_message = State()
    dialogue = State()


async def start_dialogue(
        message: types.Message,
        state: FSMContext,
        ):
    await state.set_state(DialogueStates.system_message)
    await message.answer(
        'Введите системное сообщение',
        )


async def system_message(
        message: types.Message,
        state: FSMContext,
        ):
    await state.set_state(DialogueStates.dialogue)
    await state.update_data(m_history=[
        {"role": "system", "content": message.text},
        ])
    await message.answer(
        'Диалог начался',
        reply_markup=DIALOGUE_KB
        )


async def dialogue(
        message: types.Message,
        state: FSMContext,
        ):
    data: list = await state.get_data()
    m_history: list = data['m_history']
    pprint(m_history)
    m_history.append({"role": "user", "content": message.text})

    await SendMessage(
        text='Запрос к gpt-3.5-turbo отправлен',
        chat_id=message.from_user.id,
        reply_markup=DIALOGUE_KB
    )
    completion: Response = await openai_async.chat_complete(
        api_key=OPENAI_API_KEY,
        timeout=60,
        payload={
            'model': "gpt-3.5-turbo",
            'messages': m_history
            },
        )
    chat_response = completion.json()["choices"][0]["message"]['content']
    m_history.append({"role": "assistant", "content": chat_response})

    await SendMessage(
        text=chat_response,
        chat_id=message.from_user.id,
    )


async def clear(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(DialogueStates.system_message)
    state.update_data(m_history=[])
    await SendMessage(
        text='История запросов стёрта',
        chat_id=query.from_user.id,
    )



# async def select_product(
#         query: types.CallbackQuery,
#         callback_data: ProductCD,
#         state: FSMContext,
#         session_maker: sessionmaker
#         ):
#     await state.update_data(select_product=callback_data.name)
#     await state.set_state(ReportStates.select_role)
#     user_roles = await get_user_roles(
#         int(query.from_user.id),
#         session_maker)
#     await SendMessage(
#         text='Укажите роль в которой вы выполниля работу',
#         chat_id=query.from_user.id,
#         reply_markup=generate_roles_board(user_roles)
#         )


# async def select_role(
#         query: types.CallbackQuery,
#         callback_data: UserRoleCD,
#         state: FSMContext,
#         ):
#     await state.update_data(select_role=callback_data.name)
#     await state.set_state(ReportStates.select_count)
#     await SendMessage(
#         text='Укажите количество обработанной продукции (Цифрой)',
#         chat_id=query.from_user.id,
#         )


# async def select_count(
#         message: types.Message,
#         state: FSMContext,
#         ):
#     await state.update_data(select_count=message.text)
#     await state.set_state(ReportStates.select_marriage)
#     await SendMessage(
#         text='Укажите количество брака (Цифрой)',
#         chat_id=message.from_user.id,
#         )


# async def select_marriage(
#         message: types.Message,
#         state: FSMContext,
#         ):
#     await state.update_data(select_marriage=message.text)
#     await state.set_state(ReportStates.select_comment)
#     await SendMessage(
#         text='Оставьте комментарий',
#         chat_id=message.from_user.id,
#         reply_markup=EMPTY_BOARD
#         )


# async def send_report(
#         message: types.Message,
#         state: FSMContext,
#         session_maker: sessionmaker
#         ):

#     report_data = {}
#     data = await state.get_data()
#     await state.clear()
#     user: User = await get_user(message.from_user.id, session_maker)
#     product: Product = await get_product(
#         session_maker, data['select_category'], data['select_product'])

#     report_data['username'] = user.name
#     report_data['product'] = product.name
#     report_data['user_id'] = user.user_id
#     report_data['deta'] = datetime.today().strftime('%Y-%m-%d')
#     report_data['count'] = float(data.get('select_count'))
#     report_data['prise'] = (
#         float(product.__getattribute__(ROLE_NAMES[data['select_role']]))
#         )
#     report_data['salary'] = 0
#     report_data['comment'] = message.text
#     report_data['amount'] = report_data.get('prise') * report_data.get('count')
#     report_data['marriage'] = float(data.get('select_marriage'))

#     await create_report(report_data, session_maker)
#     await add_reports(report_data, message.from_user.id)
#     await SendMessage(
#         text=(f'Отчёт о работе над {product.name}-{report_data.get("prise")}р'
#               + f' на сумму {report_data.get("amount")}р отправлен'),
#         chat_id=message.from_user.id,
#         reply_markup=START_WORKER_BOARD
#         )
