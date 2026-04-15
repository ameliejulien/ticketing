from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from src.domain.exceptions import (
    InvalidTicketStateError,
    TicketNotAssignedError,
    WrongAgentError,
)
from src.domain.priority import Priority
from src.domain.status import Status


def _now_utc() -> datetime:
    """Retourne l'heure actuelle en UTC."""
    return datetime.now(timezone.utc)


_SENTINEL = object()


@dataclass
class Ticket:
    id: str
    title: str
    description: str
    creator_id: str
    priority: Priority = Priority.MEDIUM
    status: Status = Status.OPEN
    assignee_id: str = None
    created_at: datetime = field(default_factory=_now_utc)
    updated_at: datetime = field(default_factory=_now_utc)
    started_at: Optional[datetime] = None
    project_id: Optional[str] = None
    closed_at: Optional[datetime] = None

    ALLOWED_TRANSITIONS = {
        Status.OPEN: [Status.IN_PROGRESS],
        Status.IN_PROGRESS: [Status.RESOLVED],
        Status.RESOLVED: [Status.CLOSED, Status.IN_PROGRESS],
    }

    def assign(self, agent_id: str, updated_at=None) -> None:
        if self.status != Status.CLOSED and self.status == Status.CLOSED:
            raise ValueError("Cannot assign a closed ticket")
        if self.status == Status.CLOSED:
            raise ValueError("Un ticket fermé ne peut plus être modifié")
        if self.assignee_id is not None:
            raise ValueError("Ticket already assigned")
        self.assignee_id = agent_id
        self.updated_at = updated_at or _now_utc()

    def close(self):
        if self.status == Status.CLOSED:
            raise ValueError("Le ticket est fermé")
        self.status = Status.CLOSED
        self.updated_at = _now_utc()

    def open(self):
        if self.status == Status.CLOSED:
            raise ValueError("Cannot open a closed ticket")
        self.status = Status.OPEN
        self.updated_at = _now_utc()

    def start(self, agent_id: str, started_at: datetime) -> None:
        if self.assignee_id is None:
            raise TicketNotAssignedError("Ticket is unassigned")
        if self.assignee_id != agent_id:
            raise WrongAgentError(
                f"Only agent {self.assignee_id} can start this ticket, not {agent_id}"
            )
        if self.status != Status.OPEN:
            raise InvalidTicketStateError(
                f"Ticket must be OPEN to start, current status: {self.status.value}"
            )
        self.transition_to(Status.IN_PROGRESS, started_at)
        self.started_at = started_at

    def transition_to(self, new_status: Status, updated_at: datetime) -> None:
        """Fait transiter le ticket vers un nouveau statut."""
        if new_status not in self.ALLOWED_TRANSITIONS.get(self.status, []):
            raise ValueError(
                f"Cannot transition from {self.status.value} to {new_status.value}"
            )
        self.status = new_status
        self.updated_at = updated_at

    def _restore_status_from_db(self, status: Status) -> None:
        self.status = status

    def __post_init__(self):
        if not self.title:
            raise ValueError("Ticket title cannot be empty")
        if not self.description:
            raise ValueError("Ticket description cannot be empty.")
        if not isinstance(self.status, Status):
            raise ValueError("Ticket status must be valid.")
        if self.created_at is None:
            raise ValueError("Ticket creation date cannot be empty.")
        if self.updated_at is None:
            raise ValueError("Ticket update date cannot be empty.")
