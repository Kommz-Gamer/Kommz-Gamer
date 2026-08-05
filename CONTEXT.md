# Contexte projet — Kommz Gamer

Je travaille sur **Kommz Gamer**, un logiciel desktop Windows orienté **gaming, audio temps réel, traduction vocale, STT/TTS, monitoring et outils pour joueurs/streamers**.

- **V5.1 = terminée**
- **V5.2 = terminée**
- **V5.3 = terminée**
- **Version actuelle de travail = V5.4**

Le projet est pensé en plusieurs éditions :
- **Community Edition** : sans dépendance obligatoire à des clés/licences cloud privées
- **Private Edition** : avec services cloud, licence, endpoints privés, etc.

Langue principale de travail : **français**
Style souhaité : **avancer vite, faire du concret, ne pas repartir de zéro, préserver l'existant**

---

# Dossiers / contexte local utile

Projet local principal :
- `C:\Users\nicol\Desktop\KommzGamer`

Repo Community :
- `C:\Users\nicol\Desktop\Kommz-Gamer-Community`

Repo voice lié :
- `C:\Users\nicol\Desktop\kommzVoice`

Fichiers les plus importants :
- `vtp_core.py`
- `web/index.html`
- `version.txt`
- `CHANGELOG.md`
- scripts build `.bat` / install / portable selon la version

---

# État global actuel

- **V5.1** : stabilisation, longue session, watchdog, QA, presets, voice focus auto — ✅ terminé
- **V5.2** : polish, nouveaux presets jeux, UI/UX, overlay desktop, builds, QA avancée — ✅ terminé
- **V5.3** : intelligence audio, refactoring Flask complet, bugfix stabilisation — ✅ terminé
- **V5.4** : social, streaming, multijoueur — 🔄 en cours

---

# Ce qui a déjà été fait

## V5.1 — terminé
- watchdog longue session renforcé
- auto-restart si stream écoute bloqué
- heartbeat audio/runtime
- preset `long_session`, Voice Focus Auto
- presets expressifs V5
- onglet `Bugs & QA` + endpoints QA backend
- builds Community V5.1, versioning global V5.1
- suppression de `third_party/Matcha-TTS`

## V5.2 — terminé
- 5 nouveaux presets jeux (Tarkov, Rust, PUBG, LoL, Dota 2)
- séparation voix/bruit — 5 profils de bruit
- 3 nouveaux presets expressifs
- onboarding testeurs + flux support centralisé
- watchdog V5.2, profils de bruit par map
- export stats session CSV, alertes watchdog configurables
- mode benchmark preset, auto-pause si silence, log rotation
- dark mode OLED, tray icon santé, raccourcis clavier globaux
- mini overlay desktop, toasts natifs, page stats avec graphiques
- installer Windows NSIS + ZIP portable
- auto-update check, runtime Python embarqué, nightly GitHub Actions
- auto-bug report zip, base bugs connus, mode debug verbose
- tests automatiques, feedback in-app

## V5.3 — terminé

### Features audio
- détection auto du jeu via fingerprint audio
- fallback : process → window title → fingerprint → manuel
- base fingerprints locale + sync cloud optionnelle
- mode preset `Auto`, détection multi-jeu / alt-tab
- historique jeux détectés, contribution communautaire fingerprints
- calibration auto voice focus
- réduction bruit par bandes de fréquences
- de-essing / de-clicking / de-clipping
- auto gain riding, VAD amélioré + fallback Silero
- voiceprint léger utilisateur, anti-réverbération pièce
- preset universel intelligent, presets par type de micro
- import/export preset JSON, preset store communautaire, preset schedule
- support ASIO, buffer size auto-tuning, multi-périphérique
- support natif VB-Cable / Voicemeeter, mix micro + son jeu
- overlay temps réel enrichi, dashboard analytics local HTML
- export logs session JSON structuré
- métriques avancées latence / CPU / RAM, alertes intelligentes

### Refactoring Flask / Modularisation — ✅ complet
- 13 blueprints créés : config, license, audio, overlay, tts, stt, listen, privacy, scenes, ui, remote, cloud, subs
- ~81 routes extraites de vtp_core.py (départ ~105)
- vtp_core.py : **24 `@app.route` restantes**
- Nettoyage repo : ~436 fichiers morts, ~3,6 Go libérés

