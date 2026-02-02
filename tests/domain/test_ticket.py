from datetime import datetime

import pytest

from src.domain.status import Status
from src.domain.ticket import Ticket
from src.domain.user import User


def test_status_values_exist():
    """Vérifie que les 4 statuts existent."""
    assert Status.OPEN.value == "Open"
    assert Status.IN_PROGRESS.value == "In_progress"
    assert Status.RESOLVED.value == "Resolved"
    assert Status.CLOSED.value == "Closed"


def test_user_creation():
    """Vérifie la création d'un utilisateur."""
    user = User(id="u1", username="alice")
    assert user.id == "u1"
    assert user.username == "alice"
    assert not user.is_agent
    assert not user.is_admin


def test_ticket_creation():
    """Vérifie la création d'un ticket avec valeurs par défaut."""
    ticket = Ticket(
        id="t1",
        title="Bug connexion",
        description="Impossible de se connecter",
        creator_id="user1",
    )
    assert ticket.status == Status.OPEN
    assert ticket.assignee_id is None


def test_ticket_assign():
    """Vérifie l'assignation d'un ticket."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.assign("agent1")
    assert ticket.assignee_id == "agent1"


def test_ticket_close():
    """Vérifie la fermeture d'un ticket."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.close()
    assert ticket.status == Status.CLOSED


# ========================================
# | TESTS DES RÈGLES MÉTIER (invariants) |
# ========================================


def test_ticket_title_cannot_be_empty():
    """Règle : Un ticket doit avoir un titre non vide."""
    with pytest.raises(ValueError, match="Ticket title cannot be empty"):
        Ticket(id="t1", title="", description="Une description", creator_id="user1")


def test_user_username_cannot_be_empty():
    """Règle : Un utilisateur doit avoir un username non vide."""
    with pytest.raises(ValueError, match="Username cannot be empty"):
        User(id="u1", username="", is_agent=False, is_admin=False)


def test_cannot_assign_closed_ticket():
    """Règle : Un ticket fermé ne peut plus être assigné."""
    ticket = Ticket(
        id="t1",
        title="Bug connexion",
        description="Impossible de se connecter",
        creator_id="user1",
        status=Status.CLOSED,
    )
    with pytest.raises(ValueError, match="Un ticket fermé ne peut plus être modifié"):
        ticket.assign("user2")


def test_cannot_close_already_closed_ticket():
    """Règle : Un ticket déjà fermé ne peut pas être re-fermé."""
    ticket = Ticket(
        id="t1",
        title="Bug connexion",
        description="Impossible de se connecter",
        creator_id="user1",
    )
    # Fermer le ticket
    ticket.close()
    # Tenter de fermer le ticket à nouveau
    with pytest.raises(ValueError, match="Le ticket est fermé"):
        ticket.close()


# ==========================
# | TESTS DES CAS NOMINAUX |
# ==========================


def test_create_ticket_with_valid_values():
    """Règle : Un ticket peut être créé avec des valeurs valides."""
    ticket = Ticket(
        id="t1", title="Bug valeur", description="Valeur invalide", creator_id="user1"
    )
    assert ticket.title == "Bug valeur"
    assert ticket.status == Status.OPEN
    assert ticket.assignee_id is None
    assert ticket.created_at, datetime


def test_assign_ticket_to_agent():
    """Règle : Un ticket ouvert peut être assigné à un agent."""
    ticket = Ticket(
        id="1",
        title="Bug agent",
        description="Assignation à ticket ouvert",
        creator_id="user_123",
    )
    ticket.assign("agent_123")
    assert ticket.assignee_id == "agent_123"


def test_start_ticket_transition_to_in_progress():
    """Règle : Un ticket assigné peut être démarré."""
    ticket = Ticket(
        id="1",
        title="Bug transition",
        description="Démarrer ticket ouvert",
        creator_id="user_123",
    )
    ticket.status = Status.IN_PROGRESS
    assert ticket.status == Status.IN_PROGRESS


def test_create_user_with_valid_username():
    """Règle : Un utilisateur peut être créé avec un username valide."""
    user = User(id="user_123", username="validuser")
    assert user.username == "validuser"
    assert not user.is_agent
    assert not user.is_admin


def test_ticket_status_on_creation():
    """Règle : Un ticket a le statut OPEN à sa création."""
    ticket = Ticket(
        id="1",
        title="Bug ouverte",
        description="Statut du ticket",
        creator_id="user_123",
    )
    assert ticket.status == Status.OPEN


# ==========================
# | TESTS DES CAS D'ERREUR |
# ==========================


def test_user_roles():
    """Règle : Un utilisateur peut avoir un rôle."""
    user = User(id="u1", username="alice", is_agent=True, is_admin=False)
    assert user.is_agent is True
    assert user.is_admin is False
    user2 = User(id="u2", username="bob", is_agent=False, is_admin=True)
    assert user2.is_agent is False
    assert user2.is_admin is True


def test_closed_ticket_cannot_be_opened():
    """Règle : Un ticket fermé ne peut plus être ouvert."""
    ticket = Ticket(
        id="t1",
        title="Bug connexion",
        description="Impossible de se connecter",
        creator_id="user1",
    )
    ticket.close()
    with pytest.raises(ValueError, match="Cannot open a closed ticket"):
        ticket.open()  # Cela devrait lever une exception


def test_ticket_description_cannot_be_empty():
    """Règle : Un ticket doit avoir une description."""
    with pytest.raises(ValueError, match="Ticket description cannot be empty."):
        Ticket(id="t1", title="Bug connexion", description="", creator_id="user1")


def test_ticket_status_must_be_valid():
    """Règle : Un ticket doit avoir un statut valide."""
    with pytest.raises(ValueError, match="Ticket status must be valid."):
        Ticket(
            id="t1",
            title="Bug connexion",
            description="Impossible de se connecter",
            creator_id="user1",
            status="INVALID_STATUS",
        )


def test_ticket_creation_date_cannot_be_empty():
    """Règle : Un ticket doit avoir une date de création non vide."""
    with pytest.raises(ValueError, match="Ticket creation date cannot be empty."):
        Ticket(
            id="t1",
            title="Bug connexion",
            description="Impossible de se connecter",
            creator_id="user1",
            created_at=None,
        )


def test_ticket_update_date_cannot_be_empty():
    """Règle : Un ticket doit avoir une date de mise à jour non vide."""
    with pytest.raises(ValueError, match="Ticket update date cannot be empty."):
        Ticket(
            id="t1",
            title="Bug connexion",
            description="Impossible de se connecter",
            creator_id="user1",
            updated_at=None,
        )
