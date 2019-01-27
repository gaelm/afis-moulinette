# afis-moulinette
[AFIS](https://www.afis.org) moulinette de transformation d'un fichier [EPUB](https://en.wikipedia.org/wiki/EPUB) au format [SPIP](https://www.spip.net) pour la mise en ligne d'un article de SPS.

S'inspire largement de https://github.com/kovidgoyal/calibre
 
**En guise de préparation:**
1. Télécharger et installer [python > 3.6](https://www.python.org/downloads)
2. Récupérer le script [`afis-moulinette.py`](https://github.com/gaelm/afis-moulinette/blob/master/afis-moulinette.py) de conversion EPUB -> SPIP
3. Télécharger comme référence le pdf du SPS à convertir
4. Télécharger et installer [les Xpdf Tools](https://www.xpdfreader.com/download.html)
5. Récupérer toutes les images du SPS: `pdfimages -j SPS.pdf dir`

**Pour chaque article à convertir:**
1. S'attribuer l'article dans la liste de tâches
2. Déplacer le fichier EPUB vers "prepa-en-cours" puis le télécharger
3. Exécuter le script python et ouvrir le fichier résultat: `python afis-moulinette.py SPS_325-P_31-34.epub`
4. Créer un nouvel article avec le titre extrait du fichier résultat: [`https://www.pseudo-sciences.org/ecrire`](https://www.pseudo-sciences.org/ecrire)
5. Ajouter un chapeau: *nom de l'auteur - SPS n° 325 juillet/septembre 2018*
6. Copier les présentations des auteurs dans la partie PostScriptum
7. Enregistrer l'ébauche de l'article
8. Ajouter le mot clé numéro de SPS
9. Modifier l'article pour y copier le contenu entier du fichier produit par le script
10. Visualiser cette première version et la comparer avec la version originale de l'article dans le SPS
11. Corriger le résultat automatique du script
  - suppression des sauts de lignes et éléments inutiles
  - ajout `[(` des encadrés `)]`
  - déplacement des titres des encadrés
  - déplacement et reformatage en italique centré `[|{` des descriptions des images `}|]`
  - insertion d'un saut de ligne forcé `<br/>` après une image ou un encadré et avant le titre suivant
12. Récupérer les images des auteurs et de l'article
13. Redimensionner les images
  - 100x140 pour un auteur
  - 670 de largeur max pour les autres (650 dans un encadré)
14. Insérer les copyrights dans les images en Arial taille 10
15. Télécharger les images dans l'article SPIP
16. Insèrer les images aux bons endroits
17. Regarder toutes les références et remplacer `[les liens->http://www.adresse.com]`
18. Proposer l'article en validation
19. Prévisualiser l'article final et corriger les dernières erreurs
