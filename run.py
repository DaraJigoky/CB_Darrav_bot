import os
import asyncio
import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from dotenv import load_dotenv

from app.handlers.menu import menu
from app.handlers.account import account
from app.handlers.game import game
from app.database.models import async_main
from app.database.preload import preloads




# Главная функция. Поллинг и тд
async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(menu, account, game)
    dp.startup.register(on_startup)
    # Создаёт кнопку меню слева с командами. Прикольная вещь. На доработку
    #await bot.set_my_commands(bot_commands, scope=BotCommandScopeDefault())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



# Запуск нужных на старте дел. Создание таблиц в БД
async def on_startup(dispatcher):
    await async_main()
    await preloads()
    with open('app/logs.txt', 'a') as file:
        file.write('\n\n ************************* Бот запущен!' + str(datetime.datetime.now()) + '*************************')


# Запуск бота
if __name__ == '__main__':
    try:
        print('Бот включен')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
        with open('app/logs.txt', 'a') as file:
            file.write('\n\n ************************* Бот выключен!' + str(datetime.datetime.now()) + '*************************')
