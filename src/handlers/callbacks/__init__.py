from aiogram import Router

from src.handlers.callbacks.ticket_callbacks import _router as _ticket_cb_router
from src.handlers.callbacks.chat_callbacks import _router as _chat_cb_router

callbacks_router = Router()
callbacks_router.include_router(_ticket_cb_router)
callbacks_router.include_router(_chat_cb_router)
