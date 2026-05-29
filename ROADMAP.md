# Kommz Gamer — Roadmap

> Dernière mise à jour : V5.3 · 2026-05-29

---

## V5.1 — STABILISATION & LONGUE SESSION (✅ terminé)

- [✅] Watchdog longue session renforcé (idle/stale thresholds configurables)
- [✅] Relance auto si stream écoute bloqué
- [✅] Heartbeat audio/runtime
- [✅] Preset `long_session`
- [✅] Voice Focus mode `auto`
- [✅] Voice focus auto sur presets jeux bruyants
- [✅] Presets expressifs V5
- [✅] Bouton UI `V5 Long Session`
- [✅] Onglet `Bugs & QA` + endpoints QA backend
- [✅] Builds Community V5.1
- [✅] Versioning global V5.1
- [✅] Nettoyage repo : suppression third_party/Matcha-TTS

---

## V5.2 — FINALISATION & POLISH (✅ terminé)

- [✅] 5 nouveaux presets jeux (Tarkov, Rust, PUBG, LoL, Dota 2)
- [✅] Séparation voix/bruit par jeu — 5 profils de bruit
- [✅] 3 nouveaux presets expressifs (Agressif, Cinématique, Streamer)
- [✅] Onboarding testeurs amélioré
- [✅] Flux support centralisé (Discord, GitHub, Patreon)
- [✅] Watchdog longue session V5.2
- [✅] Profil de bruit par map
- [✅] Export stats session CSV détaillé
- [✅] Alertes watchdog configurables
- [✅] Mode benchmark preset
- [✅] Auto-pause si silence
- [✅] Log rotation automatique
- [✅] Dark mode OLED
- [✅] Indicateur santé dans la tray icon
- [✅] Raccourcis clavier globaux
- [✅] Mini overlay desktop always-on-top
- [✅] Notifications toast desktop natives
- [✅] Page stats session avec graphiques
- [✅] Toolbar mode compact
- [✅] Installer Windows (NSIS)
- [✅] Version ZIP portable
- [✅] Auto-update check au lancement
- [✅] Signature code documentée
- [✅] Bundled Python runtime embarqué
- [✅] Build nightly GitHub Actions
- [✅] Auto-bug report zip
- [✅] Base de données bugs connus intégrée
- [✅] Mode debug verbose
- [✅] Test suite automatique
- [✅] Feedback in-app

---

## V5.3 — INTELLIGENCE AUDIO & AUTO (🔄 en cours — refactoring Flask actif)

### Game Detection V2 (✅ terminé)
- [✅] Fingerprint audio : détection auto du jeu en 2-3s
- [✅] Fallback chaîne : process → window title → fingerprint → manuel
- [✅] Base de données fingerprints locale + cloud sync optionnelle
- [✅] Mode preset `Auto`
- [✅] Détection multi-jeu / alt-tab
- [✅] Log historique des jeux détectés
- [✅] Contribution communautaire de fingerprints

### Voice Focus V3 (✅ terminé)
- [✅] Calibration auto : 30s d'écoute initiale
- [✅] Réduction bruit par bande de fréquence (low/mid/high)
- [✅] Dé-essing, dé-clicking, dé-clipping
- [✅] Auto-gain riding (RMS target constant)
- [✅] VAD v2 : WebRTC + Silero VAD fallback
- [✅] Voiceprint léger utilisateur
- [✅] Anti-réverbération pièce

### Presets Intelligents (✅ terminé)
- [✅] Preset "Universel" intelligent
- [✅] Presets par type de micro
- [✅] Import/Export preset JSON
- [✅] Preset store communautaire
- [✅] Preset schedule

### Audio Pipeline Avancé (✅ terminé)
- [✅] Support ASIO basse latence
- [✅] Buffer size auto-tuning
- [✅] Multi-périphérique
- [✅] Virtual audio cable support natif (VB-Cable, Voicemeeter)
- [✅] Mixage entrée micro + son jeu

### Monitoring & Analytics (✅ terminé)
- [✅] Overlay temps réel enrichi
- [✅] Session analytics dashboard local HTML
- [✅] Export logs session JSON structuré
- [✅] Métriques avancées latence / CPU / RAM
- [✅] Alertes intelligentes

### Nettoyage Repo (✅ terminé)
- [✅] Suppression ~436 fichiers morts
- [✅] ~92 450 fichiers, ~3,6 Go libérés
- [✅] modules/ ne contient plus que les modules actifs
- [✅] Scripts de lancement corrigés

### Refactoring Flask / Modularisation (🔄 EN COURS ACTIF)

**Modules extraits — terminés :**
- [✅] `modules/config/` — config_bp
- [✅] `modules/license/` — license_bp
- [✅] `modules/audio/` — audio_bp
- [✅] `modules/overlay/` — overlay_bp
- [✅] `modules/tts/` — tts_bp
- [✅] `modules/stt/` — stt_bp
- [✅] `modules/listen/` — listen_bp (`__init__.py` + `listen.py`)
- [✅] `modules/privacy/` — privacy_bp
- [✅] `modules/scenes/` — scenes_bp
- [✅] `modules/ui/` — ui_bp ✅ créé vague 3

