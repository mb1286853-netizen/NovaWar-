import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import TOKEN
import database
from handlers import start, profile, shop, boxes, miner, defense, support, callback

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def on_startup():
    await database.init_db()
    print("WarZone Bot آنلاین شد! ⚔️")

async def main():
    dp.startup.register(on_startup)
    
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(shop.router)
    dp.include_router(boxes.router)
    dp.include_router(miner.router)
    dp.include_router(defense.router)
    dp.include_router(support.router)
    dp.include_router(callback.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
