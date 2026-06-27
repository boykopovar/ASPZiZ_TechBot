from aiogram import Router

from src.handlers.messages.ticket_messages import _router as _ticket_router

messages_router = Router()
messages_router.include_router(_ticket_router)