**Routes laissées intentionnellement dans vtp_core.py :**
- `/`, `/favicon.ico`, `/<path:path>` — WEB_DIR
- `/status` — fonction massive, ~30 globals
- `/audio/config`, `/hud/config`, `/hud/move` — _HUD_QT_WINDOW
- `/config/reset`, `/hotkey/start_capture` — keyboard hooks
- `/module/<name>/toggle`, `/hotkey/set`, `/hotkey/bypass/set` — globals runtime
- `/config/target` — DG_ENGINE, CURRENT_TARGET_LANG
- `/config/full`, `/config/kommz`, `/config/kommz/autofill-prompt` — CLOUD_FEATURES_ENABLED
- `/dialog/select-audio-file` — tkinter (intentionnel)
- `/module/hybrid/sensitivity` — _set_module_runtime
- `/audio/expressive/preset/apply` — _apply_expressive_v5_preset
- `/guide/view/<name>`, `/guide/open/<name>` — send_from_directory

### Bugfix stabilisation — ✅ complet
- BUG 1 : Crash lancement — doublon `route_hud_overlay_pos` dans `modules/overlay/overlay.py` supprimé
- BUG 2 : Settings non sauvegardés — 7 clés manquantes ajoutées dans `AUDIO_CONFIG` defaults (`modules/config/config.py`)
- BUG 3 : Activation licence VTP/VCV — endpoint, payload et champ réponse corrigés dans `activate_remote()` (`modules/license/license.py`)
- BUG 4 : Trial expiré accepté — vérification timestamp 24h ajoutée dans `license_status_route()` (`modules/license/license.py`)

---

## État avant V5.4 (bugfix V5.3 terminé)
Tous les prérequis sont verts :
- Blueprints : zéro symbole manquant confirmé
- mobile_connected : propagation correcte vers vtp_core
- Licence : centralisée dans modules/license, aucune refacto nécessaire
- IDs audio : signature canonique {hostapi}::{nom} en place,
  rétrocompatibilité assurée, commits f529d43 / dc72b3d

Prochaine étape : lancer la V5.4

---

# V5.4 — SOCIAL, STREAMING & MULTIJOUEUR — 🔄 EN COURS

## 1. Overlay OBS / Streaming
- [ ] Overlay HTML5 natif pour OBS Studio
- [ ] Widgets customisables
- [ ] Overlay transcription + traduction temps réel
- [ ] Overlay mode équipe
- [ ] Intégration StreamElements / Streamlabs
- [ ] Alertes overlay streaming (don, sub, follow, raid → TTS vocal)
- [ ] Chat overlay inversé (Twitch/YouTube → TTS casque)

## 2. Multilingue avancé
- [ ] Traduction simultanée vers plusieurs langues
- [ ] Détection auto langue source
- [ ] Glossaire custom par jeu
- [ ] Mode interprète bidirectionnel
- [ ] Sous-titres overlay in-game
- [ ] Traduction texte + voix simultanée

## 3. Voice Profiles & équipe
- [ ] Reconnaissance vocale du joueur (voiceprint matching)
- [ ] Profil vocal par contact, icônes/couleurs par joueur
- [ ] Log "qui a dit quoi" exportable
- [ ] Mode Squad Sync
- [ ] Partage de presets entre amis

## 4. TTS & Soundboard
- [ ] TTS thématiques par jeu
- [ ] Soundboard intégrée (sons custom, hotkeys)
- [ ] Banque de sons communautaire
- [ ] TTS personnalisé (pitch, speed, modèle vocal)
- [ ] Voice changer léger temps réel

## 5. Intégrations Discord
- [ ] Rich Presence (jeu détecté, preset actif, langue)
- [ ] Bot slash commands (/stats, /preset, /langue)
- [ ] Webhooks sortants (état session → serveur Discord custom)
- [ ] Twitch/YouTube chat → TTS casque
- [ ] Intégration Stream Deck
- [ ] Ducking Spotify automatique

---

# Ce qui manque avant V5.5

## 1. Mode dégradé cloud
- Stratégie documentée si Deepgram / Supabase tombent
- Fallback fonctionnel, messages UI, retry policy, mode offline partiel

