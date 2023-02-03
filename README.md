# Projet-Androide IHM : Assister l’utilisateur à utiliser les bonnes commandes

2022-2023

Alexandre Xia
Christian Zhuang
Nassim Ahmed Ali

Encadrant: 
Gilles BAILLY

== Contexte ==

De nombreuses commandes sont disponibles dans nos interfaces mais méconnues et/ou non-utilisées par les utilisateurs. Par exemple, dans un éditeur de photo, un utilisateur peut peindre en noir (commande Pinceau + commande Couleur) des yeux rouges sur une image au lieu de d’utiliser la commande “enlever yeux rouges”. Dans un éditeur de texte, l’utilisateur peut écrire deux fois la meme phrase au lieu d’utiliser la commande Copier/Coller, ou encore mieux la commande “Dupliquer”.

== Objectif ==

l’objectif est de développer un assistant pour permettre aux utilisateurs de découvrir et d’utiliser les commandes les plus efficaces dans une interface.

== Approche ==

l’approche consiste à
1) “apprendre” (du point de vue Machine Learning) l’effet de chaque commande sur un document (image, photo, texte, etc.)

2) détecter dans le document un résultat donnée (une phrase dupliquée, des yeux rouges enlevés, etc.)

3) de suggérer la ou les commandes les plus efficaces pour obtenir ce résultat.

L'originalité de ce travail est que, contrairement aux techniques actuelles qui peuvent suggérer des commandes à partir d'une séquence de commande entrées par l'utilisateur (e.g. suggérer dupliquer au lieu de copier + coller), l'approche proposée suggère des commandes en comparant les résultats finaux indépendemment de la séquence de commande entrée par l'utilisateur (i.e. peu importe sur la duplication a été faite via copier/coller au raccourci clavier, copier/coller avec la souris, saisie de texte)

== Travail à réaliser ==

(1) Choisir des scénarios où ce concept serait le plus approprié.

(2) Développer un démonstrateur simple pour illustrer ce concept. On adoptera un design itératif où les parties complexes (e.g. détecter des résultats) pourront dans un premier temps être simplifiées / simulées.

(3) Développer les composants techniques pour réaliser le concept

(4) Réaliser une étude utilisateur pour tester les bénéfices de ce concept

== Compétences nécessaires ==

- compétences en IHM,

- compétence en modélisation

- compétence empirique (réalisation d’étude utilisateur)

== Cadre ==
vous serez accompagnés par deux chercheurs en IHM. Ce travail pourrait donner lieu à une publication scientifique / stage.




