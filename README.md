# afis-moulinette
[AFIS](https://www.afis.org) moulinette de transformation d'un fichier [EPUB](https://en.wikipedia.org/wiki/EPUB) au format [SPIP](https://www.spip.net) pour la mise en ligne d'un article de SPS.

S'inspire largement de https://github.com/kovidgoyal/calibre
 
## En guise de préparation:
1. Télécharger et installer [python > 3.6](https://www.python.org/downloads)
2. Récupérer le script [`afis-moulinette.py`](https://github.com/gaelm/afis-moulinette/blob/master/afis-moulinette.py) de conversion EPUB -> SPIP
3. Télécharger comme référence le pdf du SPS à convertir
4. Télécharger et installer [les Xpdf Tools](https://www.xpdfreader.com/download.html)
5. Récupérer toutes les images du SPS: `pdfimages -j SPS.pdf dir`
6. Télécharger [GIMP](https://www.gimp.org/downloads) ou un autre éditeur d'images

## Pour chaque article à convertir:
1. S'attribuer l'article dans la liste de tâches
2. Déplacer le fichier EPUB vers "prepa-en-cours" puis le télécharger
3. Exécuter le script python et ouvrir le fichier résultat: `python afis-moulinette.py SPS_325-P_31-34.epub`
4. Créer un nouvel article avec le titre extrait du fichier résultat: [`https://www.pseudo-sciences.org/ecrire`](https://www.pseudo-sciences.org/ecrire) puis cliquer sur *Écrire un nouvel article*
   - Ajouter un soustitre si présent ou le surtitre comme soustitre si ce n'est pas un dossier ou une rubrique
5. Ajouter un chapeau: *nom de l'auteur - SPS n° 325 juillet/septembre 2018*
6. Copier les présentations des auteurs dans la partie PostScriptum
   - Vérifier la description des auteurs: ``{{Prénom Nom}} est fonction``
7. Enregistrer l'ébauche de l'article
8. Ajouter le mot clé numéro de SPS
9. Modifier l'article pour y copier le contenu entier du fichier produit par le script
10. Visualiser cette première version et la comparer avec la version originale de l'article dans le SPS
11. Corriger le résultat automatique du script en suivant [la syntaxe SPIP](https://www.spip.net/fr_rubrique483.html)
    - Suppression des sauts de lignes et éléments inutiles
    - Ajout `[(` des encadrés `)]`
    - Déplacement des titres des encadrés
    - Déplacement et reformatage en italique centré `[|{` des descriptions des images `}|]`
    - Insertion d'un saut de ligne forcé `<br/>` après une image ou un encadré et avant le titre suivant
    - Pour une note de lecture: ajouter au début le titre, soustitre, auteurs et éditeur en `[(` encadré `)]`
12. Récupérer les images des auteurs et de l'article extraites par `pdfimages` et les comparer avec celles contenues dans l'archive epub
    - Le fichier epub est une archive zip qui peut se décompresser
    - Choisir la meilleure version
13. Redimensionner et éditer les images
    - 100x140 pour un auteur
    - 670 de largeur max pour les autres (650 dans un encadré)
    - Insérer les copyrights dans les images en Arial taille 10
14. Télécharger [les images dans l'article SPIP](https://www.spip.net/fr_article5631.html)
15. Insérer les images aux bons endroits de l'article
16. Corriger les formules de `<math>$` math `$</math>` dans le texte et centrer `<math>$$` les grandes formules `$$</math>`
16. Regarder toutes les références et remplacer `[les liens->http://www.adresse.com]`
17. Proposer l'article en validation
18. Prévisualiser l'article final et corriger les dernières erreurs
