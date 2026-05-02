<div align="center">

<br/>

# 🩸 JeevanDaan+

### *Jeevan* means life. *Daan* means gift.

**A full-stack blood donation ecosystem** — connecting donors, blood banks, and hospitals across India with real-time geo-matching, verified identities, intelligent scheduling, and a reliability engine that rewards the selfless.

<br/>

[![Django](https://img.shields.io/badge/Django-5.1.7-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.17-red?style=flat-square)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.11.9-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Twilio](https://img.shields.io/badge/Twilio-F22F46?style=flat-square&logo=twilio&logoColor=white)](https://www.twilio.com/)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=flat-square&logo=cloudinary)](https://cloudinary.com/)

<br/>

</div>

---

## What is JeevanDaan+?

Every 2 seconds, someone in India needs blood. JeevanDaan+ is the backend infrastructure that bridges that gap.

Three types of users. One mission.

- A **Donor** registers, gets Aadhaar-verified, and receives geo-targeted SMS/WhatsApp alerts when nearby hospitals need their blood group.
- A **Partner** (hospital or blood bank) manages live stock, posts donation requests, runs donation camps, and verifies donations — all from one authenticated dashboard.
- An **Attender** (patient's family) raises a blood request that gets fulfilled either by a direct donor or through the inter-partner blood exchange network.

Everything is real. Every action has consequences.

---

## Core Features

### 👤 Donor System
Secure registration with bcrypt-hashed passwords, Aadhaar identity verification (one Aadhaar per account), JWT-based auth with short-lived access tokens, GPS location for proximity matching, and OTP-based password recovery over SMS.

### 🏥 Partner System
Hospital onboarding with License ID validation, admin-gated activation, live blood stock management per blood group, critical stock flagging (≤ 3 units), and partner profile management including fee structures.

### 🗺️ Geo-Matching Engine
A two-step spatial filter — a **bounding-box SQL pre-filter** trims the dataset, then **geodesic distance** via `geopy` gives precision. Finds nearby donors and nearby partners independently. Results are distance-sorted. Configurable radius, default 10km.

### 📋 Three Types of Blood Requests

| Request Type | Flow |
|---|---|
| **Attender Request** | Patient's family raises an open request visible to all verified partners |
| **Partner Donor Request** | Hospital pings nearby donors for direct walk-in donation |
| **Inter-Partner Request** | Hospital A requests blood from Hospital B when local stock is empty |

### 🔔 Notification Engine
SMS + WhatsApp via Twilio for every critical event. Fallback call queued if both channels fail. Proximity-based donor alerts fire the moment a new request is raised. All notifications run in **background threads** — they never block the HTTP response.

### 🏕️ Donation Camp System
Partners create and schedule blood donation camps. Donors within 20km are automatically notified. Donors can enroll. After the camp, the partner's dashboard **freezes** until stock is updated — enforcing accountability. Partners can download a full enrollment CSV on or after camp date.

### 🔐 OTP Donation Verification
When a donor accepts a request, a **unique 6-digit OTP** is generated and sent to the partner. The partner scans it at the time of donation. Donation history, scores, and member tags update atomically.

### 🏆 Donor Reliability Engine

| Event | Effect |
|---|---|
| Donation verified by bank | Score `+10`, member tag upgrade |
| Cancellation | Score `−10` |
| 3+ cancellations | Account locked for 30 days |
| Lock period ends | Auto-unlocked by scheduler |

Member tags climb from `New Member` → `Bronze` → `Silver` → `Gold` → `Platinum Donor` based on total verified donations.

### ⭐ Ratings & Complaints
Attenders rate hospitals post-fulfillment. Partners rate donors post-donation. Five or more complaints on a partner triggers **automatic deactivation**. Complaint categories include overcharging, exchange conditions, staff misbehavior, and fake stock listings.

### ⏰ Background Scheduler

Four APScheduler jobs run silently in the background:

- Expire pending attender requests → every 15 minutes
- Expire open donor requests → every 15 minutes
- Auto-unlock eligible donor accounts → every hour
- Expire assigned but unvisited requests → every 30 minutes

---

## Architecture

```
jeevandaan-plus/
│
├── config/              # Settings, JWT auth backends, permissions
├── users/               # Donor accounts, geo engine, scoring
├── partners/            # Hospital accounts, camps, inter-partner flows
├── requests_app/        # Full request lifecycle — attender, donor, inter-partner
├── stock/               # Blood units per partner × blood group
├── donations/           # Donation history, verification, leaderboard
├── notifications/       # Twilio SMS/WhatsApp dispatch + notification models
├── chat/                # Donor ↔ Partner in-request messaging
└── scheduler.py         # APScheduler job definitions
```

---

## Request Lifecycle

```
Partner posts open request
         │
         ▼
Nearby donors notified via SMS + WhatsApp (background)
         │
         ▼
Donor accepts → status: assigned → OTP generated & sent to partner
         │
         ├── Donor cancels → status: open again, score −10, lock check
         │
         ▼
Donor arrives → Partner verifies OTP
         │
         ▼
Partner calls verify → status: fulfilled
DonationHistory created → score +10 → member tag updated
         │
         ▼
Donor rates partner ⭐   Partner rates donor ⭐
```

---

## Security

- Passwords hashed with **bcrypt** — never stored in plain text
- JWT tokens are short-lived (1 hour) with 7-day refresh
- Aadhaar numbers are stored but **excluded from all serializer outputs**
- Donor identity is never exposed in public-facing responses
- Admin panel enforces **read-only** on all sensitive fields
- Partners cannot go live without **manual admin approval**
- Accounts **auto-lock** after repeated cancellations

---

## Tech Stack

| | |
|---|---|
| **Framework** | Django 5.1.7 + Django REST Framework 3.17 |
| **Auth** | PyJWT + bcrypt |
| **Database** | PostgreSQL via psycopg2 |
| **Media** | Cloudinary |
| **Notifications** | Twilio — SMS + WhatsApp |
| **Geo** | geopy — geodesic distance matching |
| **Scheduler** | APScheduler + django-apscheduler |
| **Static Files** | WhiteNoise |
| **Server** | Gunicorn |
| **Runtime** | Python 3.11.9 |

---

<div align="center">

<br/>

**Built to save lives. Every donation matters.**

*🇮🇳 Made in India*

</div>
