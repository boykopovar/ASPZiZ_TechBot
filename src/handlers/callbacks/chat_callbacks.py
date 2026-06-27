from aiogram import Router
from aiogram.types import CallbackQuery

from src.constants import MSG_CHAT_ACTIVATED, MSG_CHAT_DEACTIVATED, MSG_CHAT_APPROVED, MSG_CHAT_DECLINED
from src.services import chat_service, user_service
from src.constants import MSG_ACCESS_DENIED_ADMIN
from src.types.callbacks import ActivateChatCb, DeactivateChatCb, ApproveChatCb, DeclineChatCb

_router = Router()


@_router.callback_query(ActivateChatCb.filter())
async def activate_chat(callback: CallbackQuery, callback_data: ActivateChatCb) -> None:
    if not await user_service.is_admin(callback.from_user.id):
        await callback.answer(MSG_ACCESS_DENIED_ADMIN, show_alert=True)
        return
    await chat_service.activate_chat(callback_data.chat_id, callback.from_user.id)
    await callback.answer(MSG_CHAT_ACTIVATED)
    await callback.message.edit_reply_markup(reply_markup=None)


@_router.callback_query(DeactivateChatCb.filter())
async def deactivate_chat(callback: CallbackQuery, callback_data: DeactivateChatCb) -> None:
    if not await user_service.is_admin(callback.from_user.id):
        await callback.answer(MSG_ACCESS_DENIED_ADMIN, show_alert=True)
        return
    await chat_service.deactivate_chat(callback_data.chat_id, callback.from_user.id)
    await callback.answer(MSG_CHAT_DEACTIVATED)
    await callback.message.edit_reply_markup(reply_markup=None)


@_router.callback_query(ApproveChatCb.filter())
async def approve_chat(callback: CallbackQuery, callback_data: ApproveChatCb) -> None:
    if not await user_service.is_admin(callback.from_user.id):
        await callback.answer(MSG_ACCESS_DENIED_ADMIN, show_alert=True)
        return
    await chat_service.activate_chat(callback_data.chat_id, callback.from_user.id)
    await callback.answer(MSG_CHAT_APPROVED)
    await callback.message.edit_reply_markup(reply_markup=None)


@_router.callback_query(DeclineChatCb.filter())
async def decline_chat(callback: CallbackQuery, callback_data: DeclineChatCb) -> None:
    if not await user_service.is_admin(callback.from_user.id):
        await callback.answer(MSG_ACCESS_DENIED_ADMIN, show_alert=True)
        return
    await chat_service.deactivate_chat(callback_data.chat_id, callback.from_user.id)
    await callback.answer(MSG_CHAT_DECLINED)
    await callback.message.edit_reply_markup(reply_markup=None)
