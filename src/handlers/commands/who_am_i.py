from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.constants import MSG_WHO_AM_I, MSG_NOT_REGISTERED
from src.services import user_service

_router = Router()


@_router.message(Command("who_am_i"))
async def cmd_who_am_i(message: Message) -> None:
    user = await user_service.get_user(message.from_user.id)
    if user:
        await message.answer(
            MSG_WHO_AM_I.format(telegram_id=user[1], username=user[2], role=user[3])
        )
    else:
        await message.answer(MSG_NOT_REGISTERED)
