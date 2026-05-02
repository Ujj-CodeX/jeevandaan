<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:8B0000,50:DC143C,100:FF6B6B&height=220&section=header&text=🩸%20JeevanDaan+&fontSize=60&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Connecting%20Blood%20Donors%20%7C%20Saving%20Lives&descAlignY=58&descColor=FFB3B3" />

</div>

<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=20&pause=1000&color=DC143C&center=true&vCenter=true&random=false&width=700&lines=🩸+Real-time+GPS+Blood+Donor+Discovery;📲+Automated+SMS+%26+WhatsApp+Notifications;🔐+JWT+Auth+%2B+Google+OAuth+%2B+Aadhaar+Encryption;⚡+45%2B+REST+API+Endpoints+%7C+8+Django+Apps;🤖+5+Automated+Cron+Jobs+%7C+Zero+Manual+Moderation)](https://git.io/typing-svg)

</div>

<div align="center">

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST-ff1709?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-35495e?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-DC143C?style=for-the-badge)](https://jeevandaan.vercel.app)
[![Backend API](https://img.shields.io/badge/⚡_Backend_API-092E20?style=for-the-badge)](https://jeevandaan-backend.onrender.com)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

</div>

---

## 📖 About

**JeevanDaan+** is a full-stack blood donation platform that connects blood donors with recipients in real time. Built with Django REST Framework and Vue.js, it uses GPS-based discovery, automated notifications, and smart scheduling to make blood donation seamless — zero manual intervention required.

> _"Jeevan" means Life | "Daan" means Donation — JeevanDaan+ is the gift of life._

---

## ✨ Key Features

### 🩸 Core Platform
- **Smart Donor Discovery** — Find donors within **10km** using GPS + geopy
- **Multi-Blood-Group Filtering** — A+, A-, B+, B-, AB+, AB-, O+, O-
- **Real-time Request Management** — Create, track & fulfill blood requests
- **Donation History** — Complete donor & recipient activity logs

### 🔔 Notification System
- **Twilio SMS** — Instant SMS alerts to nearby donors
- **WhatsApp Integration** — WhatsApp messages via Twilio API
- **Smart Targeting** — Only notifies donors within GPS range + matching blood group

### 🤖 Automation (5 Cron Jobs — APScheduler)
| Job | Description | Frequency |
|-----|-------------|-----------|
| 🔍 Donor Scanner | Auto-match donors to active requests | Every 10 min |
| 📲 Notification Sender | Send SMS/WhatsApp to eligible donors | Every 10 min |
| ⏰ Request Expiry | Auto-expire old unfulfilled requests | Daily |
| 🏆 Badge Updater | Update donor badges based on donations | Weekly |
| 📊 Stats Updater | Refresh platform-wide statistics | Daily |

### 🔐 Authentication & Security
- **JWT Authentication** — Access + Refresh tokens
- **Google OAuth** — Social login via django-allauth
- **Aadhaar Encryption** — AES-256 encrypted storage for sensitive data
- **Role-Based Access** — Donor, Recipient, Admin roles

---

## 🏗️ Architecture

```
JeevanDaan+
├── 🖥️  Frontend (Vue.js)          → Vercel
│   ├── Donor Dashboard
│   ├── Request Management
│   ├── Live Notifications
│   └── Profile & History
│
└── ⚙️  Backend (Django + DRF)     → Render
    ├── accounts/                  → Auth, JWT, Google OAuth
    ├── donors/                    → Donor profiles, GPS, badges
    ├── requests/                  → Blood request CRUD
    ├── notifications/             → Twilio SMS & WhatsApp
    ├── scheduler/                 → 5 APScheduler cron jobs
    ├── media/                     → Cloudinary image storage
    ├── analytics/                 → Platform stats & reports
    └── core/                      → Settings, URLs, middleware
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend Framework** | Django 4.x + Django REST Framework |
| **Database** | PostgreSQL (Supabase) |
| **Frontend** | Vue.js 3 + Vite |
| **Authentication** | JWT (SimpleJWT) + Google OAuth (django-allauth) |
| **Notifications** | Twilio SMS & WhatsApp API |
| **GPS/Location** | geopy + Haversine formula |
| **Task Scheduling** | APScheduler |
| **Media Storage** | Cloudinary |
| **Deployment** | Render (Backend) + Vercel (Frontend) |
| **Encryption** | AES-256 (Aadhaar data) |

---

## 📊 API Overview

> **45+ REST API Endpoints** across 8 Django apps

<details>
<summary>📋 Click to expand API endpoints</summary>

### 🔐 Auth Endpoints
```
POST   /api/auth/register/           → Register new user
POST   /api/auth/login/              → JWT login
POST   /api/auth/token/refresh/      → Refresh access token
POST   /api/auth/google/             → Google OAuth login
POST   /api/auth/logout/             → Logout
```

### 🩸 Donor Endpoints
```
GET    /api/donors/                  → List all donors
POST   /api/donors/register/         → Register as donor
GET    /api/donors/{id}/             → Donor profile
PUT    /api/donors/{id}/update/      → Update profile
GET    /api/donors/nearby/           → GPS-based nearby donors
GET    /api/donors/history/          → Donation history
```

### 📋 Request Endpoints
```
GET    /api/requests/                → List blood requests
POST   /api/requests/create/         → Create new request
GET    /api/requests/{id}/           → Request details
PUT    /api/requests/{id}/fulfill/   → Mark as fulfilled
DELETE /api/requests/{id}/cancel/    → Cancel request
GET    /api/requests/my/             → User's requests
```

### 📲 Notification Endpoints
```
GET    /api/notifications/           → User notifications
POST   /api/notifications/send/      → Trigger notification
PUT    /api/notifications/{id}/read/ → Mark as read
```

</details>

---

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.11+
PostgreSQL
Node.js 18+
```

### Backend Setup

```bash
# 1. Clone the repo
git clone https://github.com/Ujj-CodeX/jeevandaan.git
cd jeevandaan/backend/jeevandaan_backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Fill in your values in .env

# 5. Run migrations
python manage.py migrate

# 6. Start server
python manage.py runserver
```

### Frontend Setup

```bash
cd jeevandaan/frontend

npm install
npm run dev
```

---

## ⚙️ Environment Variables

Create a `.env` file in `backend/jeevandaan_backend/`:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Twilio
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
```

---

## 📸 Screenshots

| Dashboard | Donor Discovery | Request Management |
|-----------|----------------|-------------------|
| ![Dashboard](https://via.placeholder.com/250x150/DC143C/ffffff?text=Dashboard) | ![GPS Map](https://via.placeholder.com/250x150/092E20/ffffff?text=GPS+Map) | ![Requests](https://via.placeholder.com/250x150/316192/ffffff?text=Requests) |

> _Replace placeholders with actual screenshots_

---

## 🏆 Highlights

```python
stats = {
    "api_endpoints"     : "45+",
    "django_apps"       : 8,
    "cron_jobs"         : 5,
    "gps_radius_km"     : 10,
    "notification_types": ["SMS", "WhatsApp"],
    "auth_methods"      : ["JWT", "Google OAuth"],
    "encryption"        : "AES-256",
    "deployment"        : "Fully Live & Production Ready",
}
```

---

## 🗺️ Roadmap

- [ ] 🗺️ Live Map View — Real-time donor map (Leaflet.js)
- [ ] 📱 Mobile App — React Native / Flutter
- [ ] 🏥 Hospital Integration — Direct hospital request system
- [ ] 📊 Admin Dashboard — Analytics & moderation panel
- [ ] 🌍 Multi-city Support — Expand beyond 10km radius
- [ ] 🤖 AI Matching — Smart donor-recipient compatibility

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👨‍💻 Developer

<div align="center">

**Ujjawal Kumar Rauniyar**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/ujjawal-rauniyar)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ujj-CodeX)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ujjawalrauniyar2004@gmail.com)

_Python Backend Developer | Django · DRF · Flask · PostgreSQL_

</div>

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF6B6B,50:DC143C,100:8B0000&height=100&section=footer" />

**⭐ Star this repo if it helped you!**

_Made with ❤️ and lots of ☕ by Ujjawal_

</div>
