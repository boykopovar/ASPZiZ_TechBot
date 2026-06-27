import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN, DATABASE_DIR
from handlers import router as h_router
from commands import router as c_router
from admin import router as a_router
from fallback import router as f_router
from db import init_db

# Автоматически создаём директорию data для sqlite, если не существует
os.makedirs(DATABASE_DIR, exist_ok=True)

# Настройка логирования (будет видно в docker compose logs)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger("main")

async def main():
    logger.info("Init DB")
    await init_db()
    logger.info("Starting bot")

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    # Подключение всех роутеров (сохраняется приоритет)
    dp.include_router(c_router)
    dp.include_router(a_router)
    dp.include_router(h_router)
    dp.include_router(f_router)

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Helpdesk Bot is running.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
