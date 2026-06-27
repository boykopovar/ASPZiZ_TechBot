from aiogram.filters.callback_data import CallbackData


class ActivateChatCb(CallbackData, prefix="activate"):
    chat_id: int


class DeactivateChatCb(CallbackData, prefix="deactivate"):
    chat_id: int


class ApproveChatCb(CallbackData, prefix="approve_chat"):
    chat_id: int


class DeclineChatCb(CallbackData, prefix="decline_chat"):
    chat_id: int
