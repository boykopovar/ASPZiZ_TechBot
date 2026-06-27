from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.constants import MSG_NO_USER_TICKETS
from src.services import ticket_service
from src.utils.formatting import ticket_history_line, build_paginated_messages

_router = Router()


@_router.message(Command("my_history"))
async def cmd_my_history(message: Message) -> None:
    tickets = await ticket_service.get_user_tickets(message.from_user.id)
    if not tickets:
        await message.answer(MSG_NO_USER_TICKETS)
        return
    lines = [ticket_history_line(t[0], t[2], t[3]) for t in tickets]
    for page in build_paginated_messages(lines):
        await message.answer(page)
