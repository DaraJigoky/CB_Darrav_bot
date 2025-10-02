import datetime
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, ContentType
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.database.requests import set_account, get_account
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup,)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import app.keyboard as mkb

# Роутер диспетчера
menu = Router()


# Группа состояний на старте
class StartBot(StatesGroup):
    lobby = State()
    reg_log = State()
    reg_pass = State()
    reg_end = State()
    log_log = State()
    log_pass = State()
    log_acc_id = State()
    ask_flag_vld = State()
    ask_flag_admin = State()


# Группа состояний в аккаунте
class LoggedIn(StatesGroup):
    inacc = State()
    char_acc_id = State()
    char_char_id = State()
    char_list = State()
    char_acc = State()
    char_name = State()    
    char_create = State()

#[KeyboardButton(text='Владелец сообщества')],

vkbd_flag_vld = ReplyKeyboardMarkup(
    keyboard=[        
        [KeyboardButton(text='Обычный пользователь')],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

#[KeyboardButton(text='Админ')],
#[KeyboardButton(text='Продавец')],

vkbd_flag_admin = ReplyKeyboardMarkup(
    keyboard=[
        
        [KeyboardButton(text='Обычный пользователь')],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


@menu.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(StartBot.lobby)
    await message.answer('Добро пожаловать! Нажмите на кнопку "Войти" для входа в игру', reply_markup=mkb.menu_keyboard) 
    print('\ncmd_start')
    print(datetime.datetime.now())
    print(f'||| Пользователь {message.from_user.full_name} стартовал бота |||')
    print(f'||| Его tg_id: {message.from_user.id} |||')


@menu.message(StartBot.lobby, F.text == 'Войти')
async def cmd_ask_flag_vld(message: Message, state: FSMContext):
    await message.answer(
        'Вы являетесь владельцем сообщества с этим ботом?',
        reply_markup=vkbd_flag_vld
    )
    await state.set_state(StartBot.ask_flag_vld)

@menu.message(StartBot.ask_flag_vld)
async def process_flag_vld(message: Message, state: FSMContext):
    text = message.text.lower()
    if 'владелец' in text:
        flag_vld = 1
    else:
        flag_vld = 0

    await state.update_data(flag_vld=flag_vld)

    await message.answer(
        'Вы админ, продавец или обычный пользователь?',
        reply_markup=vkbd_flag_admin
    )

    await state.set_state(StartBot.ask_flag_admin)


@menu.message(StartBot.ask_flag_admin)
async def process_flag_admin(message: Message, state: FSMContext):
    text = message.text.lower()
    if 'админ' in text:
        flag_admin = 1
    else:
        flag_admin = 0
    #elif 'комиссар' in text:
        #flag_admin = 2
    #elif 'граф' in text:
        #flag_admin = 3 (Рава, Сева, Вай, Дара)
    
    data = await state.get_data()
    flag_vld = data.get('flag_vld', 0)

    tg_id = message.from_user.id

    # Запоминаем или обновляем аккаунт с флагами
    await set_account(tg_id, flag_admin=flag_admin, flag_vld=flag_vld)

    await message.answer('Вы успешно вошли!', reply_markup=mkb.menu_login_keyboard)

    # Обновляем состояние пользователя
    account = await get_account(tg_id)
    await state.update_data(log_acc_id=account.id, char_acc_id=account.id)
    await state.set_state(LoggedIn.inacc)

    print('\nprocess_flag_admin')
    print(datetime.datetime.now())
    print(f'||| Пользователь {message.from_user.full_name} вошёл с ролями flag_admin={flag_admin}, flag_vld={flag_vld} |||')
    print(f'||| Его tg_id: {tg_id} |||')


# Пока эта кнопка ничего не делает). Только пишет 'помощь'
@menu.message(StartBot.lobby, F.text == 'Помощь')
async def cmd_help_lobby(message: Message, state: FSMContext):
    await message.answer('Помощи нет, Бог не поможет.')
    await message.answer('Пока что пишите: https://t.me/DarJigoky')
    print('\ncmd_help_lobby')
    print(datetime.datetime.now())
    print(f'||| Пользователь {message.from_user.full_name} нажал Помощь |||')
    print(f'||| Его tg_id: {message.from_user.id} |||')
