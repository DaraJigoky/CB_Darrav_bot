from app.database.models import async_session
from app.database.models import Account, Character, Inventory
from sqlalchemy import select, update, delete, desc

from app.utils.utils import PreloadDicts # Импорт класса со списками словарей для прелоада


# Сбор всех функций прелоада в одну функцию для импорта и использования (чтоб не импортировать по одной отдельно)
async def preloads():
    await set_default_accounts()
    await set_default_characters()

# Автозагрузка наших акков с Дарой
async def set_default_accounts():
    async with async_session() as session:
        for account in PreloadDicts.accounts:
            exist = await session.scalar(select(Account).where(Account.tg_id == account['tg_id']))

            if not exist:
                session.add(Account(tg_id=account['tg_id'], login=account['flag_admin'], password=account['flag_vld']))
                await session.commit()
                

# Автозагрузка персонажей наших с Дарой
async def set_default_characters():
    async with async_session() as session:
        for character in PreloadDicts.characters:
            exist = await session.scalar(select(Character).where(Character.account == character['account']))

            if not exist:
                session.add(Character(account=character['account'], inventory=character['inventory'], name=character['name'], game_state=character['game_state']))
                await session.commit()

