import datetime
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ContentType
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.database.requests import (get_account, get_account_by_id, set_character, get_character, set_char_ingame_state, get_all_characters_on_acc, 
                                  get_characters, get_character_on_create, delete_char_by_id, delete_char_inv_by_id)

import app.keyboard as mkb


# Роутер аккаунта
account = Router()


# Группа состояний при старте
class StartBot(StatesGroup):
    lobby = State()
    reg_log = State()
    reg_pass = State()
    reg_end = State()
    log_log = State()
    log_pass = State()
    log_acc_id = State()


# Создаём состояние "залогинен"
class LoggedIn(StatesGroup):
    inacc = State()
    char_acc_id = State()
    char_char_id = State()
    char_list = State()
    char_acc = State()
    char_name = State()
    char_create = State()


# Группа состояний в игре
class InGame(StatesGroup):
    ingame = State()
    game_char_id = State()
    var1 = State()
    var2 = State()


# Проверка в игре ли я. Возвращает пользователю его данные
@account.message(LoggedIn.inacc, F.text == 'Помощь')
async def cmd_loggedin_amihere(message: Message, state: FSMContext):
    data = await state.get_data() 
    print(data['char_acc_id'])
    await message.answer('Помощи нет, Бог не поможет.')
    await message.answer('Пока что пишите: https://t.me/DarJigoky')
    print('\ncmd_loggedin_amihere')
    print(datetime.datetime.now())
    print(f'||| Пользователь {message.from_user.full_name} нажал кнопку Помощь |||')
    print(f'||| Его acc_id: {data['char_acc_id']} |||')

# Дописать как чатовую клавиатуру
#


# Кнопка выхода в стартовое меню
@account.message(LoggedIn.inacc, F.text == 'Выйти')
async def cmd_loggedin_exit(message: Message, state: FSMContext):
    await message.answer('Вы вышли из аккаунта', reply_markup=mkb.menu_keyboard)
    data = await state.get_data()
    acc = await get_account_by_id(data['char_acc_id'])
    characters = await get_all_characters_on_acc(acc.id)
    for character in characters:
        await set_char_ingame_state(character.id, char_state=0)
    await state.set_state(StartBot.lobby)
    print('\ncmd_loggedin_exit')
    print(datetime.datetime.now())
    print(f'||| Пользователь {message.from_user.full_name} нажал кнопку Выйти |||')
    print(f'||| Его acc_id: {data['char_acc_id']} |||')


# Ловим ID пользователя и на его основе получаем список его персонажей
@account.message(LoggedIn.inacc, F.text == 'Персонажи')
async def cmd_loggedin_char_list(message: Message, state: FSMContext):
    account = await get_account(message.from_user.id)
    await message.answer('Список персонажей', reply_markup=await mkb.char_list(account.id))
    print('\ncmd_loggedin_char_list')
    print(datetime.datetime.now())
    print(f'||| Пользователь {message.from_user.full_name} нажал кнопку Персонажи |||')
    print(f'||| Его acc_id: {account.id} |||')


