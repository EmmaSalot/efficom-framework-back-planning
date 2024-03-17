# Projet Back-end
## Membres du projet
Hugo Gaudre, Benoît Lavoine et Emma Salot
## Description du projet
Une application permettant de gérer de manière sécurisée les plannings des employés d'entreprises.
## Installation du projet
Pré-requis :
- avoir python
- avoir poetry
- avoir docker
```
git clone https://github.com/EmmaSalot/efficom-framework-back-planning.git
```
## Lancement du projet
```
poetry install
poetry update
docker-compose up --build
```
Une fois que le conteneur docker est lancé se rendre sur http://localhost/docs pour accéder à la documentation FastAPI de notre projet.
Pour pouvoir tester les fonctionnalités du projet voici un utilisateur example : mail = loic_poisot@mail.com / mdp = loic1234
