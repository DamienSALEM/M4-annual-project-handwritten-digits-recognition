# Projet fin d'année de M1 IPSSI

Projet de Machine Learning / Deep Learning pour la reconnaissance de chiffres écrits à la main.

## Participants

Simon DANIEL
Lucas MONNET-POUPON
Ali-Haïdar ATIA
Damien SALEM

## Langages, versions et dépendances

Python 3.11
_pip install -r requirements.txt_
React
MongoDB

## Comment installer le projet?

## Points principaux


### FRONT

Un formulaire avec un canvas pour que l'utilisateur dessine un chiffre que notre IA pourra analyser.

### API

API en django, 1 route qui récupère l'image du front, transforme l'image et données utilisables par l'IA, stock l'image et la prédiction de l'IA en BDD et renvoie la prédiction au front.

### Machine Learning / Deep Learning

2 algos retenus, random forest et CNN.
Pour le random forest, la fonction RandozimedSearchCV a été utilisé pour chercher les meilleurs hyper paramètres.

### Base de données

Base de données sur Mongo Atlas avec accès par pymongo (librairie python)
