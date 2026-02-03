"""
Adaptateur de persistance en mémoire pour les tickets.

Cette implémentation stocke les tickets dans un dictionnaire Python.
Utile pour les tests et le développement, mais les données sont perdues
au redémarrage de l'application.

À remplacer par un adaptateur SQLite pour la persistence réelle.
"""

from typing import Dict, List, Optional

from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository


class InMemoryTicketRepository(TicketRepository):
    """
    Repository de tickets stockant les données en mémoire.

    Implémente l'interface TicketRepository en utilisant un dictionnaire
    comme stockage. Les tickets sont indexés par leur identifiant unique.
    """

    def __init__(self):
        """Initialise le stockage avec un dictionnaire vide."""
        self._tickets: Dict[str, Ticket] = {}

    def save(self, ticket: Ticket) -> Ticket:
        """
        Sauvegarde un ticket dans le dictionnaire.

        Si le ticket existe déjà (même id), il est remplacé.

        Args:
            ticket: Le ticket à sauvegarder
        """
        self._tickets[ticket.id] = ticket
        return ticket

    def get(self, ticket_id: str) -> Optional[Ticket]:
        """
        Récupère un ticket par son identifiant.

        Args:
            ticket_id: L'identifiant unique du ticket

        Returns:
            Le ticket trouvé, ou None s'il n'existe pas
        """
        return self._tickets.get(ticket_id)

    def list(self) -> List[Ticket]:
        """
        Récupère tous les tickets stockés.

        Returns:
            Liste de tous les tickets
        """
        return list(self._tickets.values())

    def clear(self):
        """
        Vide le repository (utile pour les tests).

        Note: Cette méthode n'est pas dans le port, elle est spécifique
        à l'implémentation InMemory pour faciliter les tests.
        """
        self._tickets.clear()
