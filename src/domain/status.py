"""
Énumération des statuts de ticket.
"""

from enum import Enum


class Status(Enum):
    """
    États possibles d'un ticket.
    """

    OPEN = "Open"
    IN_PROGRESS = "In_progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
