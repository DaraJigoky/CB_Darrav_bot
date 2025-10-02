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
    tg_id = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    flag_admin: Mapped[int] = mapped_column(nullable=False, default=0)
    flag_vld: Mapped[int] = mapped_column(nullable=False, default=0)


# Прототип таблицы персонажей
class Character(Base):
    __tablename__ = 'characters'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    account: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    money: Mapped[str] = mapped_column(String(100), default='0')
    name: Mapped[str] = mapped_column(String(80))
    items: Mapped[str] = mapped_column(ForeignKey('donat_shop.items'), nullable=True)
    game_state: Mapped[int] = mapped_column()

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
