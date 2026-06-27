from aiogram import Router, F
from aiogram.types import Message

from src.constants import MSG_UNKNOWN_COMMAND

_router = Router()


@_router.message(F.text & F.text.startswith("/"))
async def unknown_command(message: Message) -> None:
    await message.answer(MSG_UNKNOWN_COMMAND)
