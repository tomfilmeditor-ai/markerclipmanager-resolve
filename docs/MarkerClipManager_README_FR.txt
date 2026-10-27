MarkerClipManager — Gestionnaire de Marqueurs de Timeline et de Clips pour DaVinci Resolve
==========================================================================================
Author: Tommaso Feraboli — Film Editor
Version: 1.4.7
MIT License — see the script header

CE QU'IL FAIT
-------------
Une seule fenêtre pour afficher et gérer tous les marqueurs d'une timeline Resolve : à la fois
les marqueurs de règle (niveau timeline) et les marqueurs placés sur les clips individuels, sur
toutes les pistes vidéo et audio.

Pour chaque marqueur, il affiche : graphique du marqueur (même forme native que Resolve),
piste, TC début, TC fin, durée, couleur, nom, mot-clé, note.

FONCTIONNALITÉS
---------------
- Sélectionnez un ou plusieurs marqueurs et changez la couleur, changez de
  piste (y compris vers/depuis la règle "TIMELINE"), supprimez
- Modifiez Nom, Mot-clé et Note directement dans le tableau (double-clic),
  même sur plusieurs marqueurs sélectionnés à la fois
- La touche Suppr fait la même chose que le bouton Supprimer, avec une
  confirmation que vous pouvez désactiver
- Annulez et rétablissez avec Cmd+Z / Ctrl+Z, plus un panneau History :
  double-cliquez sur une étape précédente pour y revenir directement. Cela ne
  couvre que la session en cours et s'efface à la fermeture du script
- Filtrez par couleur, piste, auteur/nom, mot-clé
- Exportez/importez les marqueurs au format CSV
- Cliquez sur une ligne : la tête de lecture saute à ce marqueur
- Interface disponible en 12 langues : elle démarre dans la langue de votre
  système s'il y a correspondance, sinon en anglais, et vous pouvez la changer
  depuis le menu en haut de la fenêtre (effectif au redémarrage du script)

PRÉREQUIS
---------
- DaVinci Resolve 19/20 (macOS)
- Python 3 installé sur le système
- PySide6 (installé automatiquement par le script de configuration ci-dessous — aucune
  étape manuelle nécessaire)

INSTALLATION (une seule fois)
-----------------------------
1. Téléchargez l'installeur correspondant à votre système
2. macOS : CLIC DROIT sur le fichier .command puis "Ouvrir" — pas un
   double-clic, que macOS bloque car le fichier n'est pas signé avec un
   certificat de développeur Apple
   Windows : double-cliquez sur le fichier .cmd ; si SmartScreen vous avertit,
   choisissez "Informations complémentaires" puis "Exécuter quand même"
3. L'installeur copie les fichiers puis prépare l'environnement Python dont le
   script a besoin (cette partie nécessite une connexion internet et prend
   environ une minute)
4. Si cette seconde partie échoue — pas de connexion, ou Python absent — les
   fichiers restent correctement installés : ouvrez le dossier installé et
   lancez "MarkerClipManager_Setup.command" (macOS) ou
   "MarkerClipManager_Setup_Windows.cmd" (Windows) quand vous le pourrez
5. Terminé. Les mises à jour s'installent de la même façon, par-dessus la
   version précédente, et vos réglages ne sont pas touchés

UTILISATION
-----------
Dans DaVinci Resolve : Workspace > Scripts > Comp > MarkerClipManager > MarkerClipManager
(le script réside dans le sous-dossier "MarkerClipManager" à l'intérieur de Comp, il s'affiche donc
dans le menu sous forme de sous-menu avec le même nom)

LIMITATIONS CONNUES
-------------------
- Le marqueur dans le tableau est une icône recréée par le script, pas l'icône
  officielle de Resolve (non exposée par l'API). Les couleurs sont les valeurs
  hexadécimales exactes fournies par l'utilisateur — seule la forme de l'icône
  reste une approximation
- "Mot-clé" n'est pas un champ marqueur natif de Resolve : il est stocké dans
  un champ marqueur interne (customData), invisible au panneau Marqueur natif
  de Resolve — lisible/inscriptible uniquement par ce script
- Le code temporel lit le fps et le mode Drop Frame/Non-Drop Frame directement
  à partir de la timeline active du projet (29.97 et 59.94 DF gérés correctement
  avec l'algorithme SMPTE standard) ; sur fps non-standard, les calculs restent
  approximatifs
- L'import/export EDL n'est pas géré par ce script : utilisez la fonctionnalité
  native de Resolve (Timeline > Markers > Export/Import)
- Déplacer un marqueur vers une piste vidéo/audio nécessite qu'un clip existe
  déjà à cette position

SUPPORT
-------
Signalement de bugs : utilisez le bouton 🐛 dans l'app (ouvre un email pré-rempli vers
tomfilmeditor.tools@gmail.com)
Si vous souhaitez soutenir le développement : bouton ☕ dans l'app, ou
https://paypal.me/acoffeefortom

⚠️  Note on translations: This documentation is available in multiple languages.
These translations were generated automatically. If you find any errors or typos,
please report them to the contact listed in the SUPPORT section above.
