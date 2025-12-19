"""
Entité User (utilisateur du système).

TODO (TD01) : Compléter cette classe avec les attributs nécessaires.
"""

from dataclasses import dataclass


@dataclass
class User:
    """
    Représente un utilisateur du système de ticketing.

    TODO: Définir les attributs nécessaires.
    Réfléchissez aux informations minimales pour identifier un utilisateur
    et distinguer ses rôles (simple utilisateur, agent support, admin...).

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
