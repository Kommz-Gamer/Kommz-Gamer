import TestCosy2Button from "@/components/TestCosy2Button";

export default function TtsControls() {
  // ... tes autres contrôles
  return (
    <div className="space-y-4">
      {/* Sélecteur de voix, Appliquer config, etc. */}
      <div className="flex items-center gap-3">
        {/* autres boutons */}
        <TestCosy2Button />
      </div>
    </div>
  );
}
