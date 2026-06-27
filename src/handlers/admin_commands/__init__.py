from aiogram import Router

from src.handlers.admin_commands.chat_commands import _router as _chat_cmd_router
from src.handlers.admin_commands.chat_member import _router as _chat_member_router
from src.handlers.admin_commands.ticket_commands import _router as _ticket_cmd_router
from src.handlers.admin_commands.role_commands import _router as _role_cmd_router
from src.handlers.admin_commands.help_command import _router as _help_cmd_router

admin_router = Router()
admin_router.include_router(_chat_member_router)
admin_router.include_router(_chat_cmd_router)
admin_router.include_router(_ticket_cmd_router)
admin_router.include_router(_role_cmd_router)
admin_router.include_router(_help_cmd_router)
