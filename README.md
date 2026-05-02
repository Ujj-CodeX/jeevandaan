<div align="center">
  <img src="./header.svg" width="100%" alt="JeevanDaan+"/>
</div>

<div align="center">

[![Django](https://img.shields.io/badge/Django-5.1.7-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.17-C8102E?style=flat-square)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.11.9-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Twilio](https://img.shields.io/badge/Twilio-F22F46?style=flat-square&logo=twilio&logoColor=white)](https://www.twilio.com/)
[![JWT](https://img.shields.io/badge/JWT-black?style=flat-square&logo=jsonwebtokens)](https://jwt.io/)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=flat-square&logo=cloudinary)](https://cloudinary.com/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

</div>

<br/>

## What is JeevanDaan+?

Every 2 seconds, someone in India needs blood. JeevanDaan+ is the backend infrastructure that bridges that gap — a multi-role REST API connecting **donors**, **blood banks**, and **patients' families** on one platform, with real-time geo-matching, Aadhaar-verified identities, and a reliability engine that rewards the selfless.

<br/>

## Who Uses It

| Role | What They Do |
|---|---|
| 🧑 **Donor** | Registers, gets Aadhaar-verified, receives geo-targeted SMS/WhatsApp alerts when a nearby hospital needs their blood group |
| 🏥 **Partner** | Hospital or blood bank — manages live stock, posts donation requests, runs camps, verifies donations |
| 🤝 **Attender** | Patient's family — raises a blood request fulfilled by a direct donor or via inter-partner exchange |

<br/>

## Core Features

**📍 Geo-Matching Engine**
Bounding-box SQL pre-filter trims the candidate set first, then geodesic distance via `geopy` gives precision. Finds nearby donors and partners independently. Distance-sorted, 10km default radius, fully configurable.

**🔔 Multi-Channel Notification Engine**
SMS + WhatsApp via Twilio on every critical event. Fallback call queued if both channels fail. All notifications run in **background threads** — they never block the HTTP response.

**🔐 OTP Donation Verification**
On donor acceptance a unique 6-digit OTP is generated and delivered to the partner. Scanned at donation time. Donation history, scores, and member tags update atomically.

**🏕️ Donation Camp System**
Partners schedule camps, donors within 20km are auto-notified. Dashboard **freezes** post-camp until stock is updated — enforcing accountability. CSV enrollment download on camp date.

**🔄 Inter-Partner Blood Exchange**
Hospital A has no stock? The system finds the nearest Hospital B within 20km with available units and auto-raises a transfer request between them.

**⏰ Background Scheduler**
Four APScheduler jobs run silently — expires stale requests every 15 min, auto-unlocks accounts every hour, cleans unvisited assignments every 30 min.

<br/>

## Donor Reliability Engine

| Event | Effect |
|---|---|
| Donation verified by bank | `+10` score |
| Cancellation | `−10` score |
| 3+ cancellations | Account locked 30 days |
| Lock period ends | Auto-unlocked by scheduler |
| 2+ donations | 🥉 Bronze Donor |
| 5+ donations | 🥇 Gold Donor |
| 10+ donations | 💎 Platinum Donor |

<br/>

## Request Lifecycle

```
Partner posts open request
        │
        ▼
Nearby donors notified via SMS + WhatsApp  ← background thread
        │
        ▼
Donor accepts → status: assigned → OTP generated & sent to partner
        │
        ├── Donor cancels → status: open again, score −10, lock check
        │
        ▼
Donor arrives → Partner scans OTP → arrival confirmed
        │
        ▼
Partner verifies donation → status: fulfilled
DonationHistory created → score +10 → member tag upgraded
        │
        ▼
Donor rates partner ⭐  |  Partner rates donor ⭐
```

<br/>

## Architecture

```
jeevandaan-plus/
├── config/              # Settings, JWT auth backends, permissions
├── users/               # Donor accounts, geo engine, scoring
├── partners/            # Hospital accounts, camps, inter-partner flows
├── requests_app/        # Full request lifecycle management
├── stock/               # Blood units per partner × blood group
├── donations/           # Donation history, verification, leaderboard
├── notifications/       # Twilio dispatch + notification models
├── chat/                # Donor ↔ Partner in-request messaging
└── scheduler.py         # APScheduler job definitions
```

<br/>

## Security

- Passwords hashed with **bcrypt** — never stored in plain text
- JWT tokens are short-lived (1 hour access, 7-day refresh)
- Donor and partner are **completely separate identity systems**
- Aadhaar numbers excluded from **all serializer outputs**
- Admin panel is **fully read-only** on sensitive fields
- Partners cannot go live without **manual admin approval**
- Accounts **auto-lock** after 3 cancellations

<br/>

## Tech Stack

| | |
|---|---|
| **Framework** | Django 5.1.7 + Django REST Framework 3.17 |
| **Auth** | PyJWT + bcrypt |
| **Database** | PostgreSQL via psycopg2 |
| **Media** | Cloudinary |
| **Notifications** | Twilio — SMS + WhatsApp |
| **Geo Engine** | geopy — geodesic distance matching |
| **Scheduler** | APScheduler + django-apscheduler |
| **Static Files** | WhiteNoise |
| **Server** | Gunicorn with preload |
| **Runtime** | Python 3.11.9 |

<br/>

<div align="center">

**Built to save lives. Every donation matters.**

*🇮🇳 Made in India*

</div>
