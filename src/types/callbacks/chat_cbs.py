from aiogram.filters.callback_data import CallbackData

from src.constants import (
    CB_PREFIX_ACTIVATE_CHAT,
    CB_PREFIX_DEACTIVATE_CHAT,
    CB_PREFIX_APPROVE_CHAT,
    CB_PREFIX_DECLINE_CHAT,
)


class ActivateChatCb(CallbackData, prefix=CB_PREFIX_ACTIVATE_CHAT):
    chat_id: int


class DeactivateChatCb(CallbackData, prefix=CB_PREFIX_DEACTIVATE_CHAT):
    chat_id: int


class ApproveChatCb(CallbackData, prefix=CB_PREFIX_APPROVE_CHAT):
    chat_id: int


class DeclineChatCb(CallbackData, prefix=CB_PREFIX_DECLINE_CHAT):
    chat_id: int
