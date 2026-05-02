<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>JeevanDaan+</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --red:#C8102E;--red-dark:#8B0000;
  --bg:#0a0a0a;--bg2:#111;--bg3:#161616;
  --text:#f0ebe6;--muted:#777;
  --border:rgba(200,16,46,0.22);
  --font-display:'Segoe UI',system-ui,-apple-system,sans-serif;
  --font-body:system-ui,-apple-system,'Segoe UI',sans-serif;
}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:var(--font-body);overflow-x:hidden;line-height:1.7}

/* PARTICLES */
#particles{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden}
.pt{position:absolute;border-radius:50%;background:var(--red);opacity:0;animation:floatUp linear infinite}
@keyframes floatUp{
  0%{transform:translateY(100vh) scale(0);opacity:0}
  10%{opacity:.35}90%{opacity:.1}
  100%{transform:translateY(-10vh) scale(1);opacity:0}
}

/* BLOB */
#blob{position:fixed;width:550px;height:550px;border-radius:50%;
  background:radial-gradient(circle,rgba(200,16,46,.07) 0%,transparent 70%);
  pointer-events:none;z-index:0;transition:transform .9s ease;top:0;left:0}

/* HERO */
.hero{position:relative;min-height:100vh;display:flex;flex-direction:column;
  align-items:center;justify-content:center;text-align:center;padding:4rem 2rem;z-index:1;overflow:hidden}

/* animated wave bg */
.wave-bg{position:absolute;inset:0;z-index:-1}
.wave-bg svg{width:100%;height:100%;position:absolute}

/* blood drop */
.drop-wrap{margin-bottom:1.8rem;opacity:0;animation:dropIn 1.2s .2s cubic-bezier(.23,1.02,.32,1) forwards}
@keyframes dropIn{from{transform:translateY(-50px) scale(.5);opacity:0}to{transform:translateY(0) scale(1);opacity:1}}
.drop{width:68px;height:68px;animation:glow 2.8s ease-in-out infinite;display:block;margin:0 auto}
@keyframes glow{
  0%,100%{filter:drop-shadow(0 0 16px rgba(200,16,46,.65))}
  50%{filter:drop-shadow(0 0 36px rgba(200,16,46,1))}
}

/* eyebrow */
.eyebrow{font-size:.72rem;letter-spacing:.28em;text-transform:uppercase;color:var(--red);
  margin-bottom:.8rem;font-weight:500;opacity:0;animation:rise 1s .5s cubic-bezier(.23,1.02,.32,1) forwards}

/* title */
.hero-title{font-family:var(--font-display);font-size:clamp(3.2rem,9vw,7rem);font-weight:800;
  letter-spacing:-.03em;line-height:1;margin-bottom:.6rem;
  background:linear-gradient(130deg,#fff 20%,#ff4d6d 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  opacity:0;animation:rise 1s .7s cubic-bezier(.23,1.02,.32,1) forwards}

/* typewriter */
.tw-wrap{font-size:clamp(.95rem,2.2vw,1.2rem);color:#bbb;min-height:2em;margin:1rem 0 2rem;
  opacity:0;animation:rise 1s 1s cubic-bezier(.23,1.02,.32,1) forwards}
#tw{border-right:2px solid var(--red);padding-right:3px}

/* badges */
.badges{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;margin-bottom:3rem;
  opacity:0;animation:rise 1s 1.2s cubic-bezier(.23,1.02,.32,1) forwards}
.badge{padding:.3rem .85rem;border-radius:999px;font-size:.7rem;font-weight:500;
  letter-spacing:.04em;border:1px solid rgba(255,255,255,.09);background:rgba(255,255,255,.04);color:#bbb}
.badge.r{border-color:rgba(200,16,46,.4);background:rgba(200,16,46,.09);color:#ff7a8a}

/* scroll hint */
.scroll-hint{position:absolute;bottom:2rem;display:flex;flex-direction:column;align-items:center;
  gap:.4rem;color:var(--muted);font-size:.65rem;letter-spacing:.18em;text-transform:uppercase;
  opacity:0;animation:rise 1s 1.7s forwards}
.s-line{width:1px;height:38px;background:linear-gradient(to bottom,transparent,var(--red));
  animation:sLine 1.8s ease-in-out infinite}
@keyframes sLine{0%,100%{transform:scaleY(1);opacity:1}50%{transform:scaleY(.35);opacity:.35}}

@keyframes rise{from{transform:translateY(28px);opacity:0}to{transform:translateY(0);opacity:1}}

/* SECTIONS */
section{position:relative;z-index:1;padding:5rem 2rem;max-width:880px;margin:0 auto}
.s-label{font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--red);
  margin-bottom:.7rem;font-weight:500}
h2{font-family:var(--font-display);font-size:clamp(1.7rem,4vw,2.7rem);font-weight:800;
  line-height:1.1;margin-bottom:1.4rem;letter-spacing:-.02em}
p{color:#999;margin-bottom:1rem;font-size:.97rem}

/* CARDS */
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1.1rem;margin-top:2rem}
.card{background:var(--bg3);border:1px solid var(--border);border-radius:14px;padding:1.7rem;
  position:relative;overflow:hidden;transition:transform .3s,border-color .3s,box-shadow .3s}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--red),transparent);opacity:0;transition:opacity .3s}
.card:hover{transform:translateY(-5px);border-color:rgba(200,16,46,.5);
  box-shadow:0 20px 40px rgba(0,0,0,.4)}
.card:hover::before{opacity:1}
.c-icon{font-size:1.7rem;margin-bottom:.9rem}
.c-title{font-family:var(--font-display);font-size:1rem;font-weight:700;color:#eee;margin-bottom:.45rem}
.c-body{font-size:.85rem;color:#777;line-height:1.6}

/* FEATURE LIST */
.flist{list-style:none;margin-top:1.5rem}
.flist li{padding:.9rem 0;border-bottom:1px solid rgba(255,255,255,.05);
  display:flex;gap:.9rem;align-items:flex-start;font-size:.93rem;color:#999}
.flist li:last-child{border-bottom:none}
.fi{color:var(--red);font-size:1rem;flex-shrink:0;margin-top:3px}
.fl{font-weight:600;color:#ddd;display:block;margin-bottom:.15rem;font-family:var(--font-display)}

/* TABLE */
.stbl{width:100%;border-collapse:collapse;margin-top:1.5rem;font-size:.88rem}
.stbl th{text-align:left;padding:.7rem 1rem;border-bottom:1px solid rgba(200,16,46,.3);
  color:var(--red);font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;font-weight:500}
.stbl td{padding:.7rem 1rem;border-bottom:1px solid rgba(255,255,255,.04);color:#999}
.stbl td:first-child{color:#ddd}
.g{color:#4ade80;font-weight:600}.m{color:#f87171;font-weight:600}

/* FLOW */
.flow{margin-top:2rem;position:relative;padding-left:2rem}
.flow::before{content:'';position:absolute;left:0;top:0;bottom:0;width:1px;
  background:linear-gradient(to bottom,var(--red),transparent)}
.fs{position:relative;padding:0 0 2rem 1.5rem;opacity:0;transform:translateX(-18px);transition:opacity .5s,transform .5s}
.fs.on{opacity:1;transform:translateX(0)}
.fs::before{content:'';position:absolute;left:-4.5px;top:7px;width:9px;height:9px;
  border-radius:50%;background:var(--red);box-shadow:0 0 10px rgba(200,16,46,.7)}
.fs strong{color:#eee;font-weight:600;display:block;font-family:var(--font-display);margin-bottom:.2rem}
.fs span{font-size:.85rem;color:#666}

/* STACK */
.sgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:.75rem;margin-top:1.5rem}
.si{background:var(--bg3);border:1px solid rgba(255,255,255,.06);border-radius:10px;padding:.9rem 1.1rem}
.sl{color:var(--muted);font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.3rem}
.sv{color:#ddd;font-weight:500;font-size:.9rem}

/* DIVIDER */
.divider{width:100%;max-width:880px;margin:0 auto;overflow:hidden;line-height:0}
.divider svg{display:block;width:100%}

/* REVEAL */
.reveal{opacity:0;transform:translateY(28px);transition:opacity .7s,transform .7s}
.reveal.on{opacity:1;transform:translateY(0)}

/* FOOTER */
footer{position:relative;z-index:1;text-align:center;padding:4rem 2rem;
  border-top:1px solid rgba(255,255,255,.05)}
footer p{font-size:.82rem;color:#444;margin-bottom:.3rem}
footer strong{color:var(--red)}
</style>
</head>
<body>

<div id="particles"></div>
<div id="blob"></div>

<!-- HERO -->
<div class="hero">
  <div class="wave-bg">
    <svg viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <radialGradient id="rg" cx="50%" cy="38%" r="55%">
          <stop offset="0%" stop-color="#C8102E" stop-opacity="0.13"/>
          <stop offset="100%" stop-color="#0a0a0a" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect width="1440" height="900" fill="url(#rg)"/>
      <path fill="rgba(200,16,46,.045)">
        <animate attributeName="d" dur="9s" repeatCount="indefinite"
          values="M0,580 C280,500 560,660 840,560 C1120,460 1300,620 1440,540 L1440,900 L0,900 Z;
                  M0,560 C280,640 560,520 840,600 C1120,680 1300,540 1440,580 L1440,900 L0,900 Z;
                  M0,580 C280,500 560,660 840,560 C1120,460 1300,620 1440,540 L1440,900 L0,900 Z"/>
      </path>
      <path fill="rgba(200,16,46,.065)">
        <animate attributeName="d" dur="13s" repeatCount="indefinite"
          values="M0,700 C360,630 720,750 1080,670 C1260,630 1380,690 1440,670 L1440,900 L0,900 Z;
                  M0,720 C360,790 720,670 1080,730 C1260,770 1380,710 1440,690 L1440,900 L0,900 Z;
                  M0,700 C360,630 720,750 1080,670 C1260,630 1380,690 1440,670 L1440,900 L0,900 Z"/>
      </path>
    </svg>
  </div>

  <div class="drop-wrap">
    <svg class="drop" viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg">
      <path d="M50 8 C50 8,13 62,13 80 C13 100,30 112,50 112 C70 112,87 100,87 80 C87 62,50 8,50 8Z" fill="#C8102E"/>
      <path d="M50 28 C50 28,31 66,31 80 C31 91,39 99,50 99" stroke="rgba(255,255,255,.22)" stroke-width="3" fill="none" stroke-linecap="round"/>
    </svg>
  </div>

  <div class="eyebrow">A Blood Donation Ecosystem</div>
  <h1 class="hero-title">JeevanDaan+</h1>

  <div class="tw-wrap"><span id="tw"></span></div>

  <div class="badges">
    <span class="badge r">Django 5.1</span>
    <span class="badge">DRF 3.17</span>
    <span class="badge">Python 3.11</span>
    <span class="badge">PostgreSQL</span>
    <span class="badge r">Twilio SMS + WhatsApp</span>
    <span class="badge">JWT + bcrypt</span>
    <span class="badge">Cloudinary</span>
    <span class="badge">APScheduler</span>
    <span class="badge">Gunicorn</span>
  </div>

  <div class="scroll-hint">
    <span>scroll</span>
    <div class="s-line"></div>
  </div>
</div>

<!-- WAVE DIVIDER -->
<div class="divider">
  <svg viewBox="0 0 1440 60" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" height="60">
    <path d="M0,30 C360,60 1080,0 1440,30 L1440,60 L0,60 Z" fill="#111111"/>
  </svg>
</div>

<!-- THE MISSION -->
<section class="reveal">
  <div class="s-label">The Mission</div>
  <h2>Every 2 seconds,<br/>someone in India needs blood.</h2>
  <p>JeevanDaan+ is the backend infrastructure that bridges that gap — a full REST API platform connecting three types of users, with real-time geo-matching, verified identities, and a reliability engine that rewards the selfless.</p>
  <div class="cards">
    <div class="card">
      <div class="c-icon">🧑</div>
      <div class="c-title">Donor</div>
      <div class="c-body">Registers, Aadhaar-verified, gets geo-targeted SMS/WhatsApp alerts when a nearby hospital needs their blood group. Every donation builds a score.</div>
    </div>
    <div class="card">
      <div class="c-icon">🏥</div>
      <div class="c-title">Partner</div>
      <div class="c-body">Hospital or blood bank. Manages live stock, posts donation requests, runs camps, and verifies donations — behind a single admin-gated dashboard.</div>
    </div>
    <div class="card">
      <div class="c-icon">🤝</div>
      <div class="c-title">Attender</div>
      <div class="c-body">Patient's family member. Raises a blood request visible to all verified partners — fulfilled by a direct donor or via inter-partner exchange.</div>
    </div>
  </div>
</section>

<!-- FEATURES -->
<section class="reveal">
  <div class="s-label">Core Features</div>
  <h2>Built for real emergencies.</h2>
  <ul class="flist">
    <li><span class="fi">📍</span><div><span class="fl">Geo-Matching Engine</span>Bounding-box SQL pre-filter + geodesic precision via geopy. Distance-sorted results, 10km default, fully configurable.</div></li>
    <li><span class="fi">🔔</span><div><span class="fl">Multi-Channel Notification Engine</span>SMS + WhatsApp via Twilio. Fallback call queued if both fail. All notifications run in background threads — zero HTTP blocking.</div></li>
    <li><span class="fi">🔐</span><div><span class="fl">OTP Donation Verification</span>Unique 6-digit OTP generated on acceptance, sent to partner. Scanned at donation time. History and scores update atomically.</div></li>
    <li><span class="fi">🏕️</span><div><span class="fl">Donation Camp System</span>Partners schedule camps. Donors within 20km auto-notified. Dashboard freezes until stock is updated post-camp. CSV enrollment download.</div></li>
    <li><span class="fi">🔄</span><div><span class="fl">Inter-Partner Blood Exchange</span>Hospital A has no stock? System finds nearest Hospital B within 20km and auto-raises a transfer request between them.</div></li>
    <li><span class="fi">⏰</span><div><span class="fl">Background Scheduler</span>Silently expires stale requests every 15 min, auto-unlocks accounts every hour, cleans unvisited assignments every 30 min.</div></li>
  </ul>
</section>

<!-- RELIABILITY -->
<section class="reveal">
  <div class="s-label">Donor Reliability</div>
  <h2>Every action<br/>has consequences.</h2>
  <p>A scoring system that rewards consistency and penalises no-shows. Donors who cancel repeatedly get locked. Donors who show up build a legacy.</p>
  <table class="stbl">
    <thead><tr><th>Event</th><th>Effect</th></tr></thead>
    <tbody>
      <tr><td>Donation verified by bank</td><td><span class="g">+10 score</span></td></tr>
      <tr><td>Cancellation</td><td><span class="m">−10 score</span></td></tr>
      <tr><td>3+ cancellations</td><td><span class="m">Locked 30 days</span></td></tr>
      <tr><td>Lock period expires</td><td>Auto-unlocked by scheduler</td></tr>
      <tr><td>2+ donations</td><td>🥉 Bronze Donor</td></tr>
      <tr><td>5+ donations</td><td>🥇 Gold Donor</td></tr>
      <tr><td>10+ donations</td><td>💎 Platinum Donor</td></tr>
    </tbody>
  </table>
</section>

<!-- LIFECYCLE -->
<section class="reveal">
  <div class="s-label">How It Works</div>
  <h2>The request lifecycle.</h2>
  <p>From the moment a hospital posts a need to the moment blood is verified — every step tracked, scored, and stored.</p>
  <div class="flow" id="flow">
    <div class="fs"><strong>Partner posts open request</strong><span>Visible to all nearby donors. Notifications fire in background threads.</span></div>
    <div class="fs"><strong>Nearby donors notified via SMS + WhatsApp</strong><span>Geo-filtered within 10km. Each message includes distance from donor.</span></div>
    <div class="fs"><strong>Donor accepts → status: assigned</strong><span>Unique 6-digit OTP generated instantly and delivered to the partner.</span></div>
    <div class="fs"><strong>Donor arrives → partner verifies OTP</strong><span>Real-time confirmation. OTP marks physical arrival at blood bank.</span></div>
    <div class="fs"><strong>Partner verifies donation → fulfilled</strong><span>DonationHistory created. Score +10. Member tag auto-upgraded.</span></div>
    <div class="fs"><strong>Both sides rate each other ⭐</strong><span>5+ complaints on any partner triggers automatic deactivation.</span></div>
  </div>
</section>

<!-- SECURITY -->
<section class="reveal">
  <div class="s-label">Security</div>
  <h2>Identity protected.<br/>Data locked.</h2>
  <ul class="flist">
    <li><span class="fi">🔒</span><div><span class="fl">bcrypt password hashing</span>Passwords are never stored in plain text. Ever.</div></li>
    <li><span class="fi">🪙</span><div><span class="fl">Short-lived JWT tokens</span>1-hour access, 7-day refresh. Donor and partner tokens are fully separate identity systems.</div></li>
    <li><span class="fi">🛡️</span><div><span class="fl">Aadhaar excluded from all API responses</span>Stored for verification — never serialized out to any endpoint.</div></li>
    <li><span class="fi">👁️</span><div><span class="fl">Admin panel is read-only</span>All sensitive fields locked. No editing, no deleting via admin.</div></li>
    <li><span class="fi">✅</span><div><span class="fl">Partners require manual approval</span>No partner goes live without is_verified + is_live set by admin.</div></li>
  </ul>
</section>

<!-- STACK -->
<section class="reveal">
  <div class="s-label">Tech Stack</div>
  <h2>What powers it.</h2>
  <div class="sgrid">
    <div class="si"><div class="sl">Framework</div><div class="sv">Django 5.1.7 + DRF 3.17</div></div>
    <div class="si"><div class="sl">Auth</div><div class="sv">PyJWT + bcrypt</div></div>
    <div class="si"><div class="sl">Database</div><div class="sv">PostgreSQL via psycopg2</div></div>
    <div class="si"><div class="sl">Media</div><div class="sv">Cloudinary</div></div>
    <div class="si"><div class="sl">Notifications</div><div class="sv">Twilio SMS + WhatsApp</div></div>
    <div class="si"><div class="sl">Geo Engine</div><div class="sv">geopy — geodesic distance</div></div>
    <div class="si"><div class="sl">Scheduler</div><div class="sv">APScheduler</div></div>
    <div class="si"><div class="sl">Static Files</div><div class="sv">WhiteNoise</div></div>
    <div class="si"><div class="sl">Server</div><div class="sv">Gunicorn — preload</div></div>
    <div class="si"><div class="sl">Runtime</div><div class="sv">Python 3.11.9</div></div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <svg style="display:block;margin:0 auto 1.5rem" width="36" height="44" viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg" opacity=".35">
    <path d="M50 8 C50 8,13 62,13 80 C13 100,30 112,50 112 C70 112,87 100,87 80 C87 62,50 8,50 8Z" fill="#C8102E"/>
  </svg>
  <p><strong>JeevanDaan+</strong> — Built to save lives.</p>
  <p>Every donation matters. Every request counts. Every life is worth the effort.</p>
  <p style="margin-top:.8rem;font-size:.72rem">🇮🇳 Made in India</p>
</footer>

<script>
// Particles
const pc = document.getElementById('particles');
for(let i=0;i<20;i++){
  const p=document.createElement('div');
  p.className='pt';
  const s=Math.random()*4+2;
  p.style.cssText=`width:${s}px;height:${s}px;left:${Math.random()*100}%;animation-duration:${9+Math.random()*12}s;animation-delay:${Math.random()*12}s`;
  pc.appendChild(p);
}

// Glow blob
document.addEventListener('mousemove',e=>{
  const b=document.getElementById('blob');
  b.style.transform=`translate(${e.clientX-275}px,${e.clientY-275}px)`;
});

// Typewriter
const phrases=[
  'Jeevan means life. Daan means gift.',
  'Real-time blood request matching.',
  'Geo-aware donor notifications.',
  'OTP-verified donations.',
  'A platform built for emergencies.',
];
let pi=0,ci=0,del=false;
const tw=document.getElementById('tw');
function type(){
  const ph=phrases[pi];
  if(!del){tw.textContent=ph.slice(0,++ci);if(ci===ph.length){del=true;setTimeout(type,1900);return}}
  else{tw.textContent=ph.slice(0,--ci);if(ci===0){del=false;pi=(pi+1)%phrases.length}}
  setTimeout(type,del?32:58);
}
setTimeout(type,1600);

// Scroll reveal
const obs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('on')});
},{threshold:.1});
document.querySelectorAll('.reveal,.fs').forEach(el=>obs.observe(el));
</script>
</body>
</html>
