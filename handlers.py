from datetime import datetime, timezone, timedelta

from aiogram import Router, Bot, types, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaVideo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import GTM_PLUS
from db import (
    add_or_update_user, save_ticket, save_ticket_media,
    get_active_support_chats, register_publication,
    set_ticket_accepted, get_ticket, get_ticket_media, set_ticket_done,
    is_ticket_published, log, get_user_by_id
)
from aiogram.exceptions import TelegramBadRequest
import logging

router = Router()
logger = logging.getLogger(__name__)

def user_link(user: types.User):
    if user.username:
        return f"@{user.username}"
    return f"<a href='tg://user?id={user.id}'>{user.full_name or user.id}</a>"

def gen_accept_kb(ticket_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text="Принять", callback_data=f"accept_{ticket_id}")
    return kb.as_markup()

def gen_done_kb(ticket_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text="Завершить", callback_data=f"done_{ticket_id}")
    return kb.as_markup()

@router.message(F.media_group_id)
async def handle_media_group(message: Message, album: list[Message], bot: Bot):
    user = message.from_user
    await add_or_update_user(user.id, user.username or "")
    text = album[0].caption if album[0].caption else ""
    ticket_id = await save_ticket(user.id, user.username, text)
    media = []
    for msg in album:
        if msg.photo:
            media.append({'type': 'photo', 'file_id': msg.photo[-1].file_id})
        elif msg.video:
            media.append({'type': 'video', 'file_id': msg.video.file_id})
        elif msg.audio:
            media.append({'type': 'audio', 'file_id': msg.audio.file_id})
    await save_ticket_media(ticket_id, media)
    await message.answer("Джинны творят магию, ожидайте!")

    chats = await get_active_support_chats()
    for chat in chats:
        group = []
        for m in media:
            if m['type'] == 'photo':
                group.append(InputMediaPhoto(m['file_id'], caption=text if len(group) == 0 else None))
            elif m['type'] == 'video':
                group.append(InputMediaVideo(m['file_id'], caption=text if len(group) == 0 else None))
        if group:
            msgs = await bot.send_media_group(chat_id=chat[0], media=group)
            try:
                await bot.edit_message_reply_markup(
                    chat_id=chat[0],
                    message_id=msgs[0].message_id,
                    reply_markup=gen_accept_kb(ticket_id)
                )
            except Exception as e:
                logger.warning(f"Ошибка при попытке добавить клавиатуру: {e}")
            await register_publication(ticket_id, chat[0], msgs[0].message_id)
        elif media and media[0]['type'] == 'audio':
            msg = await bot.send_audio(
                chat[0], media[0]['file_id'],
                caption=text if text else None,
                reply_markup=gen_accept_kb(ticket_id)
            )
            await register_publication(ticket_id, chat[0], msg.message_id)

@router.message(F.photo | F.video | F.audio | (F.text & ~F.text.startswith("/")))
async def handle_single(message: Message, bot: Bot):
    user = message.from_user
    await add_or_update_user(user.id, user.username or "")
    text = message.caption or message.text or ""
    ticket_id = await save_ticket(user.id, user.username, text)
    media = []
    if message.photo:
        media.append({'type': 'photo', 'file_id': message.photo[-1].file_id})
    elif message.video:
        media.append({'type': 'video', 'file_id': message.video.file_id})
    elif message.audio:
        media.append({'type': 'audio', 'file_id': message.audio.file_id})
    await save_ticket_media(ticket_id, media)
    await message.answer("Джинны творят магию, ожидайте!")

    chats = await get_active_support_chats()
    for chat in chats:
        if media:
            if media[0]['type'] == 'photo':
                msg = await bot.send_photo(chat[0], media[0]['file_id'],
                    caption=f"{text}\n{user_link(user)}", reply_markup=gen_accept_kb(ticket_id))
            elif media[0]['type'] == 'video':
                msg = await bot.send_video(chat[0], media[0]['file_id'],
                    caption=f"{text}\n{user_link(user)}", reply_markup=gen_accept_kb(ticket_id))
            elif media[0]['type'] == 'audio':
                msg = await bot.send_audio(chat[0], media[0]['file_id'],
                    caption=f"{text}\n{user_link(user)}", reply_markup=gen_accept_kb(ticket_id))
            else:
                msg = await bot.send_message(chat[0],
                    f"{text}\n{user_link(user)}", reply_markup=gen_accept_kb(ticket_id))
        else:
            msg = await bot.send_message(chat[0],
                f"{text}\n{user_link(user)}", reply_markup=gen_accept_kb(ticket_id))
        await register_publication(ticket_id, chat[0], msg.message_id)


