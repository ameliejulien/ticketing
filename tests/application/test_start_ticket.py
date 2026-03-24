from datetime import datetime, timezone

import pytest

from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.adapters.fixed_clock import FixedClock
from src.application.usecases.assign_ticket import AssignTicketUseCase
from src.application.usecases.create_ticket import CreateTicketUseCase
from src.application.usecases.start_ticket import StartTicketUseCase
from src.domain.exceptions import (
    InvalidTicketStateError,
    TicketNotAssignedError,
    TicketNotFoundError,
    WrongAgentError,
)
from src.domain.status import Status


class TestStartTicketUseCase:
    def setup_method(self):
        self.repo = InMemoryTicketRepository()
        self.fixed_time = datetime(2026, 1, 16, 14, 30, 0, tzinfo=timezone.utc)
        self.clock = FixedClock(self.fixed_time)
        self.create_use_case = CreateTicketUseCase(self.repo)
        self.assign_use_case = AssignTicketUseCase(self.repo)
        self.start_use_case = StartTicketUseCase(self.repo, self.clock)

    def test_start_ticket_success(self):
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )
        agent_id = "agent-456"
        self.assign_use_case.execute(ticket.id, agent_id)

        started_ticket = self.start_use_case.execute(ticket.id, agent_id)

        assert started_ticket.status == Status.IN_PROGRESS
        assert started_ticket.started_at == self.fixed_time
        assert started_ticket.assignee_id == agent_id

    def test_start_ticket_not_found(self):
        with pytest.raises(TicketNotFoundError):
            self.start_use_case.execute("ticket-inexistant", "agent-789")

    def test_start_ticket_invalid_status(self):
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )
        agent_id = "agent-456"
        self.assign_use_case.execute(ticket.id, agent_id)
        self.start_use_case.execute(ticket.id, agent_id)
        with pytest.raises(InvalidTicketStateError):
            self.start_use_case.execute(ticket.id, agent_id)

    def test_start_ticket_not_assigned(self):
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )
        with pytest.raises(TicketNotAssignedError):
            self.start_use_case.execute(ticket.id, "agent-789")

    def test_start_ticket_wrong_agent(self):
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )
        assigned_agent = "agent-456"
        self.assign_use_case.execute(ticket.id, assigned_agent)
        wrong_agent = "agent-999"
        with pytest.raises(WrongAgentError):
            self.start_use_case.execute(ticket.id, wrong_agent)

    def test_start_ticket_persists_change(self):
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )
        agent_id = "agent-456"
        self.assign_use_case.execute(ticket.id, agent_id)
        self.start_use_case.execute(ticket.id, agent_id)
        persisted_ticket = self.repo.get(ticket.id)
        assert persisted_ticket.status == Status.IN_PROGRESS
        assert persisted_ticket.started_at == self.fixed_time

    def test_start_ticket_deterministic_with_fixed_clock(self):
        agents = ["agent-1", "agent-2", "agent-3"]
        tickets = []

        for i, agent in enumerate(agents):
            ticket = self.create_use_case.execute(
                f"Bug {i}", f"Description {i}", "user-123"
            )
            self.assign_use_case.execute(ticket.id, agent)
            tickets.append(ticket)

        started_tickets = []
        for ticket, agent in zip(tickets, agents):
            started = self.start_use_case.execute(ticket.id, agent)
            started_tickets.append(started)

        for started in started_tickets:
            assert started.started_at == self.fixed_time
