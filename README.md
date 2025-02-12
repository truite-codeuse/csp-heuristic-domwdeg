# csp-heuristic-domwdeg
## Installation
Après avoir cloné le repertoire, aucune installation n'est nécessaire. Ce projet n'utilise que Python3 sans bibliothèque.

## Lancer le programme
NE PAS LANCER LES PROGRAMMES CONTENUS DANS :
- `create_data.py` -> cela va effacer les instances de problèmes utilisées pour le rapport et les remplacer par de nouvelles
- `expe.py` - cela va relancer le calcul des temps d'exécution des heuristiques et remplacer les données déjà calculées

Pour tester le solveur, utiliser les fichiers `test1.py` et `test2.py` qui vont chacun lancer une résolution pour un problème vu en cours (celui avec la coloration de cartes).

- `python3 test1.py` donne une solution, "lexico" fait 11 erreurs et les deux autres méthodes en font 4
- `python3 test2.py` ne trouve pas de solution (car pas AC)

Vous pouvez modifier l'heuristique en changeant l'argument passé à la fonction `BackTracking().solve(..., method)` où `method` peut valoir "lexico", "dom_wdeg" ou "dom_wdeg_wattez".
