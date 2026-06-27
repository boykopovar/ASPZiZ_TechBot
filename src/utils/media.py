from typing import List, Tuple

from aiogram.types import InputMediaPhoto, InputMediaVideo

from src.types.enums import MediaType


def build_media_group(
    media: List[Tuple[str, str]], caption: str
) -> List[InputMediaPhoto]:
    group: List[InputMediaPhoto] = []
    for m_type, file_id in media:
        if m_type == MediaType.PHOTO:
            group.append(InputMediaPhoto(media=file_id, caption=caption if not group else None))
        elif m_type == MediaType.VIDEO:
            group.append(InputMediaVideo(media=file_id, caption=caption if not group else None))
    return group
