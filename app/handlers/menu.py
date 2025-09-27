import datetime
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, ContentType
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.database.requests import set_account, get_account

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


# Группа состояний в аккаунте
class LoggedIn(StatesGroup):
    inacc = State()
    char_acc_id = State()
    char_char_id = State()
    char_list = State()
    char_acc = State()
    char_name = State()    
    char_create = State()



@menu.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """
    Описание:
    ---------
    
    Команда старта бота. Создаёт аккаунт пользователя и записывает его в таблицу Аккаунтов. Явно пока не будет использоваться, но может быть полезно в будущем. Так же сразу устанавливает состояние пользователю

    """
    
    await state.clear()
    await state.set_state(StartBot.lobby)
    await message.answer('Добро пожаловать! Нажмите на кнопку "Войти" для входа в игру', reply_markup=mkb.menu_keyboard)
    print('\ncmd_start')
    print(datetime.datetime.now())
    print(f'||| Пользователь {message.from_user.full_name} стартовал бота |||')
    print(f'||| Его tg_id: {message.from_user.id} |||')
    with open('app/logs.txt', 'a') as file:
        file.write('\n\ncmd_start ')
        file.write(str(datetime.datetime.now()))
        file.write(f' ||| Пользователь {message.from_user.full_name} стартовал бота |||')
        file.write(f' ||| Его tg_id: {message.from_user.id} |||')
   

@menu.message(StartBot.lobby, F.text == 'Войти')
async def cmd_log(message: Message, state: FSMContext):
    """
    Описание:
    ---------
    
    Вход в меню управления персонажами и тд

    """
    
    await state.set_state(LoggedIn.inacc)
    await message.answer('Вы вошли в систему!', reply_markup=mkb.menu_login_keyboard)


# Хэндлер доната
@menu.message(StartBot.lobby, F.text == 'Донат')
async def cmd_donat(message: Message, state: FSMContext):
    await message.answer('Благодарим за Ваш вклад в развитие проекта!')
    await message.answer('https://boosty.to/darada_okami/donate')
    print('\ncmd_donate')
    print(datetime.datetime.now())
    print(f'||| Пользователь {message.from_user.full_name} нажал Донат |||')
    print(f'||| Его tg_id: {message.from_user.id} |||')
    with open('app/logs.txt', 'a') as file:
        file.write('\n\ncmd_donate ')
        file.write(str(datetime.datetime.now()))
        file.write(f' ||| Пользователь {message.from_user.full_name} нажал Донат |||')
        file.write(f' ||| Его tg_id: {message.from_user.id} |||')


# Пока эта кнопка ничего не делает). Только пишет 'помощь'
@menu.message(StartBot.lobby, F.text == 'Помощь')
async def cmd_help_lobby(message: Message, state: FSMContext):
    await message.answer('Помощи нет, Бог не поможет.')
    await message.answer('Пока что пишите: https://t.me/DarJigoky')
    print('\ncmd_help_lobby')
    print(datetime.datetime.now())
    print(f'||| Пользователь {message.from_user.full_name} нажал Помощь |||')
    print(f'||| Его tg_id: {message.from_user.id} |||')
    with open('app/logs.txt', 'a') as file:
        file.write('\n\ncmd_help_lobby ')
        file.write(str(datetime.datetime.now()))
        file.write(f' ||| Пользователь {message.from_user.full_name} нажал Помощь |||')
        file.write(f' ||| Его tg_id: {message.from_user.id} |||')

