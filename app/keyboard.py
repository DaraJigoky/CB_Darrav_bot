from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup,)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.requests import get_characters, get_item_by_id, get_shop_items


# Клавиатура главного меню на старте
menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Войти'), KeyboardButton(text='Помощь')]
   
],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню',
)

# Клавиатура залогиненного пользователя
menu_login_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Персонажи'), KeyboardButton(text='Создать персонажа')],
    [KeyboardButton(text='Выйти'), KeyboardButton(text='Помощь')]
],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню',
)
# Клавиатура залогиненного пользователя
menu_login_keyboard1 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Персонажи'), KeyboardButton(text='Помощь')],
    [KeyboardButton(text='Выйти')]
],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню',
)


# Клавиатура с кнопкой отмены, где это нужно
menu_reg_end = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Завершить')],
    [KeyboardButton(text='Отмена')],
],
    resize_keyboard=True,
)


# Кнопка играть при выборе персонажа
char_play = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Играть', callback_data='play')],
    [InlineKeyboardButton(text='Удалить', callback_data='delete')],
])


# Тестовая клавиатура в игре
ingame_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Персонаж'), KeyboardButton(text='Донат создателю')],
    [KeyboardButton(text='Помощь'), KeyboardButton(text='Выйти')] 
],
    resize_keyboard=True,
    input_field_placeholder='Вы в игре',
)

# Клавиатура персонажа
ingame_char = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Магазин', callback_data='ingame_loc_shop')],
    [InlineKeyboardButton(text='Инвентарь', callback_data='ingame_char_inventory')],
])

# Список персонажей на аккаунте
async def char_list(account):
    all_characters = await get_characters(account)
    keyboard = InlineKeyboardBuilder()

    for character in all_characters:
        keyboard.add(InlineKeyboardButton(text=character.name, callback_data=f'character_{character.id}'))
    
    return keyboard.adjust(1).as_markup()



# Клавиатура инвентаря персонажа
async def ingame_char_inventory(items):
    try:
        item_list = [int(item) for item in (items.split('_'))]
        keyboard = InlineKeyboardBuilder()
        items_in_keyboard = []

        for item in item_list:
            if item in items_in_keyboard:
                pass
            else:
                items_in_keyboard.append(item)
                btn = await get_item_by_id(item)
                keyboard.add(InlineKeyboardButton(text=f'{item_list.count(item)} {btn.name}', callback_data=f'ingame_char_inventory_item_{btn.id}'))
    
        return keyboard.adjust(1).as_markup()
    except:
        pass


# Клавиатура ассортимента магазина
async def ingame_shop_items(shop_id):
    try:
        shop = await get_item_by_id(shop_id)
        shop_items = shop.items
        items_id = [int(item) for item in (shop_items.split('_'))]
        keyboard = InlineKeyboardBuilder()

        for item_id in items_id:
            btn = await get_item_by_id(item_id)
            keyboard.add(InlineKeyboardButton(text=f'{btn.name}', callback_data=f'ingame_shop_keyboard_item_{btn.id}'))
    
        return keyboard.adjust(1).as_markup()
    except:
        pass


# Инлайн кнопка купить в предмете в магазине
async def ingame_loc_shop_item_buy(item_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Купить', callback_data=f'ingame_shop_item_buy_pressed_{item_id}'))

    return keyboard.adjust(1).as_markup()


# Дописать как чатовую клавиатуру с реквестом из файла
#async def cmd_help_lobby(message: Message, state: FSMContext):
    #Help = await help_cmd
    #keyboard = InlineKeyboardBuilder()

    #for character in all_characters:
        #keyboard.add(InlineKeyboardButton(text=character.first_name, callback_data=f'character_{character.id}'))
    
    #return keyboard.adjust(1).as_markup()