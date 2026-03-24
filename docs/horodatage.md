Q1. Comment obtenir la date/heure actuelle en Python ?
    Avec le module datetime de stdlib : datetime.datetime.now()

Q2. Si on met datetime.now() dans le use case, pourquoi c'est problématique pour les tests ?
    Il lit l'heure du système donc chaque exécution peut donner un résultat différent
    Il empêche de reproduire facilement des scénarios temporels
    Il rend difficile le test de comportements dépendant du temps

Q3. Au TD2a, comment avez-vous géré la base de données pour que les tests soient indépendants ?
    J'ai isolé l'accès à la BDD derrière une interface et fourni des adaptateurs
    Les tests utilisaient l'adaptateur de test, assurant l'indépendance et la reproductibilité

Q4. Quelle architecture du TD2a pourrait s'appliquer ici ?
    Même approche hexagonale : définir un port Clock qui dépend du use case
