# Principe de fonctionnement du choixpeau magique

Les questions proviennent du site suivant : https://harrypotter.fandom.com/fr/wiki/Pottermore/R%C3%A9partition

Le quiz comporte sept questions. Chaque question possède plusieurs variations (de trois à six).
Pour décider de l'affectation d'une personne à une maison, une seule variation de chaque question est posée dans la version classique du quiz.

Certaines réponses sont exclusives à une maison tandis que d'autres peuvent être associées à plusieurs maisons.

La somme des points obtenus par chaque maison permet de déterminer l'affectation du choixpeau magique !

# Installation

Copier le package dans un répertoire et créez un nouvel environnement virtuel :

```sh
python3 -m venv venv
```

Activez ce nouvel environnement :

```sh
. venv/bin/activate
```

Installez le package :

```sh
pip install --editable .
```

# Utilisation

L'utilisation se fait via la ligne de commande.

Pour lancer la répartition du choixpeau, utilisez la commande suivante :

```sh
sorting-hat sort
```

Répondez ensuite aux sept questions pour connaître votre maison !

> Note : Il est possible de jouer à une version longue du quiz avec l'ensemble des variations de chaque question en utilisant le flag `--long-quiz`.
