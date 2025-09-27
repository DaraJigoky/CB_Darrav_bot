from sqlalchemy import ForeignKey, String, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=False)


async_session = async_sessionmaker(engine)


# Наследуемся отсюда
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Таблица аккаунтов
class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    login: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(20))


# Таблица локаций
class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(String(600))
    transport: Mapped[str] = mapped_column(String(50))
    flag: Mapped[int] = mapped_column(nullable=False)
    art: Mapped[str] = mapped_column(String(600), nullable=True)


class Char_location(Base):
    __tablename__ = 'char_locations'

    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    name: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(String(600))
    transport: Mapped[str] = mapped_column(String(50))
    flag: Mapped[int] = mapped_column(nullable=False)
    art: Mapped[str] = mapped_column(String(600), nullable=True)


# Прототип таблицы персонажей
class Character(Base):
    __tablename__ = 'characters'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    account: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    inventory: Mapped[int] = mapped_column(ForeignKey('inventories.id'), nullable=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    race: Mapped[int] = mapped_column(ForeignKey('race.id'))
    age: Mapped[str] = mapped_column(String(4))
    location: Mapped[int] = mapped_column(ForeignKey('locations.id'))
    description: Mapped[str] = mapped_column(String(600))
    game_state: Mapped[int] = mapped_column()
    art: Mapped[str] = mapped_column(String(600), nullable=True)
    
    
# Таблица рас. Пока не используется
class Race(Base):
    __tablename__ = 'race'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(String(600))
    art: Mapped[str] = mapped_column(String(600), nullable=True)


# Список предметов в игре. 
class ItemList(Base):
    __tablename__ = 'items'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(String(600))


# Модель инвентаря
class Inventory(Base):
    __tablename__ = 'inventories'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_char: Mapped[int] = mapped_column(ForeignKey('characters.id'), nullable=False)
    items: Mapped[str] = mapped_column(String(600), nullable=True)
    money: Mapped[str] = mapped_column(String(10), default='0')


# Модель магазина
class Shop(Base):
    __tablename__ = 'shops'

    id: Mapped[int] = mapped_column(primary_key=True)
    items: Mapped[str] = mapped_column(String(600), nullable=True)


# Модель магазина доната
class Donat_shop(Base):
    __tablename__ = 'donat_shop'

    id: Mapped[int] = mapped_column(primary_key=True)
    items: Mapped[str] = mapped_column(String(600), nullable=True)
    price: Mapped[str] = mapped_column(String(10), default='0')


# Функция инициализации новых таблиц, если их нет
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