# Получаем ответ от кнопки персонажа, оттуда же его ID и показываем его статус и кнопку играть
@account.callback_query(LoggedIn.inacc, F.data.startswith('character_'))
async def character_list(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    charloc = await get_character(callback.data.split('_')[1])
    await state.update_data(char_char_id=callback.data.split('_')[1])
    await callback.answer('')
    await callback.message.answer(f'Имя персонажа: {charloc.name}', reply_markup=mkb.char_play)
    print('\ncharacter_list')
    print(datetime.datetime.now())
    print(f'||| Пользователь {callback.from_user.full_name} вывел информацию о персонаже {charloc.id} |||')
    print(f'||| Его acc_id: {data['char_acc_id']} |||')


# Кнопка запускает нас в игру и передаёт ID персонажа вдобавок
@account.callback_query(LoggedIn.inacc, F.data == 'play')
async def character_list_play(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pers = await get_character(data['char_char_id'])
    await callback.answer('')
    await callback.message.answer(f'Вы вошли в игру', reply_markup=mkb.ingame_keyboard)
    await set_char_ingame_state(data['char_char_id'], char_state=1)
    await state.set_state(InGame.ingame)
    await state.update_data(game_char_id=data['char_char_id'])
    print('\ncharacter_list_play')
    print(datetime.datetime.now())
    print(f'||| Пользователь {callback.from_user.full_name} нажал кнопку играть на игроке {data['char_char_id']} |||')
    print(f'||| Его acc_id: {data['char_acc_id']} |||')


# Удаление персонажа при нажатии кнопки delete
@account.callback_query(LoggedIn.inacc, F.data == 'delete')
async def character_list_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    char = await get_character(data['char_char_id'])
    await delete_char_by_id(char.id)
    await delete_char_inv_by_id(char.money)
    acc = await get_account_by_id(data['char_acc_id'])
    await callback.answer('')
    await callback.message.answer('Персонаж удален! Ваши персонажи:', reply_markup=await mkb.char_list(acc.id))
    print('\ncharacter_list_delete')
    print(datetime.datetime.now())
    print(f'||| Пользователь {callback.from_user.full_name} нажал кнопку Удалить персонажа с айди: {char.id} {char.name} |||')
    print(f'||| Его acc_id: {data['char_acc_id']} |||')


# Кнопка вызывает цепочку создания персонажа
@account.message(LoggedIn.inacc, F.text == 'Создать персонажа')
async def cmd_loggedin_create_char(message: Message, state: FSMContext):
    count = 0
    data = await state.get_data()
    characters = await get_characters(data['char_acc_id'])    
    for character in characters:
        count += 1
    if count < 1:        
        await state.set_state(LoggedIn.char_name)
        await message.answer('Введите имя вашего персонажа:')
        print('\ncmd_loggedin_create_char')
        print(datetime.datetime.now())
        print(f'||| Пользователь {message.from_user.full_name} нажал кнопку Создать персонажа |||')
        print(f'||| Его acc_id: {data['char_acc_id']} |||')
    if count >= 1:
        await message.answer('Максимальное количество персонажей - 1!', reply_markup=mkb.menu_login_keyboard)
        



# Ловит имя персонажа при создании
@account.message(LoggedIn.char_name)
async def cmd_loggedin_char_name(message: Message, state: FSMContext):
    if message.content_type == ContentType.TEXT and message.text.isalpha() == True:
        await state.update_data(char_name=message.text)
        data = await state.get_data()
        await state.set_state(LoggedIn.char_create)
        await message.answer(f'Статус вашего персонажа:\nИмя: {data['char_name']}', reply_markup=mkb.menu_reg_end)
    else:
        data = await state.get_data()
        await message.answer('Недопустимое имя. Повторите попытку')
    print('\ncmd_loggedin_char_desc')
    print(datetime.datetime.now())
    print(f'||| Пользователь {message.from_user.full_name} завершает создание персонажа |||')
    print(f'||| Его acc_id: {data['char_acc_id']} |||')


# Собираем дату и создаём в итоге персонажа
@account.message(LoggedIn.char_create, F.text == 'Завершить')
async def cmd_loggedin_char_create(message: Message, state: FSMContext):
    data = await state.get_data()
    account = await get_account(message.from_user.id)
    await set_character(account.id, data['char_name'])
    new = await get_character_on_create(data['char_name'])
    await message.answer('Создание персонажа завершено!', reply_markup=mkb.menu_login_keyboard)
    await state.set_state(LoggedIn.inacc)
    print('\ncmd_loggedin_char_create')
    print(datetime.datetime.now())
    print(f'||| Пользователь {message.from_user.full_name} завершил создание персонажа, его id: {new.id} |||')
    print(f'||| Его acc_id: {data['char_acc_id']} |||')


# Отмена создания персонажа если что то не так было введено
@account.message(LoggedIn.char_create, F.text == 'Отмена')
async def cmd_loggedin_char_create_cancel(message: Message, state: FSMContext):
    await message.answer('Вы отменили создание персонажа', reply_markup=mkb.menu_login_keyboard)
    await state.set_state(LoggedIn.inacc)
    data = await state.get_data()
    print('\ncmd_loggedin_char_create_cancel')
    print(datetime.datetime.now())
    print(f'||| Пользователь {message.from_user.full_name} отменил создание персонажа |||')
    print(f'||| Его acc_id: {data['char_acc_id']} |||')
