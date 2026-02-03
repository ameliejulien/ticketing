from typing import List, Optional

from src.domain.status import Status
from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository


class ListTicketsUseCase:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo

    def execute(self, status: Optional[Status] = None) -> List[Ticket]:
        all_tickets = self.ticket_repo.list()

        if status is not None:
            filtered_tickets = [
                ticket for ticket in all_tickets if ticket.status == status
            ]
            return filtered_tickets

        return all_tickets
