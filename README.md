CI/CD Pipeline 

1. Contexte
Vous appartenez à une cellule technologique chargée d’automatiser la veille des offres d’emploi dans le domaine du développement logiciel. Votre mission : construire un pipeline CI/CD complet piloté par Jenkins qui

extrait les offres depuis plusieurs sources ;
stocke le résultat au format CSV ;
transforme ce CSV en une page HTML lisible ;
publie automatiquement cette page sur un espace public ;
se déclenche et s’arrête sans intervention manuelle en fonction de la présence (ou non) de nouvelles offres.
2. Objectifs
Compétence visée	Description
Automatisation	Chaîne complète : scraping ➝ transformation ➝ tests ➝ publication.
CI/CD	Intégration et déploiement continus via Jenkins.
Détection de changements	Arrêt prématuré du pipeline si aucune nouveauté.
Déploiement Web	Mise en ligne publique du rapport HTML.
Documentation	Explications claires dans un README.md.
3. Matériel fourni
Fichier	Rôle
scraper.py	Script Python de scraping multi-sources (HackerNews, Python.org, Remotive, JSRemotely, WorkingNomads, AuthenticJobs).
requirements.txt	Dépendances : requests, beautifulsoup4, lxml, pandas.
Remarque : le script complet est annexé en fin d’énoncé ; il génère jobs.csv.

4. Arborescence cible
projet-offres/
├── Jenkinsfile
├── scraper.py
├── html_generator.py        # À créer
├── requirements.txt
├── data/
│   ├── jobs.csv             # Dernière extraction
│   └── jobs_previous.csv    # Extraction précédente
├── public/
│   └── index.html           # Rapport HTML généré
├── logs/
│   └── log.txt              # Historique / erreurs
└── README.md