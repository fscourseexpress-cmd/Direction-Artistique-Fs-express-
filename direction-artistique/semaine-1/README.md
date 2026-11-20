# Semaine 1 (23–29 novembre 2026) — créas non vidéo

Source : `FS_Course_Planning_Semaine1_FinalVersion.xlsx` et la direction artistique FS Express.
67 visuels dans `png/`, nommés par le code du planning (ex. `LU-FB2-3` = lundi, Facebook, 2e publication, slide 3).

## Régénérer

```
python3 build.py        # écrit creas.html
node export.js          # exporte png/*.png et signale les débordements
node export.js DI-FB3   # 2e passe pour le récap (il reprend des vignettes)
```

`sources/retouche-photos.py` contient la retouche des trois photos (polo et sac passés en bleu, faux logo du carton effacé, lumières orange passées en rouge).

## Créas produites

| Jour | Codes | Formats |
|---|---|---|
| Lundi | LU-FB1, LU-FB2 (5), LU-FB3, LU-IG2 (5), LU-IG3 | affiche, carrousels carré et 4:5, story sondage |
| Mardi | MA-FB1, MA-FB3, MA-IG1 (6), MA-IG3 | citation, post image, carrousel, story question |
| Mercredi | ME-FB1, ME-FB3 (4), ME-IG3 (3) | affiche, carrousel, stories |
| Jeudi | JE-FB1 (5), JE-FB2, JE-FB3, JE-IG2 (6), JE-IG3 | carrousels, affiche, post FAQ, story lien |
| Vendredi | VE-IG2-MODELE | modèle d'affiche citation à compléter |
| Samedi | SA-FB1, SA-FB3, SA-IG1 (5), SA-IG3 | post image, affiche, carrousel, story question |
| Dimanche | DI-FB1, DI-FB2 (5), DI-FB3, DI-IG1 (5), DI-IG3 (2) | couverture du guide, carrousels, récap, stories |

## Non produites

- **Vidéos** (Reels, TikTok, face caméra, sketchs, témoignages) : à tourner.
- **ME-IG2 « 1 h ou gratuit »** : garantie retirée (décision du 20/11).
- **VE-FB2 Oremo, VE-FB3 album, VE-IG3 stories** : il faut l'accord écrit du marchand et de vraies photos de livraisons.

## Adaptations par rapport au planning

- Nom **FS Express** partout, numéro **687 53 53 73**.
- Garantie « 1 h ou gratuit » retirée de LU-FB3, ME-IG3, JE-FB1, JE-IG2 et SA-FB3. ME-IG3 et JE-IG2 la remplacent par « un appel de validation avant chaque course » et « un interlocuteur dédié ».
- Les phrases d'appui courtes (sous-titres des carrousels, citations des émotions de MA-IG1) ont été écrites pour les créas. Relisez-les.

## À valider avant publication

- **Photos** : licence et source des trois photos à confirmer. Le filigrane « PhotoRoom » reste visible sur le sac du livreur souriant.
- **ME-FB3-2** : liste des zones de Yaoundé à compléter. La carte est une illustration, pas un plan réel.
- **MA-FB3** : les montants du carnet sont fictifs (illustration).
- **JE-FB3** : la conversation est un exemple, signalé sur l'image.
- **JE-FB2** : détail « dépôt par Orange Money » à vérifier avec l'équipe opérations.
- **DI-FB1, DI-FB2, DI-IG1** : le guide « 5 erreurs » doit être prêt avant dimanche.
- **VE-IG2-MODELE** : citation, nom, activité et photo du commerçant à remplacer, avec son accord.
