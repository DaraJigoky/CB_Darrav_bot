from app.database.models import async_session
from app.database.models import Account, Character, Location, Inventory, ItemList, Shop, Race
from sqlalchemy import select, update, delete, desc

from app.utils.utils import PreloadDicts # Импорт класса со списками словарей для прелоада


# Сбор всех функций прелоада в одну функцию для импорта и использования (чтоб не импортировать по одной отдельно)
async def preloads():
    await set_default_locations()
    await set_default_accounts()
    await set_default_characters()
    await set_default_inventories()
    await set_default_items()
    await set_default_items_in_shop()
    await set_default_race()


# Автозагрузка наших акков с Дарой
async def set_default_accounts():
    async with async_session() as session:
        for account in PreloadDicts.accounts:
            exist = await session.scalar(select(Account).where(Account.tg_id == account['tg_id']))

            if not exist:
                session.add(Account(tg_id=account['tg_id'], login=account['login'], password=account['password']))
                await session.commit()


# Автозагрузка локаций
async def set_default_locations():
    async with async_session() as session:
        for location in PreloadDicts.locations:
            exist = await session.scalar(select(Location).where(Location.name == location['name']))

            if not exist:
                session.add(Location(name=location['name'], description=location['description'], transport=location['transport'], flag=location['flag']))
                await session.commit()


# Автозагрузка рас
async def set_default_race():
    async with async_session() as session:
        for race in PreloadDicts.races:
            exist = await session.scalar(select(Race).where(Race.name == race['name']))

            if not exist:
                session.add(Race(name=race['name'], description=race['description']))
                await session.commit()


# Автозагрузка персонажей наших с Дарой
async def set_default_characters():
    async with async_session() as session:
        for character in PreloadDicts.characters:
            exist = await session.scalar(select(Character).where(Character.account == character['account']))

            if not exist:
                session.add(Character(account=character['account'], inventory=character['inventory'], first_name=character['first_name'], last_name=character['last_name'], race=character['race'], age=character['age'], location=character['location'], description=character['description'], game_state=character['game_state']))
                await session.commit()


# Автозагрузка инвентарей наших с Дарой
async def set_default_inventories():
    async with async_session() as session:
        for inventory in PreloadDicts.inventories:
            exist = await session.scalar(select(Inventory).where(Inventory.id_char == inventory['char_id']))

            if not exist:
                session.add(Inventory(id_char=inventory['char_id'], items=inventory['items']))
                await session.commit()


# Автозагрузка предметов
async def set_default_items():
    async with async_session() as session:
        for item in PreloadDicts.items:
            exist = await session.scalar(select(ItemList).where(ItemList.description == item['description']))

            if not exist:
                session.add(ItemList(name=item['name'], description=item['description']))
                await session.commit()


# Автозагрузка ассортиментов магазинов
async def set_default_items_in_shop():
    async with async_session() as session:
        for shop in PreloadDicts.shops:
            exist = await session.scalar(select(Shop).where(Shop.items == shop['items']))

            if not exist:
                session.add(Shop(items=shop['items']))
                await session.commit()
