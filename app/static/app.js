const $=id=>document.getElementById(id),esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const label={keep:"Kept",check:"Listen again",drop:"Dropped"};let last=null;
let birdAudio = null;
window.playBird = async (name) => {
  if (birdAudio) { birdAudio.pause(); birdAudio = null; }
  try {
    const r = await fetch("/api/audio?bird=" + encodeURIComponent(name));
    if (r.ok) {
      const j = await r.json();
      if (j.url) { birdAudio = new Audio(j.url); birdAudio.play(); }
    }
  } catch(e) {}
};
// Screen time: seconds the page was visible, stored only in this browser.
let seen=Number(localStorage.getItem("screenSec")||0),t0=document.visibilityState==="visible"?Date.now():0;
function tick(){if(t0){seen+=(Date.now()-t0)/1000;t0=0}if(document.visibilityState==="visible")t0=Date.now();try{localStorage.setItem("screenSec",seen)}catch{}}
document.addEventListener("visibilitychange",tick);addEventListener("pagehide",tick);
$("date").value=new Date().toISOString().slice(0,10);
const mmss=s=>Math.floor(s/60)+":"+String(Math.floor(s%60)).padStart(2,"0");
function draw(rows,mins){const names=[...new Set(rows.map(r=>r.name))],W=640,L=150,H=names.length*28+34,end=Math.max(...rows.map(r=>r.t),60),x=t=>L+(W-L-12)*t/end;
 let g=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Timeline of ${rows.length} detections across ${names.length} species during a ${mins} minute walk. Full list in the table below.">`;
 names.forEach((n,i)=>{const y=22+i*28;g+=`<line class="l" x1="${L}" x2="${W-12}" y1="${y}" y2="${y}"/><text x="4" y="${y+4}" style="cursor:pointer" onclick="playBird('${esc(n)}')">${esc(n.length>22?n.slice(0,21)+"…":n)}</text>`});
 rows.forEach(r=>{const y=22+names.indexOf(r.name)*28;g+=`<circle class="dot ${r.status}" cx="${x(r.t).toFixed(1)}" cy="${y}" r="${5+r.conf*4}" style="cursor:pointer" onclick="playBird('${esc(r.name)}')"><title>${esc(r.name)} ${mmss(r.t)} ${label[r.status]} (Click to listen)</title></circle>`});
 return g+`<text x="${L}" y="${H-6}">0:00</text><text x="${W-52}" y="${H-6}">${mmss(end)}</text></svg>`}
function show(d){last=d;const s=d.summary;$("res").hidden=false;$("demoNote").hidden=!d.demo;
 $("sum").textContent=`${s.keep} detections kept across ${s.species_kept.length} species, ${s.check} to listen to again, ${s.drop} dropped as unlikely here.`;
 $("sky").innerHTML=draw(d.rows,d.minutes);$("journal").textContent=d.journal_ai||d.journal;
 $("tb").innerHTML=d.rows.map(r=>`<tr><td>${esc(r.name)}</td><td>${mmss(r.t)}</td><td>${Math.round(r.conf*100)}%</td><td class="${r.status}">${label[r.status]}</td><td>${esc(r.why)}</td></tr>`).join("");
 tick();$("time").textContent=`${d.minutes} minutes outside, about ${Math.max(1,Math.round(seen/60))} minute${seen>90?"s":""} on screen in this browser.`;
 $("res").focus();$("res").scrollIntoView({behavior:matchMedia("(prefers-reduced-motion:reduce)").matches?"auto":"smooth"})}
async function api(url,body){$("err").textContent="";try{const r=await fetch(url,body?{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)}:{});
 const j=await r.json();if(!r.ok)throw new Error(typeof j.detail==="string"?j.detail:"Check the date, time and CSV file.");show(j)}catch(e){$("err").textContent=e.message||"Could not reach the server. Try again."}}
$("demo").onclick=()=>api("/api/demo");
$("f").onsubmit=async e=>{e.preventDefault();const f=$("file").files[0];if(!f){$("err").textContent="Choose the BirdNET CSV file first, or try the sample walk.";return}
 if(f.size>1e6){$("err").textContent="That file is over 1 MB. Export a shorter walk.";return}
 api("/api/analyze",{csv:await f.text(),date:$("date").value,start:$("start").value,place:$("place").value})};
$("say").onclick=()=>{speechSynthesis.cancel();const u=new SpeechSynthesisUtterance($("journal").textContent);u.rate=.9;speechSynthesis.speak(u)};
$("dl").onclick=()=>{const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([$("journal").textContent+"\n"],{type:"text/plain"}));a.download="field-journal.txt";a.click();URL.revokeObjectURL(a.href)};
