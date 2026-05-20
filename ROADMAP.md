# Kommz Gamer — Roadmap

> Dernière mise à jour : V5.2 · 2026-05-19

---

## V5.1 — STABILISATION & LONGUE SESSION (✅ terminé)

- [x] Watchdog longue session renforcé (idle/stale thresholds configurables)
- [x] Relance auto si stream écoute bloqué (watchdog_stream_stale_restarts)
- [x] Gestion anti faux positifs avec heartbeat audio/runtime
- [x] Preset `long_session` + réglages stables
- [x] Voice Focus mode `auto` : backend choisit balanced ou aggressive selon bruit RMS
- [x] Voice focus auto activé sur presets jeux bruyants (warzone, fortnite, apex, overwatch, r6)
- [x] Presets expressifs V5 : v5_balanced, v5_long_session_stable + endpoint /audio/expressive/preset/apply
- [x] Bouton UI `V5 Long Session`
- [x] Nouvel onglet `Bugs & QA` + tools (Quick Check, Template bug, Pack Debug, Rapport session, Retest cloud, Reset)
- [x] Endpoints QA backend : /quickcheck, /debug_bundle, /session_report/export, /health/reset
- [x] Builds Community V5.1 (nommage versionné, standalone nettoyé, alias Community/Private)
- [x] Versioning global V5.1 (version.txt, vtp_core.py, web/index.html, CHANGELOG.md)
- [x] Nettoyage repo : suppression third_party/Matcha-TTS (non utilisé)

---

## V5.2 — FINALISATION & POLISH (courant)

### Déjà fait
- [x] 5 nouveaux presets jeux (Tarkov, Rust, PUBG, LoL, Dota 2)
- [x] Séparation voix/bruit par jeu — 5 profils de bruit (combat_mixed, survival, br_large, moba, stable)
- [x] 3 nouveaux presets expressifs (Agressif, Cinématique, Streamer)
- [x] Onboarding testeurs — détection auto du jeu + copy one-click Discord/GitHub
- [x] Flux support centralisé (Discord, GitHub, Patreon dans UI + endpoint)
- [x] Watchdog longue session V5.2 (100s idle / 30s stale)

### Terrain & Calibration
- [x] Profil de bruit par map (pas juste par jeu — ex: Tarkov Factory vs Woods vs Interchange)
- [x] Export stats session CSV détaillé : uptime, restarts watchdog, RMS min/max/avg, SNR, words/min, preset actif
- [x] Alertes watchdog configurables : son système, overlay popup, log fichier
- [x] Mode benchmark preset : mesure latence STT/TTS, CPU%, RAM MB, latence totale boucle
- [x] Auto-pause écoute si silence détecté > N secondes (économie ressources)
- [x] Log rotation automatique : taille max configurable, rétention N jours

