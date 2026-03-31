## Adaptateurs de persistance

### TicketRepository

**Implémentations disponibles** :
- `InMemoryTicketRepository` : Stockage en mémoire (tests)
- `SQLiteTicketRepository` : Stockage SQLite (production)

**Interchangeabilité** : Les use cases utilisent uniquement le port `TicketRepository`.
Le choix de l'implémentation se fait à l'instanciation (injection de dépendances).

## UserRepository

**Implémentations disponibles** :
- `InMemoryUserRepository` : Stockage en mémoire (tests)
- `SQLiteUserRepository` : Stockage SQLite (production)

**Méthodes spécifiques** :
- `find_by_username(username)` : Recherche par username