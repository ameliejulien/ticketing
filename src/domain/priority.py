from enum import Enum


class Priority(Enum):
    """
    Enumération pour définir les priorités des tickets.
    """

    LOW = "Basse"
    MEDIUM = "Moyenne"
    HIGH = "Élevée"
    CRITICAL = "Critique"

    def __str__(self):
        return self.value
