from typing import List, Tuple

from src.repositories import db_repository


async def get_active_chats() -> List[Tuple[int, str, int]]:
    return await db_repository.get_active_support_chats()


async def get_all_chats() -> List[Tuple[int, str, int]]:
    return await db_repository.get_all_chats()


async def add_support_chat(chat_id: int, title: str) -> None:
    await db_repository.add_support_chat(chat_id, title)


async def activate_chat(chat_id: int, approved_by: int) -> None:
    await db_repository.set_chat_active(chat_id, True, approved_by)
    await db_repository.log("activate_chat", approved_by, f"Активация чата {chat_id}")


async def deactivate_chat(chat_id: int, approved_by: int) -> None:
    await db_repository.set_chat_active(chat_id, False, approved_by)
    await db_repository.log("deactivate_chat", approved_by, f"Деактивация чата {chat_id}")
