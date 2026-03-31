"""
Tests du use case AssignTicket.
"""

import pytest

from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.application.usecases.assign_ticket import AssignTicketUseCase
from src.application.usecases.create_ticket import CreateTicketUseCase
from src.domain.exceptions import TicketNotFoundError
from src.domain.status import Status


class TestAssignTicketUseCase:
    """Suite de tests pour l'assignation de tickets."""

    def setup_method(self):
        """Initialise le repository et les use cases."""
        self.repo = InMemoryTicketRepository()
        self.create_use_case = CreateTicketUseCase(self.repo)
        self.assign_use_case = AssignTicketUseCase(self.repo)

    def test_assign_ticket_success(self):
        """Doit assigner un ticket à un agent."""
        # Arrange - Créer un ticket d'abord
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )
        agent_id = "agent-456"

        # Act
        updated_ticket = self.assign_use_case.execute(ticket.id, agent_id)

        # Assert
        assert updated_ticket.assignee_id is not None
        assert updated_ticket.assignee_id == agent_id

    def test_assign_nonexistent_ticket_raises_error(self):
        """Doit lever une erreur si le ticket n'existe pas."""
        # Arrange
        fake_id = "ticket-inexistant"
        agent_id = "agent-789"

        # Act & Assert
        with pytest.raises(TicketNotFoundError):
            self.assign_use_case.execute(fake_id, agent_id)

    def test_assign_ticket_persists_change(self):
        """Doit persister l'assignation dans le repository."""
        # Arrange - Créer un ticket
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )
        agent_id = "agent-999"

        # Act
        updated_ticket = self.assign_use_case.execute(ticket.id, agent_id)
        assert updated_ticket.assignee_id is not None
        assert updated_ticket.assignee_id == agent_id

        # Assert - Récupérer depuis le repo pour vérifier la persistance
        saved_ticket = self.repo.get(ticket.id)
        assert saved_ticket.assignee_id is not None
        assert saved_ticket.assignee_id == agent_id

    def test_assign_ticket_with_sqlite(self, sqlite_ticket_repo):
        """Créer puis assigner un ticket en utilisant le repo SQLite."""
        repo = sqlite_ticket_repo
        create_uc = CreateTicketUseCase(repo)
        assign_uc = AssignTicketUseCase(repo)

        ticket = create_uc.execute(
            title="Nouvelle fonctionnalité",
            description="Ajouter export CSV",
            creator_id="user-123",
        )

        # Assigner à un agent
        assigned = assign_uc.execute(ticket_id=ticket.id, agent_id="agent-456")

        assert assigned.assignee_id == "agent-456"
        assert assigned.status == Status.OPEN

        # Lire depuis la DB pour confirmer
        retrieved = repo.get(ticket.id)
        assert retrieved.assignee_id == "agent-456"
