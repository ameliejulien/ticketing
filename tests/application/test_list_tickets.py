from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.application.usecases.create_ticket import CreateTicketUseCase
from src.application.usecases.list_tickets import ListTicketsUseCase
from src.domain.status import Status


class TestListTicketsUseCase:
    def setup_method(self):
        self.repo = InMemoryTicketRepository()
        self.create_use_case = CreateTicketUseCase(self.repo)
        self.list_use_case = ListTicketsUseCase(self.repo)

    def test_list_all_tickets(self):
        self.create_use_case.execute("Bug 1", "Description 1", "user-1")
        self.create_use_case.execute("Bug 2", "Description 2", "user-2")

        tickets = self.list_use_case.execute()

        assert len(tickets) == 2

    def test_list_tickets_by_status(self):
        ticket1 = self.create_use_case.execute("Bug 1", "Description 1", "user-1")
        ticket1.close()

        ticket2 = self.create_use_case.execute("Bug 2", "Description 2", "user-2")

        closed_tickets = self.list_use_case.execute(Status.CLOSED)

        assert len(closed_tickets) == 1
        assert closed_tickets[0].id == ticket1.id

        open_tickets = self.list_use_case.execute(Status.OPEN)

        assert len(open_tickets) == 1
        assert open_tickets[0].id == ticket2.id
