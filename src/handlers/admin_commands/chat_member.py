from aiogram import Router, Bot, types

from src.constants import MSG_NEW_CHAT_NOTIFY
from src.services import chat_service, user_service
from src.utils.keyboards import approve_decline_chat_kb

_router = Router()


@_router.my_chat_member()
async def on_bot_added(event: types.ChatMemberUpdated, bot: Bot) -> None:
    if event.new_chat_member.user.id != (await bot.me()).id:
        return
    await chat_service.add_support_chat(event.chat.id, event.chat.title)
    admin_ids = await user_service.get_all_admin_ids()
    kb = approve_decline_chat_kb(event.chat.id)
    for admin_id in admin_ids:
        await bot.send_message(
            admin_id,
            MSG_NEW_CHAT_NOTIFY.format(title=event.chat.title, chat_id=event.chat.id),
            reply_markup=kb,
        )
