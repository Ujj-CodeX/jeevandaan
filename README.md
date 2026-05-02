<div align="center">

<img src="https://img.shields.io/badge/-%F0%9F%A9%B8%20JeevanDaan+-DC143C?style=for-the-badge&labelColor=8B0000&color=DC143C" height="60"/>

# JeevanDaan+

### *Jeevan* — life. *Daan* — gift. Together, a platform built to save both.

**A full-stack blood donation ecosystem** connecting donors, blood banks, and hospitals across India — with real-time location matching, verified identities, intelligent scheduling, and a reliability engine that rewards the selfless.

<br/>

[![Django](https://img.shields.io/badge/Django-5.1.7-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.17-red?style=flat-square)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.11.9-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-psycopg2-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT%20%2B%20bcrypt-000000?style=flat-square&logo=jsonwebtokens)](https://jwt.io/)
[![Twilio](https://img.shields.io/badge/Notifications-Twilio-F22F46?style=flat-square&logo=twilio&logoColor=white)](https://www.twilio.com/)
[![Cloudinary](https://img.shields.io/badge/Storage-Cloudinary-3448C5?style=flat-square&logo=cloudinary)](https://cloudinary.com/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

<br/>

[Features](#-features) · [Architecture](#-architecture) · [API Reference](#-api-reference) · [Getting Started](#-getting-started) · [Tech Stack](#-tech-stack)

---

</div>

## 🩸 What is JeevanDaan+?

Every 2 seconds, someone in India needs blood. JeevanDaan+ is the backend infrastructure that bridges that gap — a multi-role REST API that orchestrates **donors**, **blood banks (partners)**, and **attenders (patients' family members)** on a single platform.

- A **donor** registers, gets Aadhaar-verified, and receives geo-targeted SMS/WhatsApp alerts when nearby hospitals need their blood group.
- A **partner** (hospital or blood bank) manages live stock, posts donation requests, runs donation camps, and verifies donations — all from one authenticated dashboard.
- An **attender** raises a blood request on behalf of a patient, which is fulfilled either by a direct donor or through the inter-partner blood exchange network.

Everything is real. Every action has consequences — reliability scores, donor locks, automated expiry, and a leaderboard that celebrates the committed.

---

## ✨ Features

### 👤 Donor System
- Secure registration with **bcrypt-hashed passwords**
- **Aadhaar verification** — one Aadhaar per account, admin-verified
- **JWT authentication** with separate access (1hr) and refresh (7d) tokens
- GPS-based location updates for proximity matching
- **Forgot / Reset / Change Password** with OTP-over-SMS
- Profile updates with blood group management

### 🏥 Partner (Blood Bank / Hospital) System
- Hospital registration with License ID validation
- Admin-gated activation (`is_verified` + `is_live`)
- **Live blood stock management** — update units per blood group
- Critical stock alerts — stocks ≤ 3 units are flagged
- Partner profile editing (contact, facilities, fee structure)
- Location updates for geo-matching

### 📋 Request Management
| Request Type | Description |
|---|---|
| **Attender Request** | Patient's family raises an open blood request visible to all partners |
| **Partner Donor Request** | Hospital pings nearby donors for direct donation |
| **Inter-Partner Request** | Hospital A requests blood from Hospital B when local stock is empty |

### 🗺️ Geo-Matching Engine
- **Bounding-box SQL pre-filter** → then precise geodesic distance via `geopy`
- Configurable radius (default 10km, fallback 50km)
- Finds nearby donors AND nearby partners independently
- Distance-sorted results returned to the client

### 🔔 Notification Engine
- **SMS + WhatsApp** via Twilio for every critical event
- Fallback call queued if both channels fail
- Donor proximity notifications when a new blood request is raised
- Camp enrollment reminders
- Background threading — **notifications never block HTTP responses**

### 🏕️ Donation Camp System
- Partners create and schedule blood donation camps
- Donors near the camp receive automatic notifications
- Donor enrollment with blood group tracking
- **Dashboard freeze** until stock is updated post-camp
- CSV download of enrollments — available on/after camp date

### 🏆 Donor Reliability Engine
| Event | Score Impact |
|---|---|
| Donation verified by bank | `+10` |
| Cancellation | `-10` |
| 3+ cancellations | Account locked for 30 days |
| Auto-unlock | Scheduler runs hourly |

**Member Tags** auto-upgrade based on total donations:
`New Member` → `Bronze` → `Silver` → `Gold` → `Platinum Donor`

### ⭐ Rating & Complaint System
- Attenders rate partner hospitals post-fulfillment (1–5 stars)
- Partners rate donors after donation
- 5+ complaints on a partner → **automatic deactivation**
- Complaint types: overcharging, exchange conditions, misbehavior, fake stock

### 🔐 OTP-Based Donation Verification
- On donor acceptance, a **6-digit unique OTP** is generated
- OTP sent to the partner via notification
- Partner scans OTP at donation time — marks donation complete
- Donor score and donation history updated atomically

### ⏰ Background Scheduler (APScheduler)
| Job | Interval |
|---|---|
| Expire pending attender requests | Every 15 min |
| Expire open donor requests | Every 15 min |
| Unlock eligible donor accounts | Every hour |
| Expire unvisited assigned requests | Every 30 min |

---

## 🏗️ Architecture

```
jeevandaan-plus/
│
├── config/                  # Django settings, auth, permissions, WSGI
│   ├── authentication.py    # DonorJWT, PartnerJWT, AnyJWT backends
│   └── permissions.py       # IsDonor, IsPartner, IsAuthenticated
│
├── users/                   # Donor accounts
│   ├── models.py            # Donor model with geo, scoring, lock fields
│   ├── views.py             # Register, Login, Profile, Aadhaar, Password flows
│   ├── serializers.py
│   └── location.py          # Bounding-box + geodesic nearby engine
│
├── partners/                # Blood bank / hospital accounts
│   ├── models.py            # Partners, DonationCamp, CampEnrollment
│   ├── views.py             # Auth, camps, inter-partner flows
│   └── utils.py             # Dashboard freeze logic
│
├── requests_app/            # All request lifecycle management
│   ├── models.py            # AttenderRequest, PartnerDonorRequest, OTPCode, Ratings
│   └── views.py             # Full CRUD + accept/cancel/fulfill/OTP flows
│
├── stock/                   # Blood stock per partner
│   └── models.py            # Stock (partner × blood_group, unique together)
│
├── donations/               # Donation history & leaderboard
│   ├── models.py            # DonationHistory with score tracking
│   └── views.py             # Verify, history, leaderboard
│
├── notifications/           # Multi-channel notification system
│   ├── models.py            # Notification with type/trigger/status
│   ├── helpers.py           # notify_donor, notify_nearby_donors, notify_camp_donors
│   └── sms.py               # Twilio SMS + WhatsApp dispatch
│
├── chat/                    # Donor ↔ Partner in-request chat
│   ├── models.py            # Chat with predefined message choices
│   └── views.py             # Send + history, auth-aware
│
├── scheduler.py             # APScheduler job definitions
├── manage.py
├── requirements.txt
├── build.sh                 # pip install + collectstatic + migrate
└── start.sh                 # gunicorn with preload
```

---

## 🔑 Authentication

JeevanDaan+ uses a **dual-identity JWT system** — donors and partners are entirely separate entities with separate tokens.

```http
Authorization: Bearer <access_token>
```

| Middleware | Resolves To |
|---|---|
| `DonorJWTAuthentication` | `Donor` instance |
| `PartnerJWTAuthentication` | `Partners` instance |
| `AnyJWTAuthentication` | Either type |

Token payload:
```json
{
  "id": 42,
  "type": "donor",   // or "partner"
  "exp": 1234567890,
  "iat": 1234567890
}
```

---

## 📡 API Reference

### 🧑 Donors — `/api/users/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `register/` | ❌ | Create donor account |
| `POST` | `login/` | ❌ | Get JWT tokens |
| `GET` | `profile/` | ✅ Donor | View own profile |
| `PUT` | `update-profile/` | ✅ Donor | Update name, phone, blood group |
| `POST` | `update-location/` | ✅ Donor | Set GPS coordinates |
| `POST` | `verify-aadhaar/` | ✅ Donor | Submit Aadhaar for verification |
| `POST` | `forgot-password/` | ❌ | Send OTP to registered phone |
| `POST` | `reset-password/` | ❌ | Reset with OTP |
| `POST` | `change-password/` | ✅ Donor | Change while logged in |

### 🏥 Partners — `/api/partners/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `register/` | ❌ | Register blood bank |
| `POST` | `login/` | ❌ | Get partner JWT tokens |
| `GET/PUT` | `profile/` | ✅ Partner | View or update hospital profile |
| `POST` | `update-location/` | ✅ Partner | Set hospital GPS |
| `GET` | `list/` | ❌ | Public list of live partners |
| `GET` | `nearby/` | ❌ | Partners near coordinates |
| `GET` | `nearby-donors/` | ✅ Partner | Donors near hospital by blood group |

### 🩸 Blood Stock — `/api/stock/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `update/` | ✅ Partner | Add/update units for a blood group |
| `GET` | `partner/<id>/` | ❌ | View partner's full stock |
| `GET` | `critical/` | ❌ | Stocks with ≤ 3 units |
| `GET` | `search/?blood_group=A+&city=Mumbai` | ❌ | Search available stock |

### 📋 Requests — `/api/requests/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `attender/create/` | ✅ Donor | Raise a blood request for patient |
| `GET` | `attender/list/` | ❌ | Browse open attender requests |
| `GET` | `attender/<uuid>/` | ❌ | Request detail |
| `POST` | `attender/<uuid>/fulfill/` | ✅ Partner | Mark request fulfilled |
| `POST` | `attender/<uuid>/rate/` | ✅ Donor | Rate partner post-fulfillment |
| `GET` | `attender/my-requests/` | ✅ Donor | Own request history |
| `POST` | `donor/create/` | ✅ Partner | Post a donor recruitment request |
| `GET` | `donor/list/` | ✅ Any | Nearby open donation requests |
| `POST` | `donor/<id>/accept/` | ✅ Donor | Accept and get OTP |
| `POST` | `donor/<id>/cancel/` | ✅ Donor | Cancel (triggers score penalty) |
| `POST` | `donor/<id>/rate/` | ✅ Donor | Rate partner post-donation |
| `GET` | `otp/<request_id>/` | ✅ Partner | Fetch OTP for request |
| `POST` | `verify-otp/` | ✅ Partner | Confirm donor arrived |

### 🏕️ Donation Camps — `/api/partners/camps/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `create/` | ✅ Partner | Schedule a new camp |
| `GET` | `` | ✅ Partner | Own camps list |
| `GET` | `nearby/?lat=&lng=` | ❌ | Camps within 20km |
| `POST` | `<id>/notify/` | ✅ Partner | Notify nearby donors (background) |
| `POST` | `<id>/enroll/` | ✅ Donor | Enroll in camp |
| `GET` | `enrolled/` | ✅ Donor | My enrollments |
| `POST` | `<id>/update-stock/` | ✅ Partner | Mark stock updated post-camp |
| `GET` | `<id>/download/` | ✅ Partner | CSV of enrollments |

### 💬 Chat — `/api/chat/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `<request_id>/send/` | ✅ Any | Send a predefined message |
| `GET` | `<request_id>/history/` | ✅ Any | Full chat thread |

**Predefined messages:** `on_the_way` · `reached` · `unable_to_come` · `delayed` · `donated`

### 🔔 Notifications — `/api/notifications/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `donor/` | ✅ Donor | Donor's notification inbox |
| `GET` | `partner/` | ✅ Partner | Partner's notification inbox |
| `POST` | `<id>/read/` | ✅ Any | Mark as delivered |

### 🏆 Donations — `/api/donations/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `verify/<request_id>/` | ✅ Partner | Verify donation → update score + history |
| `GET` | `my-history/` | ✅ Donor | Personal donation history |
| `GET` | `partner-history/` | ✅ Partner | All donations received |
| `GET` | `leaderboard/` | ❌ | Top 10 donors (anonymous) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11.9
- PostgreSQL
- Redis (for Django cache — OTP storage)
- A Twilio account (SMS + WhatsApp)
- A Cloudinary account (media uploads)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/jeevandaan-plus.git
cd jeevandaan-plus

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your credentials

# 5. Run migrations
python manage.py migrate

# 6. Start development server
python manage.py runserver
```

### Environment Variables

```env
# Django
SECRET_KEY=your_super_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://user:password@localhost:5432/jeevandaan

# Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
TWILIO_WHATSAPP_NUMBER=+1XXXXXXXXXX

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Production Deployment (Render / Railway)

The project includes production-ready scripts:

```bash
# Build command
./build.sh
# → pip install -r requirements.txt
# → collectstatic
# → migrate

# Start command
./start.sh
# → gunicorn config.wsgi:application --workers 2 --timeout 120 --preload
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | Django 5.1.7 + Django REST Framework 3.17 |
| **Auth** | PyJWT 2.10 + bcrypt 5.0 |
| **Database** | PostgreSQL via psycopg2 + dj-database-url |
| **Media Storage** | Cloudinary |
| **Notifications** | Twilio (SMS + WhatsApp) |
| **Geo Engine** | geopy (geodesic distance) |
| **Scheduler** | APScheduler + django-apscheduler |
| **CORS** | django-cors-headers |
| **Static Files** | WhiteNoise |
| **Server** | Gunicorn |
| **Runtime** | Python 3.11.9 |

---

## 🔒 Security Highlights

- Passwords hashed with **bcrypt** (never stored in plain text)
- JWT tokens are **short-lived** (1 hour access) with 7-day refresh
- Aadhaar numbers stored **encrypted and hidden** from all serializers
- Donor identity is **never exposed** in public API responses
- Admin panel has **read-only** enforcement on all sensitive fields
- Partners cannot go live **without admin verification**
- Donor accounts **auto-lock** after 3 cancellations

---

## 🧪 Running Tests

```bash
python manage.py test
```

> Test suites live in each app's `tests.py`. Contributions welcome!

---

## 📊 Data Flow: Donor Request Lifecycle

```
Partner posts PartnerDonorRequest (status: open)
        │
        ▼
Scheduler / Notification → nearby donors via SMS/WhatsApp
        │
        ▼
Donor accepts → status: assigned, OTP generated & sent to partner
        │
        ├─ Donor cancels → status: open, score -10, lock check
        │
        ▼
Donor arrives → partner verifies OTP → donation confirmed
        │
        ▼
Partner calls VerifyDonation → status: fulfilled
DonationHistory created, score +10, member_tag updated
        │
        ▼
Donor rates partner ⭐  |  Partner rates donor ⭐
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes, then
git commit -m "feat: your descriptive message"
git push origin feature/your-feature-name
```

Please follow PEP8 and include tests for any new endpoints.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ to save lives.**

*Every donation matters. Every request counts. Every life is worth the effort.*

<br/>

[![Made in India](https://img.shields.io/badge/Made%20in-India%20🇮🇳-FF9933?style=flat-square)](https://en.wikipedia.org/wiki/India)
[![Blood Donation](https://img.shields.io/badge/For-Blood%20Donation%20🩸-DC143C?style=flat-square)]()

</div>
