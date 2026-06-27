from enum import Enum


class TicketStatus(str, Enum):
    NEW = "new"
    ACCEPTED = "accepted"
    DONE = "done"
