# Kommz Gamer — Roadmap

> Dernière mise à jour : V5.2

---

## V5.2 — STABILISATION & ONBOARDING (courant)

### Déjà fait
- [x] 5 nouveaux presets jeux (Tarkov, Rust, PUBG, LoL, Dota 2)
- [x] Séparation voix/bruit par jeu — 5 profils de bruit (combat_mixed, survival, br_large, moba, stable)
- [x] 3 nouveaux presets expressifs (Agressif, Cinématique, Streamer)
- [x] Onboarding testeurs — détection auto du jeu + copy one-click Discord/GitHub
- [x] Flux support centralisé (Discord, GitHub, Patreon dans UI + endpoint)
- [x] Watchdog longue session V5.2 (100s idle / 30s stale)

### Reste à faire
- [ ] Tuning terrain réel — feedback testeurs sur les 5 nouveaux presets
- [ ] Calibration auto noise profile (détecter le jeu → appliquer le bon profil automatiquement)
- [ ] Ajustements expressivité selon retours terrain
- [ ] Tests de stabilité longue session (>4h) sur chaque preset
- [ ] Packaging Community build V5.2 final

---

## V5.3 — INTELLIGENCE AUDIO

### Objectif : rendre l'audio adaptatif sans config manuelle

- [ ] Auto-preset game detection v2 — plus robuste, basé fingerprint audio + process
- [ ] Noise profile auto-switching — changement dynamique si le bruit change en cours de session
- [ ] Voice Focus v3 — mode "adaptive" qui apprend du bruit ambiant sur les 30 premières secondes
- [ ] Anti-bruit par bande de fréquence — séparation plus fine voix/bruit (low/mid/high)
- [ ] Compression dynamique audio — normalisation du volume voix selon distance micro
- [ ] Preset "universel" one-click — un seul bouton qui s'adapte à tout
- [ ] UI : indicateurs temps réel (noise RMS, voice SNR, focus actif) dans l'overlay
- [ ] Export logs session format JSON structuré pour analyse

---

## V5.4 — SOCIAL & STREAMING

### Objectif : outils pour créateurs de contenu et équipes

- [ ] Mode Streamer avancé — overlay OBS natif (transcription + traduction en overlay)
- [ ] Multi-langue simultaneous — traduire vers 2+ langues en parallèle
- [ ] Voice profiles par joueur — reconnaissance du qui parle dans l'équipe
- [ ] TTS personnalisé par jeu — voix thématiques (pirate, militaire, fantasy...)
- [ ] Clips audio — sauvegarde des 30 dernières secondes en one-click
- [ ] Soundboard intégrée — sons custom mappés sur hotkeys
- [ ] Discord rich presence — affiche le preset actif, la langue, etc.
- [ ] Intégration Twitch — commandes chat pour changer preset/traduction
- [ ] Mode équipe — sync presets entre joueurs (leader définit, squad suit)
- [ ] Boutique voix communautaire — téléchargement de voix créées par la commu

---

## V5.5 — PLATEFORME & ÉCOSYSTÈME

### Objectif : Kommz Gamer comme plateforme, pas juste un outil

- [ ] Plugin marketplace — SDK pour développeurs (nouveaux presets, voix, jeux)
- [ ] API publique REST stable — pour intégrations tierces
- [ ] Mobile companion app — contrôle presets/monitoring depuis le téléphone
- [ ] Cloud sync presets — sauvegarde/restore config entre PCs
- [ ] Analytics anonymisées — stats d'usage pour améliorer les presets
- [ ] Auto-updater — mises à jour silencieuses en background
- [ ] Mode tournoi — preset verrouillé, logs horodatés pour fair-play
- [ ] Intégration jeu directe — SDK jeu pour que les devs intègrent Kommz nativement
- [ ] Traduction contextuelle par jeu — glossaires spécifiques (callouts Apex, items Tarkov...)
- [ ] Abonnement Premium — voices exclusives, presets pro, support prioritaire
- [ ] Site web kommzgamer.com — landing, docs, marketplace, comptes

---

## Vision Long Terme (V6+)

- IA vocale locale (whisper.cpp / llama.cpp) — zéro cloud, 100% offline
- Voice cloning par joueur — ta voix traduite dans ta propre voix
- Réduction bruit IA deep learning — modèle entraîné sur bruits de jeu
- Traduction temps réel sans latency perceptible (<200ms)
- Intégration console (PS5/Xbox) via capture card audio
- Communauté open-source active avec contributeurs réguliers
