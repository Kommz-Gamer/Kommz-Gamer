# CHANGELOG

## Kommz Gamer 5.0 - 2026-04-27

### V5 Community et activation
- Passage explicite du client en V5 (backend + interface + badge version).
- Mode Community force pour les tests locaux avec deblocage du moteur `Kommz Voice (Cloud)`.
- Gate licence ajuste pour eviter les blocages UI quand le mode Community est actif.

### Monitoring ecoute joueurs (V5)
- Ajout d'un watchdog ecoute plus robuste avec relance automatique du flux live en cas de blocage.
- Ajout de metriques watchdog dans `/status` (`watchdog_restarts`, `watchdog_flaps`, `watchdog_cooldown_hits`).
- Nouvelle remontee runtime sur la derniere relance watchdog et son motif.
- UI V5 amelioree: hint connexion ecoute plus clair (`cloud OK`, `reconnexion`, `fallback`) avec stats watchdog visibles.
- Anti-spam ecoute renforce: limite de restitution vocale en rafale avec compteur `ally_voice_rate_limited`.
- Anti-coupures ecoute renforce: fusion des micro-fragments `speech_final` avec compteur `ally_short_merged`.
- Fiabilisation terrain PTT: debounce de touche (`ptt_debounce_ms`) + garde-fou anti double-trigger start/stop.
- Filtre anti-parasites PTT: ignore les captures trop courtes (`ptt_min_record_ms`).
- Reprise ecoute auto apres pause PTT/Hybrid si l'etat restait bloque.
- Presets jeux V5 enrichis: intègrent aussi les paramètres anti-coupure (`short_merge`) et anti-rafale (`rate_limit`).
- Preset pack V5 Pro: variantes `Safe` et `Agressif` pour CS2, Valorant, Warzone et Fortnite.
- Diagnostic fallback V5: compteur + dernier motif fallback TTS exposés côté backend et affichés dans une carte dédiée UI.
- Diagnostic fallback V5 enrichi: endpoint ciblé, statut HTTP et résumé des tentatives Modal visibles dans l'UI pour debug rapide.
- Voice ID V5: fallback explicite `voice_id -> clone` avec cause détaillée (quota essai, URL synthesis manquante, endpoint indisponible) visible dans le diagnostic runtime.
- Diagnostic cloud V5: sonde Whisper / XTTS health / GPT-SoVITS / Voice API avec HTTP + latence et résumé affiché dans le bloc santé moteur.
- UI V5: ajout du bouton `Retest cloud maintenant` pour forcer un refresh immédiat du diagnostic endpoints sans attendre le polling.
- Écoute joueurs V5 (longue session): watchdog renforcé avec relance auto si état `connected/waiting_audio` reste silencieux trop longtemps (`listen_watchdog_idle_threshold_s`, défaut 75s), plus compteurs runtime dédiés.
- Debug V5: ajout d'un indicateur `Santé écoute` (ok/warn/err + résumé) exposé dans `/status` et affiché en compact dans l'UI.
- UI/Backend V5: bouton `Reset santé` + endpoint `/audio/listen/health/reset` pour remettre à zéro uniquement les indicateurs watchdog/santé écoute (sans effacer les stats texte/voix).
- QA V5: export `Rapport session` (JSON) via `/audio/listen/session_report/export` avec snapshot santé écoute, runtime watchdog, fallback TTS, endpoints cloud, latence et quality log.

### Cloud endpoints
- Normalisation des endpoints cloud sur les URLs Modal `kommz-innovations` (XTTS, Whisper, GPT-SoVITS).
- Consolidation des fallbacks moteur pour limiter les erreurs silencieuses en runtime.

