# CHANGELOG

## Kommz Gamer 4.6 - 2026-03-22

### Audio et stabilite
- Correction de la selection micro pour respecter en priorite le device configure (game_input_device) au lieu d'ecraser par defaut Windows.
- Renforcement des resolutions de peripheriques d'entree avec fallback propre (config -> defaut systeme -> detection securisee).
- Stabilisation du mode Hybrid Activation pour reutiliser un micro valide et coherent avec la configuration en cours.

### Modules et interface
- Nouvel onglet `Scènes Vocales` pour sauvegarder/appliquer des presets complets (langue, moteur, modules, voix) en un clic.
- Mode auto-apply par process actif (ex: `cod.exe`) pour charger automatiquement la scène adaptée.
- Fusion visuelle complete des 16 modules dans une seule grille compacte dans l'onglet Modules.
- Hybrid Activation est maintenant integre dans la meme vue runtime que les autres modules (plus de separation en deux blocs).
- Nouvel onglet `Voix Studio` pour enregistrer, activer, tester et supprimer des profils vocaux (`voice_id`) directement depuis l'interface.
- Ajout d'un mode `voix par defaut au demarrage` pour reappliquer automatiquement le profil vocal actif a l'ouverture du logiciel.

### Nettoyage UX
- Nettoyage de plusieurs messages visibles cote moteur audio (logs micro/erreurs) pour supprimer les textes mal encodes et ameliorer la lisibilite.
## Kommz Gamer 4.5 - 2026-03-19

### Interface et lisibilite
- Nouvelle carte de suivi du pipeline vocal avec retour distinct pour la transcription, le mode Hybrid et la synthese finale.
- Nouvelle carte de supervision des modules runtime pour visualiser l'etat reel de `Team-Sync AI`, `Shadow AI`, `Profil e-sport`, `Polyglot Stream` et `Stream Connect`.
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

### Nouveautés majeures
- Renforcement important du mode Hybrid `GPT-SoVITS -> XTTS`.
- Meilleure fidélité du timbre et rendu vocal plus naturel en usage réel.
- Support Hybrid étendu sur plusieurs langues cibles : `FR`, `EN`, `JA`, `KO`, `ZH`.
- Intégration d’un pipeline distant plus cohérent avec `Whisper Modal`, `GPT-SoVITS Modal` et `XTTS Modal`.

### Infrastructure IA
- `Whisper Modal` utilisé en priorité pour la transcription.
- `GPT-SoVITS Modal` intégré au mode Hybrid pour limiter la dépendance au local.
- `XTTS Modal` consolidé pour la synthèse finale.
- Amélioration des fallbacks automatiques en cas d’indisponibilité d’un service.
- Meilleure gestion des références audio GPT-SoVITS côté serveur.

### Interface
- Interface Hybrid simplifiée et moins encombrante.
- Meilleure lisibilité des réglages avancés.
- Amélioration de la cohérence entre les réglages XTTS et le mode Hybrid.
- Correction de la persistance du preset XTTS dans l’interface.

### Moteur et logique
- Amélioration du routage entre `voice_id`, clone direct et pipeline Hybrid.
- Meilleure gestion des langues non supportées côté XTTS.
- Amélioration du comportement en temps réel sur les flux PTT.
- Auto Whisper amélioré pour le remplissage des champs Hybrid.

### Modules
- `Team-Sync AI` désormais branché côté runtime.
- `Shadow AI` désormais branché côté runtime.
- `Profil e-sport` désormais branché côté runtime.
- `Polyglot` désormais branché côté runtime.

### Mise à jour logicielle
- Système de mise à jour amélioré.
- Meilleur affichage des nouveautés et du changelog.
- Comportement de détection de version et d’ouverture des notes de version retravaillé.

### Sécurité
- Durcissement de l’authentification backend et meilleure gestion des secrets côté serveur.
- Migration progressive du stockage des mots de passe vers `bcrypt`.
- Stockage des références audio privé par défaut avec une base plus saine pour les URLs signées.
- Renforcement des cookies de session et nettoyage de certains endpoints sensibles côté administration.

### Corrections
- Correction de plusieurs problèmes d’encodage et d’affichage de caractères.
- Correction de plusieurs comportements incohérents du mode Hybrid.
- Correction de problèmes de fallback sur certains cas multilingues.
- Amélioration de la robustesse globale du pipeline temps réel.
- Stabilisation générale du logiciel sur les scénarios de test récents.





