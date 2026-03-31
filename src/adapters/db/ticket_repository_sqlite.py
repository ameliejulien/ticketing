from typing import List, Optional

from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository

from .database import close_connection, get_connection
from .mappers import row_to_ticket, ticket_to_row


class SQLiteTicketRepository(TicketRepository):
    def __init__(self, db_path: str = "ticketing.db"):
        self.db_path = db_path

    def save(self, ticket: Ticket) -> Ticket:
        """
        Insère ou remplace un ticket dans la table `tickets`.
        Retourne l'entité Ticket (comme contracté par le port).
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        row = ticket_to_row(ticket)
        cursor.execute(
            """
            INSERT OR REPLACE INTO tickets
            (id, title, description, creator_id, status, priority,
            assignee_id, project_id, created_at, updated_at, started_at, closed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["id"],
                row["title"],
                row["description"],
                row["creator_id"],
                row["status"],
                row["priority"],
                row["assignee_id"],
                row["project_id"],
                row["created_at"],
                row["updated_at"],
                row["started_at"],
                row["closed_at"],
            ),
        )
        conn.commit()
        close_connection(conn)
        return ticket

    def get(self, ticket_id: str) -> Optional[Ticket]:
        """
        Récupère un ticket par son id. Retourne None si absent.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        row = cursor.fetchone()
        close_connection(conn)

        if row is None:
            return None

        return row_to_ticket(dict(row))

    def list(self) -> List[Ticket]:
        """
        Liste tous les tickets présents dans la base.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets")
        rows = cursor.fetchall()
        close_connection(conn)

        return [row_to_ticket(dict(r)) for r in rows]
