from aiogram import Dispatcher

from src.handlers.commands import commands_router
from src.handlers.messages import messages_router
from src.handlers.callbacks import callbacks_router
from src.handlers.admin_commands import admin_router


def register_all_routers(dp: Dispatcher) -> None:
    dp.include_router(commands_router)
    dp.include_router(admin_router)
    dp.include_router(messages_router)
    dp.include_router(callbacks_router)
