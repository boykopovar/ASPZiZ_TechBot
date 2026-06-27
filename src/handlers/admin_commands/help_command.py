from aiogram import Router, types
from aiogram.filters import Command

from src.constants import MSG_HELP_ADMINS, MSG_ACCESS_DENIED_STAFF
from src.services import user_service

_router = Router()


@_router.message(Command("help_admins"))
async def help_admins(message: types.Message) -> None:
    if not await user_service.is_staff_or_admin(message.from_user.id):
        await message.answer(MSG_ACCESS_DENIED_STAFF)
        return
    await message.answer(MSG_HELP_ADMINS, parse_mode="HTML")
