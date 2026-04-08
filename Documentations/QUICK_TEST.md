1) Vérifier Sidecar:
   http://127.0.0.1:8781/status

2) Vérifier TTS:
   http://127.0.0.1:8781/tts/say?voice=fr-FR-DeniseNeural&text=Bonjour

3) Vérifier pipeline API:
   PowerShell:
   $body = @{ text="Hello team"; from="auto"; to="fr"; voice="fr-FR-DeniseNeural" } | ConvertTo-Json
   curl.exe -s -H "Content-Type: application/json" -d $body http://127.0.0.1:8781/ptt/text

4) Vérifier overlay dans OBS (source navigateur):
   http://127.0.0.1:8781/overlay?theme=dark&align=bottom&size=xl&max=3

5) Test UI:
   Ouvrir la page, maintenir PTT, parler, relâcher → la traduction apparaît dans l’overlay et la voix joue.
