from dataclasses import dataclass
from datetime import datetime, timezone

from status import Status


def _now_utc() -> datetime:
    """Retourne l'heure actuelle en UTC."""
    return datetime.now(timezone.utc)


@dataclass
class Ticket:
    id: str
    title: str
    description: str
    status: Status = Status.OPEN
    creator_id: str
    assignee_id: str = None
    created_at: datetime = _now_utc()
    updated_at: datetime = _now_utc()

    def assign(self, user_id: str):
        if self.status == Status.CLOSED:
            raise ValueError("Un ticket fermé ne peut plus être modifié")
        if not self.title:
            raise ValueError("Un ticket doit avoir un titre non vide")
        self.assignee_id = user_id
        self.updated_at = _now_utc()

    def close(self):
        if self.status == Status.CLOSED:
            raise ValueError("Le ticket est fermé")
        self.status = Status.CLOSED
        self.updated_at = _now_utc()

    def __post_init__(self):
        if not self.title:
            raise ValueError("Ticket title cannot be empty")
