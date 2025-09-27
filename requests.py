from app.database.models import async_session
from app.database.models import Account, Character, Location, Inventory, ItemList, Shop, Race
from sqlalchemy import select, update, delete, desc
from sqlalchemy.orm.query import Query


# Реквест проверки аккаунта. Если существует, то да. Если нету, то добавляет запись в базу данных
# Принимает tg id, логин и пароль аккаунта
async def set_account(tg_id, login, password):
    async with async_session() as session:
        account = await session.scalar(select(Account).where(Account.tg_id == tg_id))

        if not account:
            session.add(Account(tg_id=tg_id, login=login, password=password))
            await session.commit()


# Создание персонажа при его создании
async def set_character(account, first_name, last_name, race, age, location, description):
    async with async_session() as session:
        session.add(Character(account=account, first_name=first_name, last_name=last_name, race=race, age=age, location=location, description=description, game_state=0))
        await session.commit()


# Создание инвенторя персонажа при создании или нет
async def set_inventory(char_id):
    async with async_session() as session:
        session.add(Inventory(id_char=char_id, money='0'))
        await session.commit()


# Создает новый инвентарь игроку при его создании
async def set_inventory_to_new_player(id):
    async with async_session() as session:
        await session.execute(update(Character).where(Character.id == id).values(inventory=id))
        await session.commit()


# Установить локацию персонажа (при перемещении персонажа)
async def set_char_location(char_id, loc_id):
    async with async_session() as session:
        await session.execute(update(Character).where(Character.id == char_id).values(location=loc_id))
        await session.commit()


# Устанавливает игроку игровой статус 0 или 1 когда где нужно (вошел вышел из игры)
async def set_char_ingame_state(char_id, char_state):
    async with async_session() as session:
        await session.execute(update(Character).where(Character.id == char_id).values(game_state=char_state))
        await session.commit()


# Добавление предмета по его айди в инвентарь игрока
async def set_new_item_to_char_inv(new_items, inv_id):
    async with async_session() as session:
        await session.execute(update(Inventory).where(Inventory.id == inv_id).values(items=new_items))
        await session.commit()


# Удаление персонажа с аккаунта
async def delete_char_by_id(char_id):
    async with async_session() as session:
        await session.execute(delete(Character).where(Character.id == char_id))
        await session.commit()


# Удаление инвентаря персонажа
async def delete_char_inv_by_id(inv_id):
    async with async_session() as session:
        await session.execute(delete(Inventory).where(Inventory.id_char == inv_id))
        await session.commit()


# Реквест на выдачу данных об аккаунте. По tg id выдаёт данные
async def get_account(tg_id):
    async with async_session() as session:
        return await session.scalar(select(Account).where(Account.tg_id == tg_id))
    

# Получить акк по его акк id
async def get_account_by_id(id):
    async with async_session() as session:
        return await session.scalar(select(Account).where(Account.id == id))


# Реквест для получения tg id по игроку в игре (для лс)
async def get_tg_id_by_char(char_id):
    async with async_session() as session:
        char = await session.scalar(select(Character).where(Character.id == char_id))
        acc = await session.scalar(select(Account).where(Account.id == char.account))
        return acc.tg_id


# tg_id, account, name, surname, race, age, loc, desc
async def get_character(id):
    async with async_session() as session:
        return await session.scalar(select(Character).where(Character.id == id))


# Получить персонажа при создании персонажа по его описанию
async def get_character_on_create(desc):
    async with async_session() as session:
        return await session.scalar(select(Character).where(Character.description == desc))


# Получить всех персонажей с нами на локации и не важно какой гейм стейт
async def get_all_characters_on_acc(acc):
    async with async_session() as session:

        return await session.scalars(select(Character).where(Character.account == acc))
        #players = await get_character(char.id)
        #for player in players:
            #if player.game_state == 1 and player.account != char.account:
            #acc = await get_account_by_id(player.account)
            #Если персонаж в сети прибав, к его нику "🌇"
            #Если персонаж не в сети прибав к нику "🌃"


#Получить... Все расы?
async def get_all_race():
    async with async_session() as session:
        return await session.scalars(select(Race))


# Получить персонажей на аккаунте
async def get_characters(account):
    async with async_session() as session:
        return await session.scalars(select(Character).where(Character.account == account))


# Получить персонажей на локации
async def get_characters_in_location(location):
    async with async_session() as session:
        return await session.scalars(select(Character).where(Character.location == location))
    

# Получить локацию где игрок
async def get_char_location(char_loc):
    async with async_session() as session:
        return await session.scalar(select(Location).where(Location.id == char_loc))


# Получить локацию
async def get_location(location):
    async with async_session() as session:
        return await session.scalar(select(Location).where(Location.id == location))


# Получить инвентарь персонажа по его персонажа айди
async def get_inventory_by_char_id(char_id):
    async with async_session() as session:
        return await session.scalar(select(Inventory).where(Inventory.id_char == char_id))
    

# Получить предмет по его id
async def get_item_by_id(item_id):
    async with async_session() as session:
        return await session.scalar(select(ItemList).where(ItemList.id == item_id))


# Получить ассортимент магазина по его id магазина
async def get_shop_items(shop_id):
    async with async_session() as session:
        return await session.scalar(select(Shop).where(Shop.id == shop_id))