### UI / UX
- [x] Dark mode OLED pur (#000000 background, contraste réduit)
- [x] Indicateur santé live dans la tray icon Windows (vert/jaune/rouge)
- [x] Raccourcis clavier globaux : toggle listen, push-to-talk, preset+1, preset-1
- [x] Mini overlay desktop always-on-top avec stats temps réel (RMS, SNR, preset, uptime)
- [x] Notifications toast desktop natives : écoute ON/OFF, preset changé, erreur, reconnexion
- [x] Page stats session : graphiques RMS timeline, SNR timeline, watchdog events, heatmap activité
- [x] Toolbar mode compact (icônes seules, pas de texte)

### Builds & Packaging
- [x] Installer Windows (NSIS) avec icône, raccourci bureau, désinstallateur — script build_installer.nsi
- [x] Version ZIP portable (no install, run anywhere) — script build_portable.bat
- [x] Auto-update check au lancement (compare version.txt avec release GitHub) — appel dans main()
- [x] Signature code (EV certificate) documentée — script sign_release.bat + procédure
- [x] Bundled Python runtime embarqué — Nuitka standalone intègre python311.dll et .pyd
- [x] Build nightly automatique via GitHub Actions (lint + build exe + portable zip + release)

### QA & Support
- [x] Auto-bug report generator : screenshot + logs + config + stats en un zip
- [x] Base de données bugs connus + workarounds intégrée dans l'UI
- [x] Mode debug verbose (flag CLI `--debug` ou `--trace`)
- [x] Test suite automatique : smoke test preset, test watchdog, test API endpoints
- [x] Feedback in-app : bouton "Donner mon avis" → Discord/GitHub/Formulaire

---

## V5.3 — INTELLIGENCE AUDIO & AUTO

### Objectif : zero config manuelle, tout s'adapte automatiquement

### Game Detection V2
- [ ] Fingerprint audio : détection auto du jeu en 2-3s via analyse spectrale du flux audio
- [ ] Fallback chaîne : process name → window title → audio fingerprint → prompt manuel
- [ ] Base de données fingerprints locale (JSON/YAML) + cloud sync optionnelle
- [ ] Mode "Auto" dans la liste des presets : détecte tout et applique le bon preset sans clic
- [ ] Détection multi-jeu : si alt-tab vers un autre jeu, détecte et propose de switcher
- [ ] Log historique des jeux détectés (timeline de la session)
- [ ] Contribution communautaire de fingerprints (upload depuis l'app)

### Voice Focus V3
- [ ] Apprentissage adaptatif : 30s d'écoute initiale → calibre auto gain, noise gate, SNR threshold
- [ ] Réduction bruit par bande de fréquence : low (<250Hz), mid (250-4kHz), high (>4kHz)
- [ ] Dé-essing (sifflantes), dé-clicking (clics souris/clavier), dé-clipping (saturation micro)
- [ ] Auto-gain riding : normalisation lissée du volume voix (RMS target constant)
- [ ] Voice Activity Detection v2 : WebRTC VAD amélioré + Silero VAD fallback + seuil adaptatif
- [ ] Profil voix utilisateur (voiceprint léger) pour isolation voix vs autres joueurs
- [ ] Anti-echo room detection : détecte et compense la réverbération de la pièce

### Presets Intelligents
- [ ] Preset "Universel" intelligent : détecte jeu + bruit + micro → applique preset optimal
- [ ] Presets par type de micro : casque gaming, micro bureau, micro cravate, micro studio
- [ ] Import/Export preset JSON (partageable entre utilisateurs)
- [ ] Preset store communautaire intégré dans l'UI (parcourir, télécharger, noter)
- [ ] Preset schedule : changer de preset automatiquement selon l'heure ou le jour

### Audio Pipeline Avancé
- [ ] Support ASIO basse latence (<10ms buffer)
- [ ] Buffer size auto-tuning selon charge CPU et latence mesurée
- [ ] Multi-périphérique : micro et sortie audio séparés (ex: micro USB + speakers jack)
- [ ] Virtual audio cable support natif (VB-Cable, Voicemeeter)
- [ ] Mixage entrée micro + son jeu pour streamers (monitoring mix)

### Monitoring & Analytics
- [ ] Overlay temps réel : noise RMS, voice SNR, focus mode actif, gain appliqué
- [ ] Session analytics dashboard local (HTML interactif avec graphiques)
- [ ] Export logs session format JSON structuré (schema stable)
- [ ] Métriques avancées : latence STT p50/p95/p99, temps traitement TTS, CPU spikes
- [ ] Alertes intelligentes : "ton micro sature", "bruit de fond anormal", "latence élevée"

---

## V5.4 — SOCIAL, STREAMING & MULTIJOUEUR

### Objectif : outils pour créateurs de contenu et équipes

### Overlay OBS / Streaming
- [ ] Overlay HTML5 natif pour OBS Studio (source navigateur)
- [ ] Widgets customisables : couleurs, polices, position, taille, animations CSS
- [ ] Overlay transcription temps réel : ce que le jeu dit → texte en bas d'écran
- [ ] Overlay traduction : langue source → langue cible synchronisée
- [ ] Overlay mode équipe : qui parle + quelle langue + icône drapeau
- [ ] Intégration StreamElements et Streamlabs (widget pack)
- [ ] Alertes overlay pour événements streaming : don, sub, follow, raid → TTS vocal
- [ ] Chat overlay inversé : messages Twitch/YouTube → voix TTS dans le casque

### Multilingue Avancé
- [ ] Traduction simultanée vers N langues en parallèle (output multiple)
- [ ] Détection automatique de la langue source (plus besoin de la spécifier)
- [ ] Glossaire custom par jeu : callouts, slang, noms propres (ex: "dragon pit" → "fosse du dragon")
- [ ] Mode interprète : A parle FR → B entend EN, B parle EN → A entend FR (bidirectionnel)
- [ ] Sous-titres overlay in-game : injection overlay dans le jeu (toujours devant)
- [ ] Traduction texte + voix simultanée : le chat écrit + la voix parle

### Voice Profiles & Équipe
- [ ] Reconnaissance vocale du joueur : qui parle dans l'équipe (voiceprint matching)
- [ ] Profil vocal par contact : tag automatique "Pseudo", icône, couleur associée
- [ ] Icônes + couleurs par joueur visibles dans l'overlay équipe
- [ ] Log "qui a dit quoi" exportable (horodaté, texte, locuteur)
- [ ] Mode Squad Sync : un chef définit le preset → toute l'équipe applique le même
- [ ] Partage de preset entre amis (QR code ou lien)

### TTS & Soundboard
- [ ] TTS thématiques par jeu : pirate (Sea of Thieves), militaire (CoD), fantasy (RPG), robot (sci-fi)
- [ ] Soundboard intégrée : banque de sons custom, mappés sur hotkeys (F1-F12)
- [ ] Banque de sons communautaire (upload/download/notation)
- [ ] TTS personnalisé : pitch, speed, sélection du modèle vocal
- [ ] Voice changer léger intégré : pitch shift, reverb, EQ en temps réel sur le micro

### Intégrations Externes
- [ ] Discord Rich Presence : affiche "Joue à X — Kommz Gamer · Preset Y · Langue Z"
- [ ] Twitch chat → TTS : les messages du chat sont lus en vocal dans le casque
- [ ] Intégration Stream Deck : boutons physiques pour changer preset, langue, toggle
- [ ] Webhooks sortants : POST état vers serveur custom (pour dashboards perso)
- [ ] Intégration Spotify : ducking automatique de la musique quand une voix est détectée
- [ ] Intégration Discord bot : commandes slash pour info stats, changer preset à distance

---

## V5.5 — PLATEFORME & ÉCOSYSTÈME

### Objectif : Kommz Gamer comme plateforme, pas juste un outil

### Plugin Marketplace
- [ ] Marketplace intégrée dans l'UI : parcourir, installer, désinstaller en 1 clic
- [ ] SDK développeur : API Python + JS + documentation
- [ ] Types de plugins : presets jeux, voix TTS, soundboards, overlays, intégrations
- [ ] Sandbox plugins : permissions, sécurité, bac à sable par plugin
- [ ] Système de notation, reviews, signalement de plugins
- [ ] Monétisation : gratuit / freemium / premium avec clé licence
- [ ] Auto-update des plugins installés

### API Publique
- [ ] API REST stable v1 : documentée OpenAPI/Swagger
- [ ] API Keys avec rate limiting et quotas par tier (free/pro/premium)
- [ ] WebSocket API : flux audio temps réel, état, événements, logs
- [ ] Webhooks sortants configurables : état preset, erreurs, stats, démarrage/arrêt
- [ ] SDKs officiels : Python, JavaScript/TypeScript, C#/.NET
- [ ] Bac à sable API : environnement de test sans risque

### Mobile Companion
- [ ] App companion Android (Kotlin/Jetpack Compose)
- [ ] App companion iOS (Swift/SwiftUI)
- [ ] Télécommande desktop : changer preset, voir stats, toggle écoute
- [ ] Push notifications : erreur critique, mise à jour dispo, session longue durée
- [ ] Transfert audio mobile → PC : utiliser le micro du téléphone comme source sur PC
- [ ] Widget homescreen : état Kommz, preset actif, toggle rapide

### Cloud & Sync
- [ ] Compte Kommz : inscription, connexion, gestion profil
- [ ] Sync presets cloud : sauvegarde et restauration entre PC
- [ ] Sync config cloud : retrouver tout son setup sur une nouvelle machine
- [ ] Cloud stats dashboard web : historique sessions, stats, classements
- [ ] Leaderboard communautaire : meilleurs presets, plus de sessions, plus de langues
- [ ] Patreon intégration native : bonus abonnés, features early access

### Auto-Updater
- [ ] Mises à jour silencieuses en background (téléchargement pendant l'utilisation)
- [ ] Delta updates : patches binaires, pas de re-téléchargement complet
- [ ] Rollback automatique si crash après mise à jour
- [ ] Canaux : stable, beta, nightly (choisissable dans les settings)
- [ ] Release notes intégrées dans l'app au moment de l'update
- [ ] Vérification signature avant installation (sécurité)

### Premium & Monétisation
- [ ] Abonnement Premium : fonctionnalités exclusives
- [ ] Voix TTS premium : modèles de voix plus naturels
- [ ] Traduction avancée : DeepL / OpenAI / modèles pro
- [ ] Support prioritaire : tickets, chat, réponse <24h
- [ ] Badge premium visible dans l'app + overlay stream
- [ ] Essai gratuit 7 jours

### Mode Tournoi / Esport
- [ ] Mode tournoi : preset verrouillé (pas de changement possible)
- [ ] Logs horodatés et certifiés (hash chaîné) pour vérification fair-play
- [ ] Export preuves : rapport signé pour organisations esport
- [ ] Mode caster : 1 voix broadcast vers N spectateurs (commentateur → audience)
- [ ] Intégration plateformes tournoi : Faceit, ESL, Toornament

### Traduction Contextuelle
- [ ] Glossaire callouts par jeu : mappings spécifiques (Apex, Tarkov, LoL, Valorant...)
- [ ] Apprentissage des termes utilisés par l'équipe (récurrents)
- [ ] Mode "traduction tactique" : filtre insultes, garde uniquement les callouts
- [ ] Traduction d'emotes et slang gaming (GG, GLHF, NT, WP...)
- [ ] Dictionnaires communautaires : contribution et vote

### Site Web
- [ ] kommzgamer.com : landing page, features, tarifs, blog
- [ ] Documentation complète : guides, API docs, tutos vidéo
- [ ] Forum communauté : entraide, partage presets, feedback
- [ ] Wiki utilisateur : tout savoir sur Kommz Gamer
- [ ] Intégration webhooks site ↔ app : statut service, annonces

---

## Vision V6+ — IA & INNOVATION

### IA Locale 100% Offline
- [ ] STT local : Whisper.cpp ou Faster-Whisper embarqué (pas de cloud)
- [ ] TTS local : Piper TTS, XTTS v2 ou Coqui TTS embarqué
- [ ] Traduction locale : modèles NLLB ou OPUS-MT en local
- [ ] Tout fonctionne sans connexion internet

### Deep Learning Audio
- [ ] Voice cloning : clone ta voix en 30s d'enregistrement
- [ ] Ta voix traduite dans TA voix (pas une voix robot)
- [ ] Anti-bruit deep learning : modèle entraîné sur TON setup spécifique
- [ ] Séparation de sources audio (demucs) : isoler voix du bruit jeu
- [ ] Amélioration vocale temps réel : upsampling, dé-noising, dé-reverb

### Expansions
- [ ] Intégration console : PS5, Xbox Series via carte d'acquisition audio
- [ ] API GraphQL v2 pour requêtes complexes
- [ ] Mode Coach IA : analyse tes callouts, suggère des améliorations tactiques
- [ ] Intégration hardware : Stream Deck natif, pédales USB, mixeurs audio
- [ ] Traduction temps réel <200ms de latence (imperceptible)

### Communauté & Open Source
- [ ] Code source ouvert (parties clés)
- [ ] Programme contributeurs avec reconnaissance
- [ ] Conférences gaming / IA
- [ ] Partenariats studios de jeu pour intégration native
