from aiogram import Router

from src.handlers.commands.start import _router as _start_router
from src.handlers.commands.help_cmd import _router as _help_router
from src.handlers.commands.who_am_i import _router as _who_am_i_router
from src.handlers.commands.my_history import _router as _my_history_router
from src.handlers.commands.fallback import _router as _fallback_router

commands_router = Router()
commands_router.include_router(_start_router)
commands_router.include_router(_help_router)
commands_router.include_router(_who_am_i_router)
commands_router.include_router(_my_history_router)
commands_router.include_router(_fallback_router)
