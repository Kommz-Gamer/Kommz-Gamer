# Kommz Gamer — Roadmap

> Dernière mise à jour : V5.4 démarrée · 2026-07-05

---

## V5.1 — STABILISATION & LONGUE SESSION (✅ terminé)

- [✅] Watchdog longue session renforcé
- [✅] Relance auto si stream écoute bloqué
- [✅] Heartbeat audio/runtime
- [✅] Preset `long_session`, Voice Focus Auto
- [✅] Presets expressifs V5
- [✅] Onglet `Bugs & QA` + endpoints QA backend
- [✅] Builds Community V5.1 + versioning global
- [✅] Nettoyage repo : suppression third_party/Matcha-TTS

---

## V5.2 — FINALISATION & POLISH (✅ terminé)

- [✅] 5 nouveaux presets jeux (Tarkov, Rust, PUBG, LoL, Dota 2)
- [✅] Séparation voix/bruit — 5 profils de bruit
- [✅] 3 nouveaux presets expressifs (Agressif, Cinématique, Streamer)
- [✅] Onboarding testeurs + flux support centralisé
- [✅] Watchdog V5.2, profils de bruit par map
- [✅] Export stats session CSV, alertes watchdog configurables
- [✅] Mode benchmark preset, auto-pause si silence, log rotation
- [✅] Dark mode OLED, tray icon santé, raccourcis clavier globaux
- [✅] Mini overlay desktop, toasts natifs, page stats avec graphiques
- [✅] Installer Windows NSIS + ZIP portable
- [✅] Auto-update check, runtime Python embarqué, nightly GitHub Actions
- [✅] Auto-bug report zip, base bugs connus, mode debug verbose
- [✅] Tests automatiques, feedback in-app

---

## V5.3 — INTELLIGENCE AUDIO & REFACTORING (✅ terminé)

### Game Detection V2
- [✅] Fingerprint audio : détection auto du jeu en 2-3s
- [✅] Fallback chaîne : process → window title → fingerprint → manuel
- [✅] Base fingerprints locale + cloud sync optionnelle
- [✅] Mode preset `Auto`, détection multi-jeu / alt-tab
- [✅] Historique jeux détectés, contribution communautaire fingerprints

### Voice Focus V3
- [✅] Calibration auto (30s écoute initiale)
- [✅] Réduction bruit par bande de fréquence
- [✅] Dé-essing, dé-clicking, dé-clipping
- [✅] Auto-gain riding, VAD v2 + Silero fallback
- [✅] Voiceprint léger utilisateur, anti-réverbération pièce

### Presets Intelligents
- [✅] Preset "Universel" intelligent
- [✅] Presets par type de micro
- [✅] Import/Export preset JSON
- [✅] Preset store communautaire
- [✅] Preset schedule

### Audio Pipeline Avancé
- [✅] Support ASIO basse latence
- [✅] Buffer size auto-tuning
- [✅] Multi-périphérique, VB-Cable / Voicemeeter natif
- [✅] Mix micro + son jeu

### Monitoring & Analytics
- [✅] Overlay temps réel enrichi
- [✅] Dashboard analytics local HTML
- [✅] Export logs session JSON structuré
- [✅] Métriques avancées latence / CPU / RAM
- [✅] Alertes intelligentes

### Refactoring Flask / Modularisation
- [✅] 13 blueprints créés : config, license, audio, overlay, tts, stt, listen, privacy, scenes, ui, remote, cloud, subs
- [✅] ~81 routes extraites de vtp_core.py
- [✅] vtp_core.py : **24 `@app.route` restantes** (départ : ~105)
- [✅] python -m py_compile vtp_core.py → exit code 0
- [✅] Nettoyage repo : ~436 fichiers morts, ~3,6 Go libérés
- [✅] module license.py : code mort Supabase supprimé
- [✅] listen.py (doublon) supprimé

### Bugs résolus
- [✅] Config non sauvegardée (réassignation AUDIO_CONFIG)
- [✅] load_settings() : filtre destructeur supprimé (92 params perdus)
- [✅] Licence non persistante au démarrage (sync_license_mgr_from_config)
- [✅] Monitoring casque : dtype mismatch float64/float32
- [✅] HUD flottant figé : timeout poll 0.8s → 2s
- [✅] Overlay sous-titres expérimental retiré proprement

### Bugfix stabilisation post-refactoring — ✅ complet
- [✅] BUG 1 — Crash lancement : doublon route_hud_overlay_pos supprimé
- [✅] BUG 2 — Settings : 7 clés manquantes ajoutées dans AUDIO_CONFIG defaults
- [✅] BUG 3 — Licence VTP/VCV : endpoint + payload + champ réponse corrigés
- [✅] BUG 4 — Trial expiré accepté : vérification timestamp 24h ajoutée
- [✅] BUG 5 — Monitoring -9997 : rate_in/rate_out séparés + soxr VHQ
- [✅] BUG 6 — Sous-titres absents : garde overlay_loop étendue
- [✅] BUG 7 — Messages SYS non violet : tk.Text avec tags couleur
- [✅] BUG 8 — Device invalide -9996 : skip silencieux
- [✅] BUG 9 — Grésillements monitoring : détection sample rate dynamique
- [✅] BUG 10 — Création compte KommzVoice : validation license_key
- [✅] BUG 11 — F2/F3 muets : handlers corrigés

### Bugfix stabilisation V5.3
- [x] Phase 1 : Audit symboles manquants dans les blueprints → RAS
- [x] Phase 2A : Doublon _listen_now_utc_iso supprimé (listen_bp.py)
- [x] Phase 2B : _mobile_connected propagé correctement vers vtp_core
- [x] Phase 3 : Audit contrôles de licence → architecture saine, RAS
- [x] Phase 4 : IDs audio canoniques (WASAPI::NOM) — commits f529d43 / dc72b3d

---

## V5.4 — SOCIAL, STREAMING & MULTIJOUEUR (🔄 en cours)

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
- [ ] Profil vocal par contact, icônes/couleurs par joueur
- [ ] Log "qui a dit quoi" exportable
- [ ] Mode Squad Sync
- [ ] Partage de preset entre amis

### TTS & Soundboard
- [ ] TTS thématiques par jeu
- [ ] Soundboard intégrée (sons custom, hotkeys F1-F12)
- [ ] Banque de sons communautaire
- [ ] TTS personnalisé (pitch, speed, modèle vocal)
- [ ] Voice changer léger temps réel

### Intégrations Discord
- [ ] Rich Presence (jeu détecté, preset actif, langue)
- [ ] Bot slash commands (/stats, /preset, /langue)
- [ ] Webhooks sortants (état session → serveur Discord custom)
- [ ] Twitch/YouTube chat → TTS casque
- [ ] Intégration Stream Deck
- [ ] Ducking Spotify automatique

---

## V5.5 — PLATEFORME & ÉCOSYSTÈME

- [ ] Plugin Marketplace intégrée (parcourir, installer, désinstaller)
- [ ] SDK développeur (API Python + JS + doc)
- [ ] Sandbox plugins (permissions, sécurité)
- [ ] API REST stable v1 (OpenAPI/Swagger)
- [ ] WebSocket API (flux audio, état, événements)
- [ ] SDKs officiels : Python, JS/TS, C#/.NET
- [ ] App companion Android + iOS
- [ ] Compte Kommz (inscription, connexion, profil)
- [ ] Sync presets + config cloud
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
- [ ] Traduction temps réel <200ms
- [ ] Parties clés open source + programme contributeurs