@router.callback_query(F.data.startswith("accept_"))
async def accept_ticket(callback: CallbackQuery, bot: Bot):
    ticket_id = int(callback.data.split("_")[1])
    user = callback.from_user

    # Проверка роли
    user_db = await get_user_by_id(user.id)
    role = user_db[3] if user_db else None
    if role not in ('staff', 'admin'):
        await callback.answer("Только staff может принять заявку.", show_alert=True)
        return

    ticket = await get_ticket(ticket_id)
    if not ticket or ticket[4] != 'new':
        await callback.answer("Заявка уже занята.", show_alert=True)
        return
    await set_ticket_accepted(ticket_id, user.id)
    await log("accept", user.id, f"Принял заявку #{ticket_id}")

    ticket_text = ticket[3] or "(без текста)"

    accept_datetime = callback.message.date + timedelta(hours=GTM_PLUS)
    accept_time = accept_datetime.strftime("%H:%M:%S")

    new_text = (callback.message.html_text or "") + f"\n\nПринял: {user_link(user)} в {accept_time}"
    if (callback.message.html_text or "") != new_text:
        try:
            await callback.message.edit_text(new_text)
        except TelegramBadRequest as e:
            logger.warning(f"edit_text failed: {e}")
    # Безопасно снимаем клаву
    try:
        await callback.message.edit_reply_markup(None)
    except TelegramBadRequest as e:
        logger.warning(f"edit_reply_markup failed: {e}")

    # Для staff/admin — кнопка завершить
    await bot.send_message(
        user.id,
        f"Вы взяли заявку #{ticket_id}:\n{ticket_text}\n{user_link(user)}",
        reply_markup=gen_done_kb(ticket_id)
    )

    # Для пользователя — обязательно уведомление!
    ticket_owner_id = ticket[1]
    await bot.send_message(
        ticket_owner_id,
        f"Ваша заявка #{ticket_id} взята в работу сотрудником поддержки.\n{user_link(user)} займётся вашим вопросом!"
    )


@router.callback_query(F.data.startswith("done_"))
async def finish_ticket(callback: CallbackQuery, bot: Bot):
    ticket_id = int(callback.data.split("_")[1])
    ticket = await get_ticket(ticket_id)
    if not ticket:
        await callback.answer("Заявка не найдена.", show_alert=True)
        return
    await set_ticket_done(ticket_id)
    await log("done", callback.from_user.id, f"Завершил заявку #{ticket_id}")

    # 1. Гарантированно убираем кнопки у сообщения в чате поддержки (если уже убраны — не паникуем)
    try:
        await callback.message.edit_reply_markup(None)
    except Exception as e:
        logger.warning(f"Не удалось убрать кнопки у сообщения: {e}")

    # 2. Гарантированно уведомляем пользователя
    user_id = ticket[1]  # user_id заявки
    try:
        await bot.send_message(
            user_id,
            f"Ваша заявка #{ticket_id} успешно завершена! Спасибо за обращение."
        )
    except Exception as e:
        logger.error(f"Не удалось отправить пользователю {user_id} уведомление о завершении заявки: {e}")

    # 3. Отвечаем обработчику (админ/саппорт)
    await callback.answer("Заявка завершена.")

