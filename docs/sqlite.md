Q1. Ouvrez InMemoryTicketRepository. Quelles méthodes implémente-t-il ?
    save(ticket) -> Ticket, get_by_id(ticket_id) -> Optional[Ticket], list_all() -> list[Ticket], et parfois clear()

Q2. Ouvrez ports/ticket_repository.py. Ce sont les mêmes méthodes ?
    Oui. Le port définit l'interface contractuelle que les adaptateurs doivent implémenter.
    L'implémentation InMemory et l'implémentation SQLite respectent ces mêmes méthodes.

Q3. Si vous remplacez InMemory par SQLite dans un use case, que devez-vous modifier :
    a) Le code du use case ? 
        Non
    b) Les tests du use case ? 
        Non
    c) Uniquement l'instanciation du repository ? 
        Oui, que l'implémentation injectée au moment de la composition.

Q6. Pourquoi peut-on facilement passer de InMemory à SQLite ?
    Parce que les deux implémentations respectent le même port/contrat. Les use cases dépendent du port abstrait, pas des détails concrets. On change seulement l'implémentation au niveau de l'assemblage.

Q7. Si demain vous devez utiliser PostgreSQL, quels fichiers changent ?
    Principalement l'adaptateur : créer un nouveau fichier/adaptateur qui implémente le port. Aussi des helpers de connexion et les mappers si nécessaires. Les use cases et le domaine ne changent pas. Les tests peuvent ajouter une fixture spécifique pour Postgres.

Q8. Quel est l'avantage d'avoir InMemory et SQLite ?
    InMemory : rapide, idéal pour tests unitaires et développement, pas de dépendance externe, démarrage instantané.
    SQLite : persistance légère pour tests d'intégration ou production simple, permet vérifier la persistance réelle et les requêtes SQL.
    Avoir les deux permet tests rapides + tests réalistes, et démontre l'interchangeabilité des adaptateurs via le port.
    Exemples de tests à ajouter
    Créez un fichier de test. Ces exemples utilisent la fixture sqlite_ticket_repo fournie dans tests/conftest.py.