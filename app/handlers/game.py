from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ContentType
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.database.requests import (get_character, get_account_by_id, set_char_ingame_state, get_inventory_by_char_id, set_new_item_to_char_inv)

import app.keyboard as mkb
from app.utils.utils import censor_check


# Роутер аккаунта
game = Router()


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


# Возвращает в консоль ID игрока
@game.message(InGame.ingame, F.text == 'Персонаж')
async def cmd_ingame_char(message: Message, state: FSMContext):
    data = await state.get_data()
    char = await get_character(data['game_char_id'])
    await message.answer(f'{char.first_name} {char.last_name} id:{char.id}', reply_markup=mkb.ingame_char)
    

# Выводит инвентарь персонажа при нажатии кнопки Инвентарь
@game.callback_query(InGame.ingame, F.data == 'ingame_char_inventory')
async def cmd_ingame_char_inventory(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    inventory = await get_inventory_by_char_id(data['game_char_id'])
    await callback.answer('')
    await callback.message.answer(f'Ваш инвентарь:\nВаши деньги: {inventory.money}', reply_markup=await mkb.ingame_char_inventory(inventory.items))


# Выход в меню аккаунта
@game.message(InGame.ingame, F.text == 'Выйти из игры')
async def cmd_ingame_logout(message: Message, state: FSMContext):
    await message.answer('Вы вышли из игры', reply_markup=mkb.menu_login_keyboard)
    data = await state.get_data()
    await set_char_ingame_state(data['game_char_id'], char_state=0)
    await state.set_state(LoggedIn.inacc)


# Тестовый хэндлер магазина
@game.callback_query(InGame.ingame, F.data == 'ingame_loc_shop')
async def cmd_ingame_loc_shop(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Добро пожаловать в магазин! Желаете ли что нибудь купить?', reply_markup=await mkb.ingame_shop_items(1))


# Выводит прикол при нажатии кнопки Купить в магазине на предмете
@game.callback_query(InGame.ingame, F.data.startswith('ingame_shop_item_buy_pressed_'))
async def cmd_ingame_loc_shop_choose_buy(callback: CallbackQuery, state = FSMContext):
    #item = await get_item_by_id(int(callback.data.split('_')[5]))
    data = await state.get_data()
    inventory = await get_inventory_by_char_id(data['game_char_id'])
    try: 
        items = inventory.items.split('_')
        items.append(callback.data.split('_')[5])
        new_items = '_'.join(items)
    except: 
        new_items = callback.data.split('_')[5]
    await set_new_item_to_char_inv(new_items, inventory.id)
    await callback.answer(f'Предмет добавлен в инвентарь. Ваш баланс: {inventory.money}')
    await callback.message.answer(f'Услышал тебя родной\nДобавляю предмет тебе в инвентарь')
    await callback.message.answer_animation(animation='CgACAgQAAxkBAAIY4Wb-Za-vyrvjVvGYNltqVhOqwVwlAAKgBQACtYtkUgbeO6_QSD3oNgQ')

