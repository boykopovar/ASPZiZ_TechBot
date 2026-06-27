from aiogram import Router, types
from aiogram.filters import Command

from src.constants import (
    MSG_ACCESS_DENIED_ADMIN,
    MSG_SET_ROLE_USAGE,
    MSG_ROLE_INVALID,
    MSG_USER_NOT_FOUND,
    MSG_ROLE_UPDATED,
)
from src.services import user_service
from src.types.enums import Role

_router = Router()

_VALID_ROLES = (Role.USER, Role.STAFF, Role.ADMIN)


@_router.message(Command("set_role"))
async def set_role(message: types.Message) -> None:
    if not await user_service.is_admin(message.from_user.id):
        await message.answer(MSG_ACCESS_DENIED_ADMIN)
        return
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer(MSG_SET_ROLE_USAGE)
        return
    telegram_id_str, role_str = parts[1], parts[2]
    if role_str not in [r.value for r in _VALID_ROLES]:
        await message.answer(MSG_ROLE_INVALID)
        return
    user = await user_service.get_user(int(telegram_id_str))
    if not user:
        await message.answer(MSG_USER_NOT_FOUND.format(telegram_id=telegram_id_str))
        return
    await user_service.set_user_role(int(telegram_id_str), role_str)
    await message.answer(MSG_ROLE_UPDATED.format(telegram_id=telegram_id_str, role=role_str))