## 2. i18n de l'UI — FR + EN minimum

## 3. RGPD / Privacy
- Politique de confidentialité, consentement, rétention, droit suppression/export

## 4. Vrais tests unitaires
- Pipeline audio, presets, watchdog, fallback cloud/local, exports, routes critiques

---

# Contraintes et attentes importantes

1. Ne pas casser la logique Community / Private
2. Ne pas repartir de zéro — travailler dans la continuité
3. Priorité au concret : modifier le code, brancher les endpoints, mettre à jour l'UI
4. Version active : **V5.4**

---

# État roadmap condensé

## Terminé
- **V5.1** : stabilité / longue session / QA
- **V5.2** : polish / UX / builds / support
- **V5.3** : intelligence audio + refactoring Flask (24 routes, 13 blueprints) + 4 bugs critiques résolus

## En cours
- **V5.4** : social / streaming / multijoueur / intégrations Discord

## À finaliser avant V5.5
- fallback cloud, i18n UI, RGPD, tests unitaires

## Ensuite
- **V5.5** : plateforme / marketplace / API / mobile / cloud / updater / premium
- **V6+** : offline total, IA locale, deep learning audio

---

# Fichiers centraux pour la suite
- `C:\Users\nicol\Desktop\KommzGamer\vtp_core.py`
- `C:\Users\nicol\Desktop\KommzGamer\web\index.html`
- `C:\Users\nicol\Desktop\KommzGamer\CHANGELOG.md`
- `C:\Users\nicol\Desktop\KommzGamer\version.txt`
- `C:\Users\nicol\Desktop\KommzGamer\modules\listen\__init__.py`
- `C:\Users\nicol\Desktop\KommzGamer\modules\listen\listen_bp.py`
- `C:\Users\nicol\Desktop\KommzGamer\modules\audio\__init__.py`
- `C:\Users\nicol\Desktop\KommzGamer\modules\ui\__init__.py`
- `C:\Users\nicol\Desktop\KommzGamer\modules\license\license.py`
- `C:\Users\nicol\Desktop\KommzGamer\modules\scenes\__init__.py`
- `C:\Users\nicol\Desktop\KommzGamer\modules\remote\__init__.py`
- `C:\Users\nicol\Desktop\KommzGamer\modules\cloud\__init__.py`
- `C:\Users\nicol\Desktop\KommzGamer\modules\subs\__init__.py`
- `C:\Users\nicol\Desktop\KommzGamer\modules\overlay\overlay.py`

---

# Résumé ultra court

Projet : **Kommz Gamer**
État : **V5.4 en cours**
Terminé : **V5.1, V5.2, V5.3** (refactoring Flask complet + 4 bugs critiques résolus)
Focus actuel : **streaming, overlay OBS, multilingue, équipe, soundboard, intégrations Discord**
À finaliser avant V5.5 : **fallback cloud, i18n UI, RGPD, tests unitaires**
Contraintes : **préserver Community/Private, continuer l'existant, livrer du concret**

## Bugfix post-refactoring — tous résolus ✅

| Bug | Fichier | Fix |
|-----|---------|-----|
| Crash lancement overlay | modules/overlay/overlay.py | Doublon route_hud_overlay_pos supprimé |
| Settings non sauvegardés | modules/config/config.py | 7 clés manquantes dans AUDIO_CONFIG defaults |
| Activation licence VTP/VCV | modules/license/license.py | Endpoint + payload + champ réponse corrigés |
| Trial expiré accepté | vtp_core.py + license.py | Vérification timestamp 24h |
| Monitoring -9997 | vtp_core.py | rate_in/rate_out séparés + resample soxr VHQ |
| Sous-titres absents | vtp_core.py | Garde overlay_loop étendue à show_own_subs_active |
| Messages SYS non violet | modules/overlay/overlay.py | tk.Label → tk.Text avec tags couleur |
| Device invalide -9996 | vtp_core.py | Skip silencieux avec ℹ️ |
| Grésillements monitoring | vtp_core.py | soxr VHQ + détection sample rate dynamique |
| Création compte KommzVoice | kommzVoice/static/index.html | Validation license_key + hideCtx null check |
| F2/F3 muets | vtp_core.py | Handler F2/F3 corrigé |
