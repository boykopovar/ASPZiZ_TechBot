from typing import List, Optional, Tuple

from src.env_tools import ADMIN_USER_IDS
from src.repositories import db_repository
from src.types.enums import Role


async def add_or_update_user(telegram_id: int, username: str) -> None:
    await db_repository.add_or_update_user(telegram_id, username)


async def get_user(telegram_id: int) -> Optional[Tuple[int, int, str, str]]:
    return await db_repository.get_user_by_id(telegram_id)


async def is_admin(telegram_id: int) -> bool:
    if telegram_id in ADMIN_USER_IDS:
        return True
    user = await db_repository.get_user_by_id(telegram_id)
    return user is not None and user[3] == Role.ADMIN


async def is_staff_or_admin(telegram_id: int) -> bool:
    user = await db_repository.get_user_by_id(telegram_id)
    return user is not None and user[3] in (Role.STAFF, Role.ADMIN)


async def get_all_admin_ids() -> List[int]:
    db_admins = await db_repository.get_admin_ids_from_db()
    return list(set(ADMIN_USER_IDS + db_admins))


async def set_user_role(telegram_id: int, role: str) -> None:
    await db_repository.set_user_role(telegram_id, role)
