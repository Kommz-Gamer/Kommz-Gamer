<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <title>Kommz Remote</title>
  <style>
    body { background-color: #0b0f14; color: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
    header { background: #161b22; padding: 15px; text-align: center; border-bottom: 1px solid #30363d; display: flex; align-items: center; justify-content: space-between; }
    h1 { margin: 0; font-size: 18px; color: #2f81f7; font-weight: 700; }
    .status-badge { font-size: 11px; background: #2ea043; color: white; padding: 3px 8px; border-radius: 12px; font-weight: bold; }
    .status-badge.off { background: #f85149; }
    
    #console-view { flex: 1; overflow-y: auto; padding: 15px; font-family: monospace; font-size: 13px; color: #8b949e; background: #0d1117; margin: 10px; border-radius: 8px; border: 1px solid #30363d; scroll-behavior: smooth; display: flex; align-items: center; justify-content: center; text-align: center; }
    #last-log { font-size: 16px; color: #e6edf3; font-weight: bold; }
    
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 10px; }
    .card { background: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; text-align: center; }
    
    .btn-big { background: #2f81f7; color: white; border: none; border-radius: 12px; padding: 20px; font-size: 16px; font-weight: bold; width: 100%; touch-action: manipulation; transition: transform 0.1s; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 5px; box-shadow: 0 4px 0 #1c4e94; }
    .btn-big:active { transform: translateY(4px); box-shadow: none; }
    .btn-red { background: #f85149; box-shadow: 0 4px 0 #9e2a26; }
    .btn-purple { background: #a371f7; box-shadow: 0 4px 0 #6e40c9; }
    
    .slider-container { padding: 0 15px 15px; }
    input[type=range] { width: 100%; height: 6px; background: #30363d; border-radius: 3px; outline: none; -webkit-appearance: none; }
    input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; background: #2f81f7; border-radius: 50%; cursor: pointer; }
    
    /* Onglets de Langue */
    .lang-tabs { display: flex; overflow-x: auto; gap: 8px; padding: 10px; -webkit-overflow-scrolling: touch; scrollbar-width: none; }
    .lang-tabs::-webkit-scrollbar { display: none; }
    .lang-btn { background: #161b22; border: 1px solid #30363d; color: #8b949e; padding: 8px 16px; border-radius: 20px; font-weight: 600; white-space: nowrap; flex-shrink: 0; }
    .lang-btn.active { background: #2f81f7; color: white; border-color: #2f81f7; }
    
    /* Sexe Switch */
    .gender-switch { display: flex; background: #161b22; border-radius: 8px; margin: 10px; border: 1px solid #30363d; overflow: hidden; }
    .gender-btn { flex: 1; padding: 10px; text-align: center; font-weight: bold; color: #8b949e; cursor: pointer; }
    .gender-btn.active { background: #2f81f7; color: white; }
  </style>
</head>
<body>

<header>
  <h1>Kommz Mobile</h1>
  <span id="status-badge" class="status-badge">ONLINE</span>
</header>

<div id="console-view">
  <div id="last-log">En attente de commandes...</div>
</div>

<div class="gender-switch">
    <div class="gender-btn active" id="btn-female" onclick="setGender('FEMALE')">FEMME</div>
    <div class="gender-btn" id="btn-male" onclick="setGender('MALE')">HOMME</div>
</div>

<div class="lang-tabs" id="lang-list">
  <div class="lang-btn active" onclick="setLang('EN')">🇺🇸 EN</div>
  <div class="lang-btn" onclick="setLang('FR')">🇫🇷 FR</div>
  <div class="lang-btn" onclick="setLang('ES')">🇪🇸 ES</div>
  <div class="lang-btn" onclick="setLang('DE')">🇩🇪 DE</div>
  <div class="lang-btn" onclick="setLang('IT')">🇮🇹 IT</div>
  <div class="lang-btn" onclick="setLang('RU')">🇷🇺 RU</div>
  <div class="lang-btn" onclick="setLang('PT')">🇵🇹 PT</div>
  <div class="lang-btn" onclick="setLang('PL')">🇵🇱 PL</div>
  <div class="lang-btn" onclick="setLang('TR')">🇹🇷 TR</div>
  <div class="lang-btn" onclick="setLang('JA')">🇯🇵 JA</div>
  <div class="lang-btn" onclick="setLang('ZH')">🇨🇳 ZH</div>
  <div class="lang-btn" onclick="setLang('KO')">🇰🇷 KO</div>
</div>

<div class="grid">
  <button class="btn-big" id="btn-mic" onclick="toggleMic()">
    <span>🎤</span>
    <span id="txt-mic">MICRO ON</span>
  </button>
  <button class="btn-big btn-red" onclick="panic()">
    <span>🚨</span>
    <span>PANIC</span>
  </button>
</div>

<div class="grid">
    <button class="btn-big btn-purple" onclick="sb('GG WP')">GG WP</button>
    <button class="btn-big btn-purple" onclick="sb('Rush B')">Rush B</button>
    <button class="btn-big btn-purple" onclick="sb('Need Help')">Help!</button>
    <button class="btn-big btn-purple" onclick="sb('Thank You')">Merci</button>
</div>

<div class="card" style="margin: 10px;">
  <div style="font-size: 12px; color: #8b949e; margin-bottom: 10px;">VOLUME TTS</div>
  <div class="slider-container">
    <input type="range" min="0.1" max="2.0" step="0.1" value="1.0" onchange="setVolume(this.value)">
  </div>
</div>

<script>
  // Détection automatique de l'API (Même port que la page)
  const API_URL = location.origin; 
  
  async function api(endpoint) {
    try {
      const r = await fetch(`${API_URL}/api/${endpoint}`, { headers: {'User-Agent': 'Kommz Mobile App'} });
      return await r.json();
    } catch(e) {
      document.getElementById('status-badge').className = "status-badge off";
      document.getElementById('status-badge').innerText = "OFFLINE";
      return null;
    }
  }

  function updateUI(data) {
    if(!data) return;
    document.getElementById('status-badge').className = "status-badge";
    document.getElementById('status-badge').innerText = "ONLINE";
    
    // Log
    if(data.last_text) document.getElementById('last-log').innerText = data.last_text;
    
    // Mic Button
    const btn = document.getElementById('btn-mic');
    const txt = document.getElementById('txt-mic');
    if(data.is_active) {
       btn.style.backgroundColor = "#2f81f7";
       btn.style.boxShadow = "0 4px 0 #1c4e94";
       txt.innerText = "MICRO ON";
    } else {
       btn.style.backgroundColor = "#8b949e";
       btn.style.boxShadow = "none";
       btn.style.transform = "translateY(4px)";
       txt.innerText = "MICRO OFF";
    }
    
    // Lang Tabs
    document.querySelectorAll('.lang-btn').forEach(b => {
       if(b.innerText.includes(data.target_lang)) b.classList.add('active');
       else b.classList.remove('active');
    });

    // Gender Tabs
    if (data.gender === 'MALE') {
        document.getElementById('btn-male').classList.add('active');
        document.getElementById('btn-female').classList.remove('active');
    } else {
        document.getElementById('btn-male').classList.remove('active');
        document.getElementById('btn-female').classList.add('active');
    }
  }

  async function toggleMic() { const d = await api('toggle'); updateUI(d); }
  async function panic() { const d = await api('panic'); updateUI(d); }
  async function setLang(l) { const d = await api(`set_language?lang=${l}`); updateUI(d); }
  async function setGender(g) { const d = await api(`set_gender?gender=${g}`); updateUI(d); }
  async function setVolume(v) { await api(`set_volume?val=${v}`); }
  async function sb(txt) { await api(`soundboard?text=${encodeURIComponent(txt)}`); }

  // Polling rapide
  setInterval(async () => {
    const d = await api('status');
    updateUI(d);
  }, 1000);
</script>
</body>
</html>