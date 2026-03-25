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