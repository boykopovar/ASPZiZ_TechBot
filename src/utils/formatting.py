from typing import List, Tuple

from aiogram import types

from src.constants import (
    USER_LINK_USERNAME,
    USER_LINK_ID,
    CAPTION_WITH_LINK,
    SNIPPET_LEN,
    SNIPPET_SUFFIX,
    TG_MAX_CHARS,
    TICKET_LINE_HISTORY,
    TICKET_LINE_ALL,
)


def user_link(user: types.User) -> str:
    if user.username:
        return USER_LINK_USERNAME.format(username=user.username)
    return USER_LINK_ID.format(uid=user.id, name=user.full_name or user.id)


def caption_with_link(text: str, link: str) -> str:
    return CAPTION_WITH_LINK.format(text=text, user_link=link)


def snippet(text: str) -> str:
    if text and len(text) > SNIPPET_LEN:
        return text[:SNIPPET_LEN] + SNIPPET_SUFFIX
    return text or ""


def build_paginated_messages(lines: List[str]) -> List[str]:
    pages: List[str] = []
    current: str = ""
    for line in lines:
        if len(current) + len(line) + 1 > TG_MAX_CHARS:
            pages.append(current)
            current = ""
        current += line + "\n"
    if current:
        pages.append(current)
    return pages


def ticket_history_line(ticket_id: int, status: str, text: str) -> str:
    return TICKET_LINE_HISTORY.format(
        ticket_id=ticket_id, status=status, snippet=snippet(text)
    )


def ticket_all_line(ticket_id: int, status: str, created_at: str, username: str, user_id: int, text: str) -> str:
    return TICKET_LINE_ALL.format(
        ticket_id=ticket_id,
        status=status,
        created_at=created_at,
        username=username or str(user_id),
        snippet=snippet(text),
    )
