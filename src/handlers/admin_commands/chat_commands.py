from aiogram import Router, Bot, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.constants import (
    MSG_NO_CHATS,
    MSG_ACCESS_DENIED_ADMIN,
    CHAT_STATUS_ACTIVE,
    CHAT_STATUS_INACTIVE,
    MSG_CHAT_STATUS_LINE,
)
from src.services import chat_service, user_service
from src.utils.keyboards import toggle_chat_kb

_router = Router()


@_router.message(Command("chats"))
async def show_chats(message: types.Message) -> None:
    if not await user_service.is_admin(message.from_user.id):
        await message.answer(MSG_ACCESS_DENIED_ADMIN)
        return
    chats = await chat_service.get_all_chats()
    if not chats:
        await message.answer(MSG_NO_CHATS)
        return
    text = ""
    kb = InlineKeyboardBuilder()
    for chat_id, title, is_active in chats:
        display = title or str(chat_id)
        status = CHAT_STATUS_ACTIVE if is_active else CHAT_STATUS_INACTIVE
        text += MSG_CHAT_STATUS_LINE.format(title=display, chat_id=chat_id, status=status)
        chat_kb = toggle_chat_kb(chat_id, display, bool(is_active))
        for row in chat_kb.inline_keyboard:
            for btn in row:
                kb.button(text=btn.text, callback_data=btn.callback_data)
    await message.answer(text, reply_markup=kb.as_markup())
