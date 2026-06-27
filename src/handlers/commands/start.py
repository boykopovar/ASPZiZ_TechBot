from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.constants import MSG_WELCOME
from src.services import user_service

_router = Router()


@_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await user_service.add_or_update_user(message.from_user.id, message.from_user.username or "")
    await message.answer(MSG_WELCOME)
