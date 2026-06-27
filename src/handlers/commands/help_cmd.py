from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.constants import MSG_HELP

_router = Router()


@_router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(MSG_HELP)
