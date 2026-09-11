# Générateur des présentations commerciales

Deux présentations, une par module, chacune ouverte par la présentation de la
société : `konformix-kontrol` et `konformix-vigil`, livrées en `.potx` (modèle
PowerPoint) et en `.pptx` (présentation directement projetable).

Le contenu vient du site (`core/content.py`), resserré pour la diapositive :
il est isolé dans `content.js` pour que le discours commercial évolue sans
toucher à la mise en page.

## Régénérer

```bash
npm install pptxgenjs react react-dom react-icons sharp
node build.js .
```

Quatre fichiers sont écrits : `konformix-<module>.pptx`, la présentation
projetée avec son sommaire, et `konformix-<module>-modele.pptx`, la même
sans sommaire, qui sert de base au `.potx`.

Le `.potx` se fabrique à partir du fichier `-modele` en remplaçant, dans
`[Content_Types].xml`, le type `presentationml.presentation.main+xml` par
`presentationml.template.main+xml`.

## Plan des quinze diapositives

1. Couverture — logo, module, promesse
2. Sommaire — quatre temps et leur pagination (présentation projetée seulement)
3. La société — Konformix en bref et l'équipe fondatrice
4. Le contexte — trois chiffres du cadre UEMOA
5. Le signal — mesures de la Commission Bancaire de l'UMOA, 2024 contre 2025
6. Le constat — quatre faiblesses du référentiel client
7. Le module — promesse et résultat visé
8. Fonctionnalités — les six briques
9. En pratique — les cinq indicateurs (Kontrol) ou seuil fixe contre profil (Vigil)
10. Bénéfices — trois gains mesurables
11. Interlocuteurs — quatre fonctions et leur besoin
12. Positionnement — quatre différenciateurs
13. La démarche — quatre étapes
14. Objections — trois questions fréquentes
15. Prochaine étape — le diagnostic et le contact

Chaque diapositive porte une note de présentateur.
