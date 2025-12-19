"""
Entité User (utilisateur du système).
"""

from dataclasses import dataclass


@dataclass
class User:
    """
    Représente un utilisateur du système de ticketing.

    Attributes:
        id: Identifiant unique de l'utilisateur
        username: Nom d'affichage de l'utilisateur
        is_agent: L'utilisateur peut traiter des tickets ?
        is_admin: L'utilisateur a des droits administrateur ?
    """

    id: str
    username: str
    is_agent: bool = False
    is_admin: bool = False

def __post_init__(self):
    """S'exécute automatiquement après la création."""
    if not self.username:
        raise ValueError("Username cannot be empty")
