from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.constants import BTN_ACCEPT, BTN_DONE, BTN_APPROVE_CHAT, BTN_DECLINE_CHAT, BTN_ACTIVATE_CHAT, BTN_DEACTIVATE_CHAT
from src.types.callbacks import AcceptTicketCb, DoneTicketCb, ApproveChatCb, DeclineChatCb, ActivateChatCb, DeactivateChatCb


def accept_kb(ticket_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=BTN_ACCEPT, callback_data=AcceptTicketCb(ticket_id=ticket_id))
    return kb.as_markup()


def done_kb(ticket_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=BTN_DONE, callback_data=DoneTicketCb(ticket_id=ticket_id))
    return kb.as_markup()


def approve_decline_chat_kb(chat_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=BTN_APPROVE_CHAT, callback_data=ApproveChatCb(chat_id=chat_id))
    kb.button(text=BTN_DECLINE_CHAT, callback_data=DeclineChatCb(chat_id=chat_id))
    return kb.as_markup()


def toggle_chat_kb(chat_id: int, title: str, is_active: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if is_active:
        kb.button(
            text=BTN_DEACTIVATE_CHAT.format(title=title),
            callback_data=DeactivateChatCb(chat_id=chat_id),
        )
    else:
        kb.button(
            text=BTN_ACTIVATE_CHAT.format(title=title),
            callback_data=ActivateChatCb(chat_id=chat_id),
        )
    return kb.as_markup()
