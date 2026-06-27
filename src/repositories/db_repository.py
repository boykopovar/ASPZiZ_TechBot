from typing import List, Optional, Tuple

import aiosqlite

from src.env_tools import DATABASE_PATH, ADMIN_USER_IDS

_SQL_CREATE_USERS: str = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE NOT NULL,
    username TEXT NOT NULL DEFAULT '',
    role TEXT NOT NULL DEFAULT 'user'
)
"""
_SQL_CREATE_TICKETS: str = """
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL DEFAULT '',
    text TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
_SQL_CREATE_TICKET_MEDIA: str = """
CREATE TABLE IF NOT EXISTS ticket_media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    file_id TEXT NOT NULL
)
"""
_SQL_CREATE_SUPPORT_CHATS: str = """
CREATE TABLE IF NOT EXISTS support_chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    is_active INTEGER NOT NULL DEFAULT 0,
    approved_by INTEGER
)
"""
_SQL_CREATE_PUBLICATIONS: str = """
CREATE TABLE IF NOT EXISTS publications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    chat_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    UNIQUE(ticket_id, chat_id)
)
"""
_SQL_CREATE_LOGS: str = """
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    user_id INTEGER,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

_SQL_SEED_ADMIN: str = """
INSERT INTO users (telegram_id, username, role)
VALUES (?, '', 'admin')
ON CONFLICT(telegram_id) DO UPDATE SET role = 'admin'
"""
_SQL_UPSERT_USER: str = """
INSERT INTO users (telegram_id, username, role)
VALUES (?, ?, 'user')
ON CONFLICT(telegram_id) DO UPDATE SET username = excluded.username
"""
_SQL_GET_USER: str = "SELECT id, telegram_id, username, role FROM users WHERE telegram_id = ?"
_SQL_GET_ADMINS: str = "SELECT telegram_id FROM users WHERE role = 'admin'"
_SQL_SET_ROLE: str = "UPDATE users SET role = ? WHERE telegram_id = ?"

_SQL_INSERT_TICKET: str = "INSERT INTO tickets (user_id, username, text, status) VALUES (?, ?, ?, 'new')"
_SQL_GET_TICKET: str = "SELECT id, user_id, username, text, status FROM tickets WHERE id = ?"
_SQL_GET_NEW_TICKETS: str = "SELECT id, user_id, username, text, status FROM tickets WHERE status = 'new'"
_SQL_GET_ALL_TICKETS: str = "SELECT id, user_id, username, created_at, status, text FROM tickets ORDER BY id DESC"
_SQL_GET_USER_TICKETS: str = "SELECT id, created_at, status, text FROM tickets WHERE user_id = ? ORDER BY id DESC"
_SQL_ACCEPT_TICKET: str = "UPDATE tickets SET status = 'accepted' WHERE id = ?"
_SQL_DONE_TICKET: str = "UPDATE tickets SET status = 'done' WHERE id = ?"

_SQL_INSERT_MEDIA: str = "INSERT INTO ticket_media (ticket_id, type, file_id) VALUES (?, ?, ?)"
_SQL_GET_MEDIA: str = "SELECT type, file_id FROM ticket_media WHERE ticket_id = ?"

_SQL_INSERT_CHAT: str = """
INSERT INTO support_chats (chat_id, title, is_active)
VALUES (?, ?, 0)
ON CONFLICT(chat_id) DO UPDATE SET title = excluded.title
"""
_SQL_GET_ACTIVE_CHATS: str = "SELECT chat_id, title, is_active FROM support_chats WHERE is_active = 1"
_SQL_GET_ALL_CHATS: str = "SELECT chat_id, title, is_active FROM support_chats"
_SQL_SET_CHAT_ACTIVE: str = "UPDATE support_chats SET is_active = ?, approved_by = ? WHERE chat_id = ?"

_SQL_INSERT_PUBLICATION: str = "INSERT OR REPLACE INTO publications (ticket_id, chat_id, message_id) VALUES (?, ?, ?)"
_SQL_CHECK_PUBLICATION: str = "SELECT 1 FROM publications WHERE ticket_id = ? AND chat_id = ?"

_SQL_INSERT_LOG: str = "INSERT INTO logs (action, user_id, details) VALUES (?, ?, ?)"


async def init_db() -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(_SQL_CREATE_USERS)
        await db.execute(_SQL_CREATE_TICKETS)
        await db.execute(_SQL_CREATE_TICKET_MEDIA)
        await db.execute(_SQL_CREATE_SUPPORT_CHATS)
        await db.execute(_SQL_CREATE_PUBLICATIONS)
        await db.execute(_SQL_CREATE_LOGS)
        for admin_id in ADMIN_USER_IDS:
            await db.execute(_SQL_SEED_ADMIN, (admin_id,))
        await db.commit()


async def add_or_update_user(telegram_id: int, username: str) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(_SQL_UPSERT_USER, (telegram_id, username))
        await db.commit()


async def get_user_by_id(telegram_id: int) -> Optional[Tuple[int, int, str, str]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(_SQL_GET_USER, (telegram_id,)) as cursor:
            return await cursor.fetchone()


async def get_admin_ids_from_db() -> List[int]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(_SQL_GET_ADMINS) as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]


async def set_user_role(telegram_id: int, role: str) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(_SQL_SET_ROLE, (role, telegram_id))
        await db.commit()


async def save_ticket(user_id: int, username: str, text: str) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(_SQL_INSERT_TICKET, (user_id, username, text))
        await db.commit()
        last_id: int = cursor.lastrowid or 0
        return last_id


async def get_ticket(ticket_id: int) -> Optional[Tuple[int, int, str, str, str]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(_SQL_GET_TICKET, (ticket_id,)) as cursor:
            return await cursor.fetchone()


async def get_new_tickets() -> List[Tuple[int, int, str, str, str]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(_SQL_GET_NEW_TICKETS) as cursor:
            return await cursor.fetchall()


async def get_all_tickets() -> List[Tuple[int, int, str, str, str, str]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(_SQL_GET_ALL_TICKETS) as cursor:
            return await cursor.fetchall()


async def get_user_tickets(telegram_id: int) -> List[Tuple[int, str, str, str]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(_SQL_GET_USER_TICKETS, (telegram_id,)) as cursor:
            return await cursor.fetchall()


async def set_ticket_accepted(ticket_id: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(_SQL_ACCEPT_TICKET, (ticket_id,))
        await db.commit()


async def set_ticket_done(ticket_id: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(_SQL_DONE_TICKET, (ticket_id,))
        await db.commit()


async def save_ticket_media(ticket_id: int, media: List[Tuple[str, str]]) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        for m_type, file_id in media:
            await db.execute(_SQL_INSERT_MEDIA, (ticket_id, m_type, file_id))
        await db.commit()


async def get_ticket_media(ticket_id: int) -> List[Tuple[str, str]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(_SQL_GET_MEDIA, (ticket_id,)) as cursor:
            return await cursor.fetchall()


async def add_support_chat(chat_id: int, title: str) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(_SQL_INSERT_CHAT, (chat_id, title))
        await db.commit()


async def get_active_support_chats() -> List[Tuple[int, str, int]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(_SQL_GET_ACTIVE_CHATS) as cursor:
            return await cursor.fetchall()


async def get_all_chats() -> List[Tuple[int, str, int]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(_SQL_GET_ALL_CHATS) as cursor:
            return await cursor.fetchall()


async def set_chat_active(chat_id: int, is_active: bool, approved_by: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(_SQL_SET_CHAT_ACTIVE, (int(is_active), approved_by, chat_id))
        await db.commit()


async def register_publication(ticket_id: int, chat_id: int, message_id: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(_SQL_INSERT_PUBLICATION, (ticket_id, chat_id, message_id))
        await db.commit()


async def is_ticket_published(ticket_id: int, chat_id: int) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(_SQL_CHECK_PUBLICATION, (ticket_id, chat_id)) as cursor:
            return await cursor.fetchone() is not None


async def log(action: str, user_id: int, details: str) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(_SQL_INSERT_LOG, (action, user_id, details))
        await db.commit()
