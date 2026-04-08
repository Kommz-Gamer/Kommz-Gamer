import { useState } from "react";

export default function TestCosy2Button() {
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");

  async function handleTest() {
    setBusy(true);
    setMsg("");
    try {
      const r = await fetch(
        ("/tts/say?text=Hello%20from%20Cosy2&provider=cosy2")
      );
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      setMsg("✅ Requête envoyée. Vérifie la sortie audio / outputs/");
    } catch (e: any) {
      setMsg("❌ " + (e?.message ?? "Erreur"));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex items-center gap-3">
      <button
        onClick={handleTest}
        disabled={busy}
        className="px-3 py-2 rounded-2xl shadow text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
        title="Envoie un TTS vers CosyVoice2 via le Sidecar"
      >
        {busy ? "Test en cours..." : "Test Cosy2"}
      </button>
      {msg && <span className="text-sm">{msg}</span>}
    </div>
  );
}