**Routes extraites — terminées (~37 routes) :**
- [✅] Vague 1 (12 routes) : GET /privacy/list, /audio/monitoring_mix/status, /hud/status, /hud_overlay.html, /license/hwid, /license/status, /scenes/list + listen support/preset/latency
- [✅] Vague 2 (18 routes) : listen game_timeline, game_noise_profile, fingerprint/db/stats, fingerprint/db/export, detect_game, detect_game_v2, smart_alerts, analytics/v3/dashboard, analytics/v3/smart_alerts, auto_bug_report + audio devices/asio, pipeline/multi_device
- [✅] Vague 3 (7 routes) : listen benchmark, session_report/export, quickcheck, debug_bundle + update/changelog, ui/toasts/pending, audio/pipeline/latency

**État actuel :**
- Routes restantes dans vtp_core.py : **86 `@app.route`**
- Import listen_bp dans vtp_core.py : ligne 149
- `python -m py_compile vtp_core.py` → ✅ exit code 0

**Route laissée intentionnellement :**
- `GET /dialog/select-audio-file` — dépend de `tkinter` + effets de bord sur `AUDIO_CONFIG`, non déplaçable sans refonte

**Prochain objectif : passer sous les 80 routes avant de clore V5.3**

---

## V5.4 — SOCIAL, STREAMING & MULTIJOUEUR (⏳ pas encore commencé)

### Overlay OBS / Streaming
- [ ] Overlay HTML5 natif pour OBS Studio
- [ ] Widgets customisables (couleurs, polices, position, animations)
- [ ] Overlay transcription temps réel
- [ ] Overlay traduction
- [ ] Overlay mode équipe
- [ ] Intégration StreamElements / Streamlabs
- [ ] Alertes overlay streaming (don, sub, follow, raid → TTS vocal)
- [ ] Chat overlay inversé (Twitch/YouTube → TTS casque)

### Multilingue Avancé
- [ ] Traduction simultanée vers N langues en parallèle
- [ ] Détection automatique de la langue source
- [ ] Glossaire custom par jeu
- [ ] Mode interprète bidirectionnel
- [ ] Sous-titres overlay in-game
- [ ] Traduction texte + voix simultanée

### Voice Profiles & Équipe
- [ ] Reconnaissance vocale du joueur (voiceprint matching)
- [ ] Profil vocal par contact
- [ ] Icônes + couleurs par joueur dans l'overlay
- [ ] Log "qui a dit quoi" exportable
- [ ] Mode Squad Sync
- [ ] Partage de preset entre amis

### TTS & Soundboard
- [ ] TTS thématiques par jeu
- [ ] Soundboard intégrée (sons custom, hotkeys)
- [ ] Banque de sons communautaire
- [ ] TTS personnalisé (pitch, speed, modèle vocal)
- [ ] Voice changer léger temps réel

### Intégrations Externes
- [ ] Discord Rich Presence (jeu détecté, preset actif, langue)
- [ ] Discord bot slash commands (/stats, /preset, /langue)
- [ ] Discord webhooks sortants (état session → serveur custom)
- [ ] Twitch/YouTube chat → TTS casque
- [ ] Intégration Stream Deck
- [ ] Ducking Spotify automatique
- [ ] Discord bot slash commands distants

---

## V5.5 — PLATEFORME & ÉCOSYSTÈME

- [ ] Plugin Marketplace intégrée (parcourir, installer, désinstaller)
- [ ] SDK développeur (API Python + JS + doc)
- [ ] Sandbox plugins (permissions, sécurité)
- [ ] API REST stable v1 (OpenAPI/Swagger)
- [ ] API Keys avec rate limiting
- [ ] WebSocket API (flux audio, état, événements)
- [ ] SDKs officiels : Python, JS/TS, C#/.NET
- [ ] App companion Android + iOS
- [ ] Compte Kommz (inscription, connexion, profil)
- [ ] Sync presets cloud
- [ ] Sync config cloud
- [ ] Cloud stats dashboard web
- [ ] Leaderboard communautaire
- [ ] Patreon intégration native
- [ ] Auto-updater silencieux (delta updates, rollback, canaux stable/beta/nightly)
- [ ] Abonnement Premium (voix TTS pro, traduction avancée, support prioritaire)
- [ ] Mode tournoi / esport (logs certifiés, export preuves)
- [ ] Site web : kommzgamer.com (landing, docs, forum, wiki)

---

## Vision V6+ — IA & INNOVATION

- [ ] STT local 100% offline (Whisper.cpp / Faster-Whisper)
- [ ] TTS local (Piper TTS, XTTS v2)
- [ ] Traduction locale (NLLB / OPUS-MT)
- [ ] Voice cloning (30s d'enregistrement)
- [ ] Ta voix traduite dans TA voix
- [ ] Anti-bruit deep learning sur ton setup
- [ ] Séparation de sources audio (demucs)
- [ ] Intégration console (PS5, Xbox via carte acquisition)
- [ ] Mode Coach IA (analyse callouts, suggestions tactiques)
- [ ] Intégration hardware (Stream Deck natif, pédales, mixeurs)
- [ ] Traduction temps réel <200ms
- [ ] Parties clés open source + programme contributeurs
