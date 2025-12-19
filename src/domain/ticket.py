"""
Entité Ticket (ticket de support).
"""

from dataclasses import dataclass
from datetime import datetime, timezone

from status import Status


def _now_utc() -> datetime:
    """Retourne l'heure actuelle en UTC."""
    return datetime.now(timezone.utc)


@dataclass
class Ticket:
    """
    Entité principale du domaine : un ticket de support.

    Attributs:
        id: Identifiant unique du ticket
        title: Titre court décrivant le problème
        description: Description détaillée
        status: Status du ticket (OPEN par défaut)
        creator_id: Identifiant du créateur du ticket
        assignee_id: Identifiant de la personne s'occupant du ticket
        created_at: Date et heure de création du ticket
        updated_at: Date et heure de dernière modification du ticket
    """

    id: str
    title: str
    description: str
    status: Status = Status.OPEN
    creator_id: str
    assignee_id: str = None
    created_at: datetime = _now_utc()
    updated_at: datetime = _now_utc()

    def assign(self, user_id: str):
        """Assigne le ticket à un agent."""
        if self.status == Status.CLOSED:
            raise ValueError("Un ticket fermé ne peut plus être modifié")
        if not self.title:
            raise ValueError("Un ticket doit avoir un titre non vide")
        self.assignee_id = user_id
        self.updated_at = _now_utc()

    def close(self):
        """Ferme le ticket."""
        if self.status == Status.CLOSED:
            raise ValueError("Le ticket est fermé")
        self.status = Status.CLOSED
        self.updated_at = _now_utc()
