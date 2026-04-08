
Valorant Translator Pro — Patch PTT → MT → TTS → Overlay
=======================================================

Contenu
-------
1) index.html                 → index avec branchement onPTTFinalText(txt) dans r.onend.
2) vtp_sidecar_ptt.py         → Sidecar avec routes /ptt/text, /ptt/config, /ptt/hold_down, /ptt/release, /tts/say.
3) windows_curl_examples.txt  → Exemples PowerShell/CMD pour tester les routes.
4) QUICK_TEST.md              → Procédure de smoke test.

Installation rapide
-------------------
1. Fermer/arrêter le Sidecar si déjà lancé.
2. Sauvegarder vos fichiers actuels (copie de sécurité).
3. Remplacer:
   - dist/ValorantTranslatorPro/index.html    ← index.html (fourni ici branché)
   - vtp_sidecar_ptt.py                       ← vtp_sidecar_ptt.py (fourni ici patché)
4. Relancer le Sidecar (pour charger les nouvelles routes).
5. Ouvrir OBS + source navigateur → http://127.0.0.1:8781/overlay?theme=dark&align=bottom&size=xl&max=3

Tests rapides
-------------
- TTS direct: http://127.0.0.1:8781/tts/say?voice=fr-FR-DeniseNeural&text=Bonjour
- Pipeline API (PowerShell):
  $body = @{ text="Hello team"; from="auto"; to="fr"; voice="fr-FR-DeniseNeural" } | ConvertTo-Json
  curl.exe -s -H "Content-Type: application/json" -d $body http://127.0.0.1:8781/ptt/text

FAQ 404
-------
• 404 sur "onPTTFinalText": c'est une **fonction JS**, pas une URL. Il ne faut pas "ouvrir" /onPTTFinalText. 
  Le patch appelle onPTTFinalText(txt) automatiquement à la fin de la dictée (r.onend).
• 404 sur /ptt/text: assurez-vous que le Sidecar a bien redémarré avec le fichier .py patché.
• 404 sur /tts/say: même cause; ouvrir l'URL ci-dessus doit jouer un MP3.
• Si l'app est ouverte en file://, le script utilise automatiquement http://127.0.0.1:8781 comme base.