### Editions V5
- Ajout d'un profil d'edition via variables d'environnement: `KOMMZ_EDITION_PROFILE=community|private`.
- Ajout du switch cloud via `KOMMZ_CLOUD_FEATURES=0|1`.
- Ajout du fichier de config par edition via `KOMMZ_SETTINGS_FILE` (ex: `settings.community.json`, `settings.private.json`).
- Nouveaux lanceurs:
  `Lancer_Kommz_Gamer_Community.bat` (sans cloud/cles)
  `Lancer_Kommz_Gamer_Private.bat` (avec cloud/licences).

## Kommz Gamer 4.6 - 2026-03-22

### Audio et stabilite
- Correction de la selection micro pour respecter en priorite le device configure (game_input_device) au lieu d'ecraser par defaut Windows.
- Renforcement des resolutions de peripheriques d'entree avec fallback propre (config -> defaut systeme -> detection securisee).
- Stabilisation du mode Hybrid Activation pour reutiliser un micro valide et coherent avec la configuration en cours.

### Modules et interface
- Nouvel onglet `Sc�nes Vocales` pour sauvegarder/appliquer des presets complets (langue, moteur, modules, voix) en un clic.
- Mode auto-apply par process actif (ex: `cod.exe`) pour charger automatiquement la sc�ne adapt�e.
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

### Nouveaut�s majeures
- Renforcement important du mode Hybrid `GPT-SoVITS -> XTTS`.
- Meilleure fid�lit� du timbre et rendu vocal plus naturel en usage r�el.
- Support Hybrid �tendu sur plusieurs langues cibles : `FR`, `EN`, `JA`, `KO`, `ZH`.
- Int�gration d�un pipeline distant plus coh�rent avec `Whisper Modal`, `GPT-SoVITS Modal` et `XTTS Modal`.

### Infrastructure IA
- `Whisper Modal` utilis� en priorit� pour la transcription.
- `GPT-SoVITS Modal` int�gr� au mode Hybrid pour limiter la d�pendance au local.
- `XTTS Modal` consolid� pour la synth�se finale.
- Am�lioration des fallbacks automatiques en cas d�indisponibilit� d�un service.
- Meilleure gestion des r�f�rences audio GPT-SoVITS c�t� serveur.

### Interface
- Interface Hybrid simplifi�e et moins encombrante.
- Meilleure lisibilit� des r�glages avanc�s.
- Am�lioration de la coh�rence entre les r�glages XTTS et le mode Hybrid.
- Correction de la persistance du preset XTTS dans l�interface.

### Moteur et logique
- Am�lioration du routage entre `voice_id`, clone direct et pipeline Hybrid.
- Meilleure gestion des langues non support�es c�t� XTTS.
- Am�lioration du comportement en temps r�el sur les flux PTT.
- Auto Whisper am�lior� pour le remplissage des champs Hybrid.

### Modules
- `Team-Sync AI` d�sormais branch� c�t� runtime.
- `Shadow AI` d�sormais branch� c�t� runtime.
- `Profil e-sport` d�sormais branch� c�t� runtime.
- `Polyglot` d�sormais branch� c�t� runtime.

### Mise � jour logicielle
- Syst�me de mise � jour am�lior�.
- Meilleur affichage des nouveaut�s et du changelog.
- Comportement de d�tection de version et d�ouverture des notes de version retravaill�.

### S�curit�
- Durcissement de l�authentification backend et meilleure gestion des secrets c�t� serveur.
- Migration progressive du stockage des mots de passe vers `bcrypt`.
- Stockage des r�f�rences audio priv� par d�faut avec une base plus saine pour les URLs sign�es.
- Renforcement des cookies de session et nettoyage de certains endpoints sensibles c�t� administration.

### Corrections
- Correction de plusieurs probl�mes d�encodage et d�affichage de caract�res.
- Correction de plusieurs comportements incoh�rents du mode Hybrid.
- Correction de probl�mes de fallback sur certains cas multilingues.
- Am�lioration de la robustesse globale du pipeline temps r�el.
- Stabilisation g�n�rale du logiciel sur les sc�narios de test r�cents.





