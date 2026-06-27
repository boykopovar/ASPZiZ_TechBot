from typing import List, Tuple

from aiogram import Router, Bot, types
from aiogram.filters import Command

from src.constants import (
    MSG_ACCESS_DENIED_ADMIN,
    MSG_ACCESS_DENIED_STAFF,
    MSG_NO_TICKETS,
    MSG_REPUBLISH_COUNT,
    MSG_REPUBLISH_TICKET_COUNT,
    MSG_REPUBLISH_USAGE,
    MSG_TICKET_NOT_FOUND_ID,
)
from src.services import ticket_service, chat_service, user_service
from src.utils.formatting import ticket_all_line, build_paginated_messages
from src.utils.keyboards import accept_kb
from src.handlers.messages.ticket_messages import _build_media_group

_router = Router()


async def _send_ticket_to_chat(
    bot: Bot,
    ticket: Tuple[int, int, str, str, str],
    chat_id: int,
) -> None:
    ticket_id = ticket[0]
    media = await ticket_service.get_ticket_media(ticket_id)
    group = _build_media_group(media, ticket[3])
    if group:
        msgs = await bot.send_media_group(chat_id=chat_id, media=group)
        await ticket_service.register_publication(ticket_id, chat_id, msgs[0].message_id)
    else:
        msg = await bot.send_message(chat_id, ticket[3], reply_markup=accept_kb(ticket_id))
        await ticket_service.register_publication(ticket_id, chat_id, msg.message_id)


@_router.message(Command("republish_new_tickets"))
async def republish_new_tickets(message: types.Message, bot: Bot) -> None:
    if not await user_service.is_admin(message.from_user.id):
        await message.answer(MSG_ACCESS_DENIED_ADMIN)
        return
    tickets = await ticket_service.get_new_tickets()
    chats = await chat_service.get_all_chats()
    count = 0
    for ticket in tickets:
        for chat_id, _title, is_active in chats:
            if is_active and not await ticket_service.is_ticket_published(ticket[0], chat_id):
                await _send_ticket_to_chat(bot, ticket, chat_id)
                count += 1
    await message.answer(MSG_REPUBLISH_COUNT.format(count=count))


@_router.message(Command("republish_ticket"))
async def republish_ticket(message: types.Message, bot: Bot) -> None:
    if not await user_service.is_admin(message.from_user.id):
        await message.answer(MSG_ACCESS_DENIED_ADMIN)
        return
    parts = message.text.strip().split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer(MSG_REPUBLISH_USAGE)
        return
    ticket_id = int(parts[1])
    ticket = await ticket_service.get_ticket(ticket_id)
    if not ticket:
        await message.answer(MSG_TICKET_NOT_FOUND_ID.format(ticket_id=ticket_id))
        return
    chats = await chat_service.get_all_chats()
    count = 0
    for chat_id, _title, is_active in chats:
        if is_active:
            await _send_ticket_to_chat(bot, ticket, chat_id)
            count += 1
    await message.answer(MSG_REPUBLISH_TICKET_COUNT.format(ticket_id=ticket_id, count=count))


@_router.message(Command("all_history"))
async def all_history(message: types.Message) -> None:
    if not await user_service.is_admin(message.from_user.id):
        await message.answer(MSG_ACCESS_DENIED_ADMIN)
        return
    tickets = await ticket_service.get_all_tickets()
    if not tickets:
        await message.answer(MSG_NO_TICKETS)
        return
    lines = [
        ticket_all_line(t[0], t[4], t[3], t[2], t[1], t[5]) for t in tickets
    ]
    for page in build_paginated_messages(lines):
        await message.answer(page)
