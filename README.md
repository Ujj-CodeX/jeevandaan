<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>JeevanDaan+ — README</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inter:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --red: #C8102E;
    --red-dark: #8B0000;
    --red-glow: rgba(200, 16, 46, 0.18);
    --bg: #0a0a0a;
    --bg2: #111111;
    --bg3: #161616;
    --text: #f0ebe6;
    --muted: #888;
    --border: rgba(200,16,46,0.2);
  }

  html { scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
    overflow-x: hidden;
    line-height: 1.7;
  }

  /* ── PARTICLES ── */
  #particles {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
  }
  .particle {
    position: absolute;
    border-radius: 50%;
    background: var(--red);
    opacity: 0;
    animation: float linear infinite;
  }
  @keyframes float {
    0%   { transform: translateY(100vh) scale(0); opacity: 0; }
    10%  { opacity: 0.4; }
    90%  { opacity: 0.15; }
    100% { transform: translateY(-10vh) scale(1); opacity: 0; }
  }

  /* ── HERO ── */
  .hero {
    position: relative;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 4rem 2rem;
    z-index: 1;
    overflow: hidden;
  }

  /* Animated wave background */
  .wave-bg {
    position: absolute;
    inset: 0;
    z-index: -1;
  }
  .wave-bg svg {
    width: 100%;
    height: 100%;
    position: absolute;
  }

  /* Blood drop */
  .drop-wrap {
    margin-bottom: 2rem;
    animation: dropIn 1.2s cubic-bezier(.23,1.02,.32,1) forwards;
    opacity: 0;
  }
  @keyframes dropIn {
    from { transform: translateY(-60px) scale(0.5); opacity: 0; }
    to   { transform: translateY(0) scale(1); opacity: 1; }
  }
  .drop {
    width: 70px;
    height: 70px;
    filter: drop-shadow(0 0 24px rgba(200,16,46,0.7));
    animation: pulse 2.8s ease-in-out infinite;
  }
  @keyframes pulse {
    0%,100% { filter: drop-shadow(0 0 18px rgba(200,16,46,0.6)); transform: scale(1); }
    50%      { filter: drop-shadow(0 0 36px rgba(200,16,46,0.95)); transform: scale(1.06); }
  }

  /* Title */
  .hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(3.5rem, 9vw, 7rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1;
    margin-bottom: 0.5rem;
    opacity: 0;
    animation: riseUp 1s 0.4s cubic-bezier(.23,1.02,.32,1) forwards;
    background: linear-gradient(135deg, #fff 30%, var(--red) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .hero-sub {
    font-family: 'Syne', sans-serif;
    font-size: clamp(0.9rem, 2.5vw, 1.2rem);
    font-weight: 400;
    color: var(--muted);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    opacity: 0;
    animation: riseUp 1s 0.65s cubic-bezier(.23,1.02,.32,1) forwards;
  }

  /* Typewriter */
  .typewriter-wrap {
    font-size: clamp(1rem, 2.5vw, 1.25rem);
    color: #ccc;
    min-height: 2.2em;
    margin-bottom: 2.5rem;
    opacity: 0;
    animation: riseUp 1s 0.9s cubic-bezier(.23,1.02,.32,1) forwards;
  }
  .typewriter { border-right: 2px solid var(--red); padding-right: 4px; }

  @keyframes riseUp {
    from { transform: translateY(30px); opacity: 0; }
    to   { transform: translateY(0); opacity: 1; }
  }

  /* Badges */
  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    justify-content: center;
    margin-bottom: 3rem;
    opacity: 0;
    animation: riseUp 1s 1.1s cubic-bezier(.23,1.02,.32,1) forwards;
  }
  .badge {
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.04);
    color: #ccc;
    backdrop-filter: blur(4px);
  }
  .badge.red { border-color: rgba(200,16,46,0.4); background: rgba(200,16,46,0.08); color: #ff6b7a; }

  /* Scroll indicator */
  .scroll-hint {
    position: absolute;
    bottom: 2.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
    color: var(--muted);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    opacity: 0;
    animation: riseUp 1s 1.5s forwards;
  }
  .scroll-line {
    width: 1px;
    height: 40px;
    background: linear-gradient(to bottom, transparent, var(--red));
    animation: scrollLine 1.8s ease-in-out infinite;
  }
  @keyframes scrollLine {
    0%,100% { transform: scaleY(1); opacity: 1; }
    50%      { transform: scaleY(0.4); opacity: 0.4; }
  }

  /* ── WAVE DIVIDER ── */
  .wave-divider svg { display: block; }

  /* ── SECTIONS ── */
  section {
    position: relative;
    z-index: 1;
    padding: 5rem 2rem;
    max-width: 900px;
    margin: 0 auto;
  }

  .section-label {
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--red);
    margin-bottom: 0.75rem;
    font-weight: 500;
  }

  h2 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(1.8rem, 4vw, 2.8rem);
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
  }

  p { color: #aaa; margin-bottom: 1rem; font-size: 1rem; }

  /* ── STORY CARDS ── */
  .story-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.2rem;
    margin-top: 2rem;
  }
  .story-card {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.8rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s, border-color 0.3s;
  }
  .story-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--red), transparent);
    opacity: 0;
    transition: opacity 0.3s;
  }
  .story-card:hover { transform: translateY(-4px); border-color: rgba(200,16,46,0.45); }
  .story-card:hover::before { opacity: 1; }
  .card-icon { font-size: 1.8rem; margin-bottom: 1rem; }
  .card-title { font-family: 'Syne', sans-serif; font-size: 1.05rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; }
  .card-body { font-size: 0.88rem; color: #888; line-height: 1.6; }

  /* ── FEATURE LIST ── */
  .feature-list { list-style: none; margin-top: 1.5rem; }
  .feature-list li {
    padding: 1rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    font-size: 0.95rem;
    color: #aaa;
  }
  .feature-list li:last-child { border-bottom: none; }
  .f-icon { color: var(--red); font-size: 1.1rem; flex-shrink: 0; margin-top: 2px; }
  .f-label { font-weight: 500; color: #ddd; display: block; margin-bottom: 0.2rem; font-family: 'Syne', sans-serif; }

  /* ── SCORE TABLE ── */
  .score-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1.5rem;
    font-size: 0.9rem;
  }
  .score-table th {
    text-align: left;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid rgba(200,16,46,0.3);
    color: var(--red);
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 500;
  }
  .score-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    color: #aaa;
  }
  .score-table td:first-child { color: #ddd; }
  .plus { color: #4ade80; font-weight: 600; }
  .minus { color: #f87171; font-weight: 600; }

  /* ── FLOW ── */
  .flow {
    margin-top: 2rem;
    position: relative;
    padding-left: 2rem;
  }
  .flow::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 1px;
    background: linear-gradient(to bottom, var(--red), transparent);
  }
  .flow-step {
    position: relative;
    padding: 0 0 2rem 1.5rem;
    opacity: 0;
    transform: translateX(-20px);
    transition: opacity 0.5s, transform 0.5s;
  }
  .flow-step.visible { opacity: 1; transform: translateX(0); }
  .flow-step::before {
    content: '';
    position: absolute;
    left: -4.5px;
    top: 6px;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--red);
    box-shadow: 0 0 10px var(--red);
  }
  .flow-step strong { color: #fff; font-weight: 500; display: block; font-family: 'Syne', sans-serif; }
  .flow-step span { font-size: 0.88rem; color: #666; }

  /* ── STACK GRID ── */
  .stack-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.8rem;
    margin-top: 1.5rem;
  }
  .stack-item {
    background: var(--bg3);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.85rem;
  }
  .stack-item .s-label { color: var(--muted); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.3rem; }
  .stack-item .s-val { color: #ddd; font-weight: 500; }

  /* ── FOOTER ── */
  footer {
    position: relative;
    z-index: 1;
    text-align: center;
    padding: 4rem 2rem;
    border-top: 1px solid rgba(255,255,255,0.05);
  }
  footer p { font-size: 0.85rem; color: #444; margin-bottom: 0.4rem; }
  footer strong { color: var(--red); }

  /* ── SCROLL REVEAL ── */
  .reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.7s, transform 0.7s;
  }
  .reveal.visible { opacity: 1; transform: translateY(0); }

  /* Red glow blob */
  .glow-blob {
    position: fixed;
    width: 600px;
    height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(200,16,46,0.06) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    transition: transform 0.8s ease;
  }
</style>
</head>
<body>

<div id="particles"></div>
<div class="glow-blob" id="blob"></div>

<!-- ══ HERO ══════════════════════════════════════════ -->
<div class="hero">
  <div class="wave-bg">
    <svg viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <radialGradient id="rg" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stop-color="#C8102E" stop-opacity="0.12"/>
          <stop offset="100%" stop-color="#0a0a0a" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect width="1440" height="900" fill="url(#rg)"/>
      <path d="M0,600 C240,520 480,680 720,580 C960,480 1200,640 1440,560 L1440,900 L0,900 Z" fill="rgba(200,16,46,0.04)">
        <animate attributeName="d" dur="8s" repeatCount="indefinite"
          values="M0,600 C240,520 480,680 720,580 C960,480 1200,640 1440,560 L1440,900 L0,900 Z;
                  M0,580 C240,660 480,540 720,620 C960,700 1200,560 1440,600 L1440,900 L0,900 Z;
                  M0,600 C240,520 480,680 720,580 C960,480 1200,640 1440,560 L1440,900 L0,900 Z"/>
      </path>
      <path d="M0,700 C360,640 720,760 1080,680 C1260,640 1380,700 1440,680 L1440,900 L0,900 Z" fill="rgba(200,16,46,0.06)">
        <animate attributeName="d" dur="11s" repeatCount="indefinite"
          values="M0,700 C360,640 720,760 1080,680 C1260,640 1380,700 1440,680 L1440,900 L0,900 Z;
                  M0,720 C360,780 720,680 1080,740 C1260,780 1380,720 1440,700 L1440,900 L0,900 Z;
                  M0,700 C360,640 720,760 1080,680 C1260,640 1380,700 1440,680 L1440,900 L0,900 Z"/>
      </path>
    </svg>
  </div>

  <div class="drop-wrap">
    <svg class="drop" viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg">
      <path d="M50 10 C50 10, 15 60, 15 78 C15 97, 31 110, 50 110 C69 110, 85 97, 85 78 C85 60, 50 10, 50 10 Z" fill="#C8102E"/>
      <path d="M50 30 C50 30, 32 65, 32 78 C32 88, 40 96, 50 96" stroke="rgba(255,255,255,0.25)" stroke-width="3" fill="none" stroke-linecap="round"/>
    </svg>
  </div>

  <div class="hero-sub">A Blood Donation Ecosystem</div>
  <h1 class="hero-title">JeevanDaan+</h1>

  <div class="typewriter-wrap">
    <span id="tw" class="typewriter"></span>
  </div>

  <div class="badges">
    <span class="badge red">Django 5.1</span>
    <span class="badge">DRF 3.17</span>
    <span class="badge">Python 3.11</span>
    <span class="badge">PostgreSQL</span>
    <span class="badge red">Twilio SMS + WhatsApp</span>
    <span class="badge">Cloudinary</span>
    <span class="badge">JWT + bcrypt</span>
    <span class="badge">APScheduler</span>
    <span class="badge">Gunicorn</span>
  </div>

  <div class="scroll-hint">
    <span>scroll</span>
    <div class="scroll-line"></div>
  </div>
</div>

<!-- ══ WHAT IS IT ══════════════════════════════════ -->
<section class="reveal">
  <div class="section-label">The Mission</div>
  <h2>Every 2 seconds,<br/>someone in India needs blood.</h2>
  <p>JeevanDaan+ is the backend infrastructure that bridges that gap — a full REST API ecosystem connecting three types of users on a single platform, with real-time geo-matching, verified identities, and a reliability engine that rewards the selfless.</p>

  <div class="story-grid">
    <div class="story-card">
      <div class="card-icon">🧑</div>
      <div class="card-title">Donor</div>
      <div class="card-body">Registers, gets Aadhaar-verified, and receives geo-targeted SMS/WhatsApp alerts when a nearby hospital needs their blood group. Every donation builds a score. Score unlocks legacy.</div>
    </div>
    <div class="story-card">
      <div class="card-icon">🏥</div>
      <div class="card-title">Partner</div>
      <div class="card-body">Hospital or blood bank. Manages live blood stock, posts donation requests, runs donation camps, and verifies donations — all behind a single admin-gated dashboard.</div>
    </div>
    <div class="story-card">
      <div class="card-icon">🤝</div>
      <div class="card-title">Attender</div>
      <div class="card-body">Patient's family member. Raises a blood request visible to all verified partners. Gets fulfilled by a direct donor or via inter-partner blood exchange network.</div>
    </div>
  </div>
</section>

<!-- ══ FEATURES ════════════════════════════════════ -->
<section class="reveal">
  <div class="section-label">What's Inside</div>
  <h2>Built for real emergencies.</h2>
  <ul class="feature-list">
    <li>
      <span class="f-icon">📍</span>
      <div>
        <span class="f-label">Geo-Matching Engine</span>
        Bounding-box SQL pre-filter trims the dataset first, then geodesic distance via geopy gives precision. Finds nearby donors and partners independently. Distance-sorted results, 10km default radius.
      </div>
    </li>
    <li>
      <span class="f-icon">🔔</span>
      <div>
        <span class="f-label">Multi-Channel Notification Engine</span>
        SMS + WhatsApp via Twilio on every critical event. Fallback call queued if both fail. All notifications run in background threads — they never block the HTTP response.
      </div>
    </li>
    <li>
      <span class="f-icon">🔐</span>
      <div>
        <span class="f-label">OTP Donation Verification</span>
        On donor acceptance, a unique 6-digit OTP is generated and sent to the partner. Partner scans it at donation time. Donation history and scores update atomically.
      </div>
    </li>
    <li>
      <span class="f-icon">🏕️</span>
      <div>
        <span class="f-label">Donation Camp System</span>
        Partners schedule camps. Donors within 20km get automatically notified. Dashboard freezes post-camp until stock is updated — enforcing accountability. CSV enrollment download on camp date.
      </div>
    </li>
    <li>
      <span class="f-icon">🔄</span>
      <div>
        <span class="f-label">Inter-Partner Blood Exchange</span>
        Hospital A has no stock? The system finds the nearest Hospital B within 20km with available units and automatically raises a transfer request between them.
      </div>
    </li>
    <li>
      <span class="f-icon">⏰</span>
      <div>
        <span class="f-label">Background Scheduler</span>
        APScheduler silently expires stale requests every 15 min, auto-unlocks donor accounts every hour, and cleans up unvisited assignments every 30 min.
      </div>
    </li>
  </ul>
</section>

<!-- ══ RELIABILITY ENGINE ══════════════════════════ -->
<section class="reveal">
  <div class="section-label">Donor Reliability</div>
  <h2>Every action<br/>has consequences.</h2>
  <p>A scoring system that rewards consistency and penalises no-shows. Donors who cancel repeatedly get locked out. Donors who show up build a legacy.</p>

  <table class="score-table">
    <thead>
      <tr><th>Event</th><th>Effect</th></tr>
    </thead>
    <tbody>
      <tr><td>Donation verified by bank</td><td><span class="plus">+10 score</span></td></tr>
      <tr><td>Cancellation</td><td><span class="minus">−10 score</span></td></tr>
      <tr><td>3+ cancellations</td><td><span class="minus">Account locked 30 days</span></td></tr>
      <tr><td>Lock period expires</td><td>Auto-unlocked by scheduler</td></tr>
      <tr><td>2+ donations</td><td>Bronze Donor</td></tr>
      <tr><td>5+ donations</td><td>Gold Donor</td></tr>
      <tr><td>10+ donations</td><td>Platinum Donor</td></tr>
    </tbody>
  </table>
</section>

<!-- ══ REQUEST LIFECYCLE ══════════════════════════ -->
<section class="reveal">
  <div class="section-label">How It Works</div>
  <h2>The request lifecycle.</h2>
  <p>From the moment a hospital posts a need to the moment blood is verified — every step is tracked, scored, and stored.</p>

  <div class="flow" id="flow">
    <div class="flow-step">
      <strong>Partner posts open request</strong>
      <span>Visible to all nearby donors. Notifications fire in background.</span>
    </div>
    <div class="flow-step">
      <strong>Nearby donors notified via SMS + WhatsApp</strong>
      <span>Geo-filtered within 10km. Message includes distance from donor.</span>
    </div>
    <div class="flow-step">
      <strong>Donor accepts → status: assigned</strong>
      <span>Unique 6-digit OTP generated and sent to the partner.</span>
    </div>
    <div class="flow-step">
      <strong>Donor arrives → partner verifies OTP</strong>
      <span>Real-time confirmation via chat. OTP marks arrival.</span>
    </div>
    <div class="flow-step">
      <strong>Partner verifies donation → status: fulfilled</strong>
      <span>DonationHistory created. Score +10. Member tag upgraded.</span>
    </div>
    <div class="flow-step">
      <strong>Both sides rate each other ⭐</strong>
      <span>5+ partner complaints = auto-deactivation.</span>
    </div>
  </div>
</section>

<!-- ══ SECURITY ════════════════════════════════════ -->
<section class="reveal">
  <div class="section-label">Security</div>
  <h2>Identity protected.<br/>Data locked.</h2>
  <ul class="feature-list">
    <li><span class="f-icon">🔒</span><div><span class="f-label">bcrypt password hashing</span>Passwords are never stored in plain text. Ever.</div></li>
    <li><span class="f-icon">🪙</span><div><span class="f-label">Short-lived JWT tokens</span>1-hour access tokens, 7-day refresh. Dual identity — donor and partner tokens are fully separate.</div></li>
    <li><span class="f-icon">🛡️</span><div><span class="f-label">Aadhaar excluded from all API responses</span>Stored for verification — never serialized out to any endpoint.</div></li>
    <li><span class="f-icon">👁️</span><div><span class="f-label">Admin panel is read-only</span>All sensitive fields are locked. No editing, no deleting.</div></li>
    <li><span class="f-icon">✅</span><div><span class="f-label">Partners require manual admin approval</span>No partner goes live without is_verified + is_live set by admin.</div></li>
  </ul>
</section>

<!-- ══ STACK ═══════════════════════════════════════ -->
<section class="reveal">
  <div class="section-label">Tech Stack</div>
  <h2>What powers it.</h2>
  <div class="stack-grid">
    <div class="stack-item"><div class="s-label">Framework</div><div class="s-val">Django 5.1.7 + DRF 3.17</div></div>
    <div class="stack-item"><div class="s-label">Auth</div><div class="s-val">PyJWT + bcrypt</div></div>
    <div class="stack-item"><div class="s-label">Database</div><div class="s-val">PostgreSQL via psycopg2</div></div>
    <div class="stack-item"><div class="s-label">Media</div><div class="s-val">Cloudinary</div></div>
    <div class="stack-item"><div class="s-label">Notifications</div><div class="s-val">Twilio SMS + WhatsApp</div></div>
    <div class="stack-item"><div class="s-label">Geo Engine</div><div class="s-val">geopy — geodesic distance</div></div>
    <div class="stack-item"><div class="s-label">Scheduler</div><div class="s-val">APScheduler + django-apscheduler</div></div>
    <div class="stack-item"><div class="s-label">Static Files</div><div class="s-val">WhiteNoise</div></div>
    <div class="stack-item"><div class="s-label">Server</div><div class="s-val">Gunicorn — preload</div></div>
    <div class="stack-item"><div class="s-label">Runtime</div><div class="s-val">Python 3.11.9</div></div>
  </div>
</section>

<!-- ══ FOOTER ══════════════════════════════════════ -->
<footer>
  <svg style="display:block;margin:0 auto 2rem;" width="40" height="48" viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg" opacity="0.4">
    <path d="M50 10 C50 10, 15 60, 15 78 C15 97, 31 110, 50 110 C69 110, 85 97, 85 78 C85 60, 50 10, 50 10 Z" fill="#C8102E"/>
  </svg>
  <p><strong>JeevanDaan+</strong> — Built to save lives.</p>
  <p>Every donation matters. Every request counts. Every life is worth the effort.</p>
  <p style="margin-top:1rem; font-size:0.75rem;">🇮🇳 Made in India</p>
</footer>

<script>
// Particles
const pCont = document.getElementById('particles');
for (let i = 0; i < 18; i++) {
  const p = document.createElement('div');
  p.className = 'particle';
  const sz = Math.random() * 4 + 2;
  p.style.cssText = `
    width:${sz}px; height:${sz}px;
    left:${Math.random()*100}%;
    animation-duration:${8+Math.random()*12}s;
    animation-delay:${Math.random()*10}s;
    opacity:0;
  `;
  pCont.appendChild(p);
}

// Glow blob follows mouse
document.addEventListener('mousemove', e => {
  const b = document.getElementById('blob');
  b.style.transform = `translate(${e.clientX - 300}px, ${e.clientY - 300}px)`;
});

// Typewriter
const phrases = [
  'Jeevan means life. Daan means gift.',
  'Real-time blood request matching.',
  'Geo-aware donor notifications.',
  'OTP-verified donations.',
  'A platform built for emergencies.',
];
let pi = 0, ci = 0, deleting = false;
const tw = document.getElementById('tw');
function type() {
  const phrase = phrases[pi];
  if (!deleting) {
    tw.textContent = phrase.slice(0, ++ci);
    if (ci === phrase.length) { deleting = true; setTimeout(type, 1800); return; }
  } else {
    tw.textContent = phrase.slice(0, --ci);
    if (ci === 0) { deleting = false; pi = (pi + 1) % phrases.length; }
  }
  setTimeout(type, deleting ? 35 : 60);
}
setTimeout(type, 1400);

// Scroll reveal
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal, .flow-step').forEach(el => observer.observe(el));
</script>
</body>
</html>
