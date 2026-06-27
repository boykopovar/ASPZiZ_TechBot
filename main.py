import asyncio
import os
import signal
from types import FrameType
from typing import Optional

import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.env_tools import TOKEN, DATABASE_DIR
from src.logger import logger
from src.handlers import register_all_routers
from src.repositories.db_repository import init_db

logging.getLogger("aiogram.event").setLevel(logging.WARNING)

_PARSE_MODE: str = "HTML"
_LOG_INIT_DB: str = "Init DB"
_LOG_STARTED: str = "Bot started"
_LOG_SHUTDOWN: str = "Shutting down (signal %s)"


async def main() -> None:
    os.makedirs(DATABASE_DIR, exist_ok=True)
    logger.info(_LOG_INIT_DB)
    await init_db()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=_PARSE_MODE))
    dp = Dispatcher()
    register_all_routers(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info(_LOG_STARTED)
    await dp.start_polling(bot, handle_signals=False)


def _exit_prog(sig: int, frame: Optional[FrameType]) -> None:
    logger.info(_LOG_SHUTDOWN, sig)
    os._exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, _exit_prog)
    signal.signal(signal.SIGTERM, _exit_prog)
    asyncio.run(main())
