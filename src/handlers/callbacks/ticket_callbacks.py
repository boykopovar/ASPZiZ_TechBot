from datetime import timedelta

from aiogram import Router, Bot, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from src.constants import (
    MSG_ONLY_STAFF,
    MSG_TICKET_BUSY,
    MSG_TICKET_NOT_FOUND,
    MSG_TICKET_DONE_ANSWER,
    MSG_ACCEPT_NOTIFY_STAFF,
    MSG_ACCEPT_NOTIFY_USER,
    MSG_DONE_NOTIFY_USER,
    MSG_ACCEPTED_SUFFIX,
    MSG_NO_TEXT,
    ACCEPT_TIME_FMT,
)
from src.env_tools import GTM_PLUS
from src.logger import logger
from src.services import ticket_service, user_service
from src.types.callbacks import AcceptTicketCb, DoneTicketCb
from src.utils.formatting import user_link
from src.utils.keyboards import done_kb

_router = Router()

_WARN_EDIT_TEXT: str = "edit_text failed: %s"
_WARN_EDIT_MARKUP: str = "edit_reply_markup failed: %s"
_ERR_DONE_NOTIFY: str = "Не удалось отправить пользователю %s уведомление о завершении заявки: %s"


@_router.callback_query(AcceptTicketCb.filter())
async def accept_ticket(callback: CallbackQuery, callback_data: AcceptTicketCb, bot: Bot) -> None:
    ticket_id = callback_data.ticket_id
    user = callback.from_user
    if not await user_service.is_staff_or_admin(user.id):
        await callback.answer(MSG_ONLY_STAFF, show_alert=True)
        return
    ticket = await ticket_service.get_ticket(ticket_id)
    if not ticket or ticket[4] != "new":
        await callback.answer(MSG_TICKET_BUSY, show_alert=True)
        return
    await ticket_service.accept_ticket(ticket_id, user.id)
    ticket_text = ticket[3] or MSG_NO_TEXT
    accept_datetime = callback.message.date + timedelta(hours=GTM_PLUS)
    accept_time = accept_datetime.strftime(ACCEPT_TIME_FMT)
    link = user_link(user)
    new_text = (callback.message.html_text or "") + MSG_ACCEPTED_SUFFIX.format(
        user_link=link, accept_time=accept_time
    )
    if (callback.message.html_text or "") != new_text:
        try:
            await callback.message.edit_text(new_text)
        except TelegramBadRequest as exc:
            logger.warning(_WARN_EDIT_TEXT, exc)
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest as exc:
        logger.warning(_WARN_EDIT_MARKUP, exc)
    await bot.send_message(
        user.id,
        MSG_ACCEPT_NOTIFY_STAFF.format(ticket_id=ticket_id, ticket_text=ticket_text, user_link=link),
        reply_markup=done_kb(ticket_id),
    )
    await bot.send_message(
        ticket[1],
        MSG_ACCEPT_NOTIFY_USER.format(ticket_id=ticket_id, user_link=link),
    )


@_router.callback_query(DoneTicketCb.filter())
async def finish_ticket(callback: CallbackQuery, callback_data: DoneTicketCb, bot: Bot) -> None:
    ticket_id = callback_data.ticket_id
    ticket = await ticket_service.get_ticket(ticket_id)
    if not ticket:
        await callback.answer(MSG_TICKET_NOT_FOUND, show_alert=True)
        return
    await ticket_service.finish_ticket(ticket_id, callback.from_user.id)
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception as exc:
        logger.warning(_WARN_EDIT_MARKUP, exc)
    try:
        await bot.send_message(
            ticket[1],
            MSG_DONE_NOTIFY_USER.format(ticket_id=ticket_id),
        )
    except Exception as exc:
        logger.error(_ERR_DONE_NOTIFY, ticket[1], exc)
    await callback.answer(MSG_TICKET_DONE_ANSWER)
