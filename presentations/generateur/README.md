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
node build.js .          # écrit konformix-kontrol.pptx et konformix-vigil.pptx
```

Le `.potx` se fabrique à partir du `.pptx` en remplaçant, dans
`[Content_Types].xml`, le type `presentationml.presentation.main+xml` par
`presentationml.template.main+xml`.

## Plan des quatorze diapositives

1. Couverture — logo, module, promesse
2. La société — Konformix en bref et l'équipe fondatrice
3. Le contexte — trois chiffres du cadre UEMOA
4. Le signal — mesures de la Commission Bancaire de l'UMOA, 2024 contre 2025
5. Le constat — quatre faiblesses du référentiel client
6. Le module — promesse et résultat visé
7. Fonctionnalités — les six briques
8. En pratique — les cinq indicateurs (Kontrol) ou seuil fixe contre profil (Vigil)
9. Bénéfices — trois gains mesurables
10. Interlocuteurs — quatre fonctions et leur besoin
11. Positionnement — quatre différenciateurs
12. La démarche — quatre étapes
13. Objections — trois questions fréquentes
14. Prochaine étape — le diagnostic et le contact

Chaque diapositive porte une note de présentateur.
