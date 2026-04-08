(function(){
  const $ = (id)=>document.getElementById(id);
  const slots = [$("slot1"),$("slot2"),$("slot3"),$("slot4"),$("slot5")];
  const list = $("variations_list");
  async function tick(){
    try{
      const r = await fetch("/state",{cache:"no-store"});
      const j = await r.json();
      (j.slots||[]).forEach((t,i)=>{ if(slots[i]) slots[i].textContent = t||""; });
      list.innerHTML = "";
      (j.variations||[]).forEach(v=>{
        const li = document.createElement("li");
        li.textContent = v;
        list.appendChild(li);
      });
    }catch(e){ /* ignore */ }
    setTimeout(tick, 600);
  }
  tick();
})();



