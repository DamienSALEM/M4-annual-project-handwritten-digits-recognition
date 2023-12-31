# Projet fin d'année de M1 IPSSI

Projet de Machine Learning / Deep Learning pour la reconnaissance de chiffres écrits à la main.

## Participants

Simon DANIEL
Lucas MONNET-POUPON
Ali-Haïdar ATIA
Damien SALEM

## Langages, versions et dépendances

Python 3.11
React
MongoDB

## Liens du projet

https://tome.app/data-506
https://trello.com/b/415rc4vu/suivi-de-projet
https://github.com/DamienSALEM/M4-annual-project-handwritten-digits-recognition.git

## Comment installer et lancer le projet?

Récupérer le .env et le mettre dans le backend
_cd projet annuel_
_python -m venv .venv_
_pip install -r requirements.txt_
_cd WEB_
_npm install_
_npm run dev_
Dans un autre terminal:
_cd API/backend_
_python manage.py runserver_

## Points bloquants

1. Problème lors de l'envoie de l'image du front vers l'API, format de l'image et transformation en données utilisable par le modèle (jpg/png, encodage en base 64 et resize)
2. Probabilité basse du modèle et erreurs de prédiction (sur ou sous entrainement)

### FRONT

Un formulaire avec un canvas pour que l'utilisateur dessine un chiffre que notre IA pourra analyser.

### API

API en django, 1 route qui récupère l'image du front, transforme l'image en données utilisables par le modèle, stock l'image et la prédiction de l'IA en BDD et renvoie la prédiction et la probabilité au front.

### Machine Learning / Deep Learning

2 algos retenus, random forest et CNN.
Pour le random forest, la fonction RandozimedSearchCV a été utilisé pour chercher les meilleurs hyper paramètres.
Le CNN a une meilleur précision mais demande plus de temps pour les prédictions tandis que le random forest est moins précis mais donne des prédictions plus rapidement.
Le modèle du random forest étant trop lourd, l'idée d'avoir 2 modèles a été abandonné.

### Base de données

Base de données sur Mongo Atlas avec accès par pymongo (librairie python).
1 collection avec l'image et la prédiction du modèle.

### Docker
Mise en place d'un fichier docker-compose.yaml et des dockerfile pour déployer l'application
