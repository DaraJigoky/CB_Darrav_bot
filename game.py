from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ContentType
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.database.requests import (get_character, get_char_location, get_characters_in_location, get_location, set_char_location, 
get_account_by_id, set_char_ingame_state, get_inventory_by_char_id, get_item_by_id, set_new_item_to_char_inv, get_tg_id_by_char)

import app.keyboards.menu_keyboard as mkb
from app.utils.utils import utils_send_message
from app.utils.utils import censor_check, censor_pack


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
    char_surname = State()
    char_age = State()
    char_race = State()
    char_loc = State()
    char_desc = State()
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
    

# Выводит описание персонажа при нажатии кнопки Описание
@game.callback_query(InGame.ingame, F.data == 'ingame_char_description')
async def cmd_ingame_char_info(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    char = await get_character(data['game_char_id'])
    await callback.answer('')
    await callback.message.answer(f'Имя: {char.first_name}\nФамилия: {char.last_name}\nВозраст: {char.age}\nРаса: {char.race}\nОписание: {char.description}')


# Выводит инвентарь персонажа при нажатии кнопки Инвентарь
@game.callback_query(InGame.ingame, F.data == 'ingame_char_inventory')
async def cmd_ingame_char_inventory(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    inventory = await get_inventory_by_char_id(data['game_char_id'])
    await callback.answer('')
    await callback.message.answer(f'Ваш инвентарь:\nВаши деньги: {inventory.money}', reply_markup=await mkb.ingame_char_inventory(inventory.items))


# Выводит описание предмета персонажа из его инвентаря если тыкнуть по предмету
@game.callback_query(InGame.ingame, F.data.startswith('ingame_char_inventory_item_'))
async def cmd_ingame_char_inventory(callback: CallbackQuery):
    item = await get_item_by_id(int(callback.data.split('_')[4]))
    await callback.answer('')
    await callback.message.answer(f'Айдишник предмета: {item.id}\nНазвание: {item.name}\nОписание предмета: {item.description}')


# Выход в меню аккаунта
@game.message(InGame.ingame, F.text == 'Выйти из игры')
async def cmd_ingame_logout(message: Message, state: FSMContext):
    await message.answer('Вы вышли из игры', reply_markup=mkb.menu_login_keyboard)
    data = await state.get_data()
    await set_char_ingame_state(data['game_char_id'], char_state=0)
    await state.set_state(LoggedIn.inacc)


# Флаги: 1 - все локи, 2 - магазины вещей, 3 - банк, 4 - магазин продуктов, 5 - 18+ локи
# Выводит описание текущей локации и кнопки Перемещение Игроки рядом Магазин
@game.message(InGame.ingame, F.text == 'Локация')
async def cmd_ingame_location(message: Message, state: FSMContext):
    data = await state.get_data()
    char = await get_character(data['game_char_id'])
    loc = await get_location(char.location)
    if loc.flag == 1:
        await message.answer(f'Локация: {loc.name}\nОписание: {loc.description}', reply_markup=mkb.ingame_loc)
    if loc.flag == 2:
        await message.answer(f'Локация: {loc.name}\nОписание: {loc.description}\nМагазин', reply_markup=mkb.ingame_loc_shop)
    if loc.flag == 3:
        await message.answer(f'Локация: {loc.name}\nОписание: {loc.description}\nБанк', reply_markup=mkb.ingame_loc_shop)
    if loc.flag == 4:
        await message.answer(f'Локация: {loc.name}\nОписание: {loc.description}\nМагазин продуктов', reply_markup=mkb.ingame_loc_shop)
    if loc.flag == 5:
        await message.answer(f'Локация: {loc.name}\nОписание: {loc.description}', reply_markup=mkb.ingame_loc)


# Список персонажей на этой локации
@game.callback_query(InGame.ingame, F.data == 'ingame_loc_char_here')
async def cmd_ingame_charhere(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    char = await get_character(data['game_char_id'])
    await callback.answer('')
    await callback.message.answer('Персонажи рядом:', reply_markup=await mkb.char_here(char.location))


# Выводит описание персонажа при нажатии на ник
#@game.callback_query(InGame.ingame, F.data.startswith('ingame_info_keyboard_char_'))
#async def cmd_ingame_char_info(callback: CallbackQuery):
    #char = await get_char_by_id(int(callback.data.split('_')[4]))
    #await callback.answer('')
    #await callback.message.answer(f'Имя: {char.first_name}\nФамилия: {char.last_name}\nВозраст: {char.age}\nРаса: {char.race}\nОписание: {char.description}'
    #, reply_markup=await mkb.ingame_info_keyboard_char(char.id))


# Список локаций для перемещения
@game.callback_query(InGame.ingame, F.data == 'ingame_loc_transport')
async def cmd_ingame_char_transport(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    char = await get_character(data['game_char_id'])
    loc = await get_char_location(char.location)
    await callback.answer('')
    await callback.message.answer('Список локаций для перехода:', reply_markup=await mkb.char_transport(loc.transport))


# Тестовый хэндлер магазина
@game.callback_query(InGame.ingame, F.data == 'ingame_loc_shop')
async def cmd_ingame_loc_shop(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Добро пожаловать в магазин! Желаете ли что нибудь купить?', reply_markup=await mkb.ingame_shop_items(1))


# Выводит описание предмета в магазине при нажатии
@game.callback_query(InGame.ingame, F.data.startswith('ingame_shop_keyboard_item_'))
async def cmd_ingame_loc_shop_choose(callback: CallbackQuery):
    item = await get_item_by_id(int(callback.data.split('_')[4]))
    await callback.answer('')
    await callback.message.answer(f'Айди предмета: {item.id}\nНазвание: {item.name}\nОписание предмета: {item.description}\nХВАТАЙ ПОКА БЕСПЛАТНО!!!', reply_markup=await mkb.ingame_loc_shop_item_buy(item.id))


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


# Выбранная для перемещения локация
@game.callback_query(InGame.ingame, F.data.startswith('location_'))
async def cmd_ingame_trans_list(callback: CallbackQuery, state: FSMContext):
    location = await get_location(callback.data.split('_')[1])
    await state.update_data(var1=callback.data.split('_')[1])
    data = await state.get_data()
    await callback.answer('')
    await callback.message.answer(f'Локация: {location.name}\nОписание: {location.description}\nID: {data['var1']}\nПерсонаж ID: {data['game_char_id']}', reply_markup=mkb.char_trans)


# Переход на другую локацию
@game.callback_query(InGame.ingame, F.data == 'transport')
async def cmd_trans_char(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    char = await get_character(data['game_char_id'])
    loc = await get_location(data['var1'])
    players = await get_characters_in_location(char.location)
    for player in players:
        if player.game_state == 1 and player.account != char.account:
            acc = await get_account_by_id(player.account)
            await callback.bot.send_message(chat_id=acc.tg_id, text=f'Игрок {char.first_name} {char.last_name} покинул локацию')
    await set_char_location(data['game_char_id'], loc.id)
    players = await get_characters_in_location(loc.id)
    for player in players:
        if player.game_state == 1 and player.account != char.account:
            acc = await get_account_by_id(player.account)
            await callback.bot.send_message(chat_id=acc.tg_id, text=f'Игрок {char.first_name} {char.last_name} появился на локации')
    await callback.answer('')
    await callback.message.answer(f'Вы перешли на другую локацию\nЛокация: {loc.name}\nОписание: {loc.description}', reply_markup=mkb.ingame_keyboard)


# Личное общение между персонажами (+ фото, видео, гиф, стикеры)
@game.message(InGame.ingame, Command('ls'))
async def cmd_private_message(message: Message, state: FSMContext, command: CommandObject):
    data = await state.get_data()
    char = await get_character(data['game_char_id'])
    player = await get_tg_id_by_char(command.args.split()[0])
    player_prov = await get_character(command.args.split()[0])
    bebra = command.args.split()
    bebra.pop(0)
    text_to_send = ' '.join(bebra)
    # Для отладки присылает отправившему тип контента сообщения
    #await message.answer(f'{message.content_type}')
    #await message.answer(f'...')
    if player_prov.game_state == 1 and player_prov.account != char.account:
        await utils_send_message(message, player, char.first_name, char.last_name, flag=1, command_args=text_to_send)
    else:
        pass


# Общение между персонажами (+ фото, видео, гиф, стикеры)
@game.message(InGame.ingame)
async def cmd_echogame(message: Message, state: FSMContext):
    data = await state.get_data()
    char = await get_character(data['game_char_id'])
    players = await get_characters_in_location(char.location)
    # Для отладки присылает отправившему тип контента сообщения
    #await message.answer(f'{message.content_type}')
    for player in players:
        if player.game_state == 1 and player.account != char.account:
            acc = await get_account_by_id(player.account)
            await utils_send_message(message, acc.tg_id, char.first_name, char.last_name)
        else:
            pass


# /лс(!лс) id Сообщение 


# Обработка мата
#maty = ['mat', 'mat2'..] # здесь пишешь все маты

#@game.message(InGame.ingame, F.text == maty)
#async def filter(msg: types.Message):
    #is_mat = None
    #for mat in maty:
        #if mat in msg.text.lower(): # lower() делает все буквы прописными
            #is_mat = True
            #break
    #if is_mat:
        #await msg.reply('не матерись!') # здесь действие если есть маты в тексте
