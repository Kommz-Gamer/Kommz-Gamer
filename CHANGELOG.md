# CHANGELOG

[Français](CHANGELOG.md) | [English](CHANGELOG.en.md)

## Kommz Gamer 5.3 - 2026-08-05

### Bugfix de stabilisation
- Phase 1 — Audit des symboles manquants dans les blueprints (`modules/listen`, `modules/guide`, `modules/remote`, `modules/scenes`) : zéro symbole manquant confirmé dans `vtp_core.py`.
- Phase 2 — Suppression du doublon `_listen_now_utc_iso` (`listen_bp.py`) ; propagation correcte de `_mobile_connected` vers `vtp_core` (au lieu d'une écriture locale via `globals()`).
- Phase 3 — Audit des contrôles de licence : architecture déjà centralisée dans `modules/license/license.py`, aucune refonte nécessaire.
- Phase 4 — Migration des identifiants de périphériques audio (`game_input_device` / `game_output_device`) d'un index PortAudio brut vers une signature canonique stable `"{hostapi}::{nom}"` (ex : `WASAPI::CABLE OUTPUT`), avec cache runtime séparé et rétrocompatibilité assurée pour les configurations existantes.

## Kommz Gamer 4.6 - 2026-03-22

### Audio et stabilité
- Correction de la sélection du microphone pour prioriser le périphérique d'entrée configuré (`game_input_device`) au lieu de forcer aveuglément le périphérique Windows par défaut.
- Amélioration de la résolution du périphérique d'entrée avec une logique de repli propre (config -> défaut système -> détection sûre).
- Stabilisation de l'Activation Hybrid pour réutiliser un contexte micro valide et cohérent.

### Modules et interface
- Ajout de l'onglet `Scenes Vocales` pour sauvegarder/appliquer des presets complets (langue, moteur, modules, voix) en un clic.
- Ajout de l'auto-application par processus actif (par exemple `cod.exe`).
- Unification des 16 modules dans une seule grille compacte dans l'onglet Modules.
- L'Activation Hybrid apparaît maintenant dans la même zone runtime que les autres modules.
- Ajout de l'onglet `Voix Studio` pour sauvegarder, activer, tester et supprimer des profils `voice_id`.
- Ajout du mode `voix par défaut au démarrage`.

### Nettoyage UX
- Nettoyage des messages visibles du moteur audio (erreurs micro/log) et suppression des chaînes malformées.

## Kommz Gamer 4.5 - 2026-03-19

### Interface et lisibilité
- Ajout d'une carte de pipeline vocal avec états séparés pour transcription, Hybrid et synthèse finale.
- Ajout d'une carte de supervision des modules runtime pour les modules clés.
- Refonte de la carte de mise à jour pour une version cible, un statut d'installation et des notes de version plus clairs.
- Nettoyage supplémentaire pour l'interface visible et les chaînes du guide intégré.

### Runtime et diagnostics
- Exposition de plus de détails runtime sur `/status` pour le moteur STT, le routage Hybrid et le moteur TTS actif.
- Amélioration du rapport d'état des modules backend (warmups, boosts, caches, export OBS).
- Nettoyage des messages du système de mise à jour pour éviter les sorties illisibles/malformées.

### Versioning
- Client et guides intégrés mis à jour vers `4.5`.
- Outillage de release maintenu compatible.

## Kommz Gamer 4.4 - 2026-03-18

### Changements majeurs
- Renforcement significatif du mode Hybrid `GPT-SoVITS -> XTTS`.
- Meilleure fidélité de timbre et sortie vocale plus naturelle en usage réel.
- Extension du support linguistique Hybrid (`FR`, `EN`, `JA`, `KO`, `ZH`).
- Consolidation du pipeline distant avec `Whisper Modal`, `GPT-SoVITS Modal` et `XTTS Modal`.

### Corrections et stabilité
- Amélioration du comportement de repli quand les services sont indisponibles.
- Amélioration du routage entre `voice_id`, clonage direct et pipeline Hybrid.
- Correction de plusieurs problèmes d'encodage/affichage.
- Amélioration de la stabilité globale du pipeline temps réel.
