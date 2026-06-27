from src.constants import CB_PREFIX_ACCEPT, CB_PREFIX_DONE
from aiogram.filters.callback_data import CallbackData


class AcceptTicketCb(CallbackData, prefix=CB_PREFIX_ACCEPT):
    ticket_id: int


class DoneTicketCb(CallbackData, prefix=CB_PREFIX_DONE):
    ticket_id: int
