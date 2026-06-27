from typing import List, Optional, Tuple

from src.constants import LOG_ACTION_ACCEPT, LOG_ACTION_DONE
from src.repositories import db_repository


async def create_ticket(
    user_id: int, username: str, text: str, media: List[Tuple[str, str]]
) -> int:
    ticket_id = await db_repository.save_ticket(user_id, username, text)
    await db_repository.save_ticket_media(ticket_id, media)
    return ticket_id


async def get_ticket(ticket_id: int) -> Optional[Tuple[int, int, str, str, str]]:
    return await db_repository.get_ticket(ticket_id)


async def get_ticket_media(ticket_id: int) -> List[Tuple[str, str]]:
    return await db_repository.get_ticket_media(ticket_id)


async def accept_ticket(ticket_id: int, staff_id: int) -> None:
    await db_repository.set_ticket_accepted(ticket_id)
    await db_repository.log(LOG_ACTION_ACCEPT, staff_id, f"Принял заявку #{ticket_id}")


async def finish_ticket(ticket_id: int, user_id: int) -> None:
    await db_repository.set_ticket_done(ticket_id)
    await db_repository.log(LOG_ACTION_DONE, user_id, f"Завершил заявку #{ticket_id}")


async def is_ticket_published(ticket_id: int, chat_id: int) -> bool:
    return await db_repository.is_ticket_published(ticket_id, chat_id)


async def register_publication(ticket_id: int, chat_id: int, message_id: int) -> None:
    await db_repository.register_publication(ticket_id, chat_id, message_id)


async def get_new_tickets() -> List[Tuple[int, int, str, str, str]]:
    return await db_repository.get_new_tickets()


async def get_all_tickets() -> List[Tuple[int, int, str, str, str, str]]:
    return await db_repository.get_all_tickets()


async def get_user_tickets(telegram_id: int) -> List[Tuple[int, str, str, str]]:
    return await db_repository.get_user_tickets(telegram_id)
