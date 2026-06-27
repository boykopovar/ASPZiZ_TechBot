from typing import List, Tuple

from aiogram import Router, Bot, F
from aiogram.types import Message

from src.constants import MSG_TICKET_RECEIVED, MSG_NO_TEXT
from src.logger import logger
from src.services import ticket_service, chat_service, user_service
from src.types.enums import MediaType
from src.utils.formatting import user_link, caption_with_link
from src.utils.keyboards import accept_kb
from src.utils.media import build_media_group

_router = Router()

_WARN_ADD_KB: str = "Ошибка при попытке добавить клавиатуру: %s"


def _extract_media_from_message(message: Message) -> List[Tuple[str, str]]:
    if message.photo:
        return [(MediaType.PHOTO, message.photo[-1].file_id)]
    if message.video:
        return [(MediaType.VIDEO, message.video.file_id)]
    if message.audio:
        return [(MediaType.AUDIO, message.audio.file_id)]
    return []


async def _publish_to_chats(
    bot: Bot,
    ticket_id: int,
    media: List[Tuple[str, str]],
    text: str,
    link: str,
) -> None:
    chats = await chat_service.get_active_chats()
    caption = caption_with_link(text, link)
    for chat in chats:
        chat_id = chat[0]
        if media:
            m_type = media[0][0]
            file_id = media[0][1]
            if m_type == MediaType.PHOTO:
                msg = await bot.send_photo(chat_id, file_id, caption=caption, reply_markup=accept_kb(ticket_id))
            elif m_type == MediaType.VIDEO:
                msg = await bot.send_video(chat_id, file_id, caption=caption, reply_markup=accept_kb(ticket_id))
            elif m_type == MediaType.AUDIO:
                msg = await bot.send_audio(chat_id, file_id, caption=caption, reply_markup=accept_kb(ticket_id))
            else:
                msg = await bot.send_message(chat_id, caption, reply_markup=accept_kb(ticket_id))
        else:
            msg = await bot.send_message(chat_id, caption, reply_markup=accept_kb(ticket_id))
        await ticket_service.register_publication(ticket_id, chat_id, msg.message_id)


async def _publish_album_to_chats(
    bot: Bot,
    ticket_id: int,
    media: List[Tuple[str, str]],
    text: str,
) -> None:
    chats = await chat_service.get_active_chats()
    for chat in chats:
        chat_id = chat[0]
        group = build_media_group(media, text)
        if group:
            msgs = await bot.send_media_group(chat_id=chat_id, media=group)
            try:
                await bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=msgs[0].message_id,
                    reply_markup=accept_kb(ticket_id),
                )
            except Exception as exc:
                logger.warning(_WARN_ADD_KB, exc)
            await ticket_service.register_publication(ticket_id, chat_id, msgs[0].message_id)
        elif media and media[0][0] == MediaType.AUDIO:
            msg = await bot.send_audio(
                chat_id,
                media[0][1],
                caption=text if text else None,
                reply_markup=accept_kb(ticket_id),
            )
            await ticket_service.register_publication(ticket_id, chat_id, msg.message_id)


@_router.message(F.media_group_id)
async def handle_media_group(message: Message, album: List[Message], bot: Bot) -> None:
    user = message.from_user
    await user_service.add_or_update_user(user.id, user.username or "")
    text = album[0].caption if album[0].caption else ""
    media: List[Tuple[str, str]] = []
    for msg in album:
        media.extend(_extract_media_from_message(msg))
    ticket_id = await ticket_service.create_ticket(user.id, user.username or "", text, media)
    await message.answer(MSG_TICKET_RECEIVED)
    await _publish_album_to_chats(bot, ticket_id, media, text)


@_router.message(F.photo | F.video | F.audio | (F.text & ~F.text.startswith("/")))
async def handle_single(message: Message, bot: Bot) -> None:
    user = message.from_user
    await user_service.add_or_update_user(user.id, user.username or "")
    text = message.caption or message.text or ""
    media = _extract_media_from_message(message)
    ticket_id = await ticket_service.create_ticket(user.id, user.username or "", text, media)
    await message.answer(MSG_TICKET_RECEIVED)
    link = user_link(user)
    await _publish_to_chats(bot, ticket_id, media, text, link)
