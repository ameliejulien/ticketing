from src.domain.exceptions import TicketNotFoundError
from src.domain.ticket import Ticket
from src.ports.clock import Clock
from src.ports.ticket_repository import TicketRepository


class StartTicketUseCase:
    def __init__(self, ticket_repo: TicketRepository, clock: Clock):
        self.ticket_repo = ticket_repo
        self.clock = clock

    def execute(self, ticket_id: str, agent_id: str) -> Ticket:
        # Récupérer le ticket
        ticket = self.ticket_repo.get(ticket_id)

        # Vérifier l'existence du ticket
        if ticket is None:
            raise TicketNotFoundError(f"Ticket {ticket_id} not found")

        # Obtenir l'heure actuelle
        started_at = self.clock.now()

        # Démarrer le ticket
        ticket.start(agent_id, started_at)

        # Enregistrer
        self.ticket_repo.save(ticket)

        # Retourner
        return ticket
