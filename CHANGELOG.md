# CHANGELOG

[Français](CHANGELOG.md) | [English](CHANGELOG.en.md)

## Kommz Gamer 4.6 - 2026-03-22

### Audio et stabilite
- Correction de la selection micro pour respecter en priorite le device configure (`game_input_device`) au lieu d'ecraser par defaut Windows.
- Renforcement des resolutions de peripheriques d'entree avec fallback propre (config -> defaut systeme -> detection securisee).
- Stabilisation du mode Hybrid Activation pour reutiliser un micro valide et coherent avec la configuration en cours.

### Modules et interface
- Nouvel onglet `Scenes Vocales` pour sauvegarder/appliquer des presets complets (langue, moteur, modules, voix) en un clic.
- Mode auto-apply par process actif (ex: `cod.exe`) pour charger automatiquement la scene adaptee.
- Fusion visuelle complete des 16 modules dans une seule grille compacte dans l'onglet Modules.
- Hybrid Activation integre dans la meme vue runtime que les autres modules.
- Nouvel onglet `Voix Studio` pour enregistrer, activer, tester et supprimer des profils vocaux (`voice_id`) directement depuis l'interface.
- Ajout d'un mode `voix par defaut au demarrage` pour reappliquer automatiquement le profil vocal actif a l'ouverture du logiciel.

### Nettoyage UX
- Nettoyage de plusieurs messages visibles cote moteur audio (logs micro/erreurs) pour supprimer les textes mal encodes et ameliorer la lisibilite.

## Kommz Gamer 4.5 - 2026-03-19

### Interface et lisibilite
- Nouvelle carte de suivi du pipeline vocal avec retour distinct pour la transcription, le mode Hybrid et la synthese finale.
- Nouvelle carte de supervision des modules runtime pour visualiser l'etat reel des modules principaux.
- Carte de mise a jour logiciel retravaillee pour mieux afficher la version cible, le statut d'installation et les notes de release.
- Nettoyage complementaire de plusieurs textes visibles dans l'interface et les guides embarques.

### Runtime et diagnostic
- Exposition d'un etat runtime plus detaille cote `/status` pour suivre le moteur STT actif, le routage Hybrid et le moteur TTS reellement utilise.
- Meilleure remontee des etats modules cote backend pour refleter les warmups, boosts, caches audio et exports OBS.
- Messages systeme de mise a jour nettoyes pour eviter les statuts illisibles ou mal encodes.

### Versioning
- Passage du client et des guides embarques en `4.5`.
- Outillage de release conserve et compatible avec la nouvelle version.

## Kommz Gamer 4.4 - 2026-03-18

### Nouveautes majeures
- Renforcement important du mode Hybrid `GPT-SoVITS -> XTTS`.
- Meilleure fidelite du timbre et rendu vocal plus naturel en usage reel.
- Support Hybrid etendu sur plusieurs langues cibles (`FR`, `EN`, `JA`, `KO`, `ZH`).
- Integration d'un pipeline distant coherent avec `Whisper Modal`, `GPT-SoVITS Modal` et `XTTS Modal`.

### Corrections et stabilite
- Amelioration des fallbacks automatiques en cas d'indisponibilite d'un service.
- Amelioration du routage entre `voice_id`, clone direct et pipeline Hybrid.
- Correction de plusieurs problemes d'encodage et d'affichage de caracteres.
- Stabilisation globale du pipeline temps reel.
