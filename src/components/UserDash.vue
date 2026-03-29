
    <style>

    .partner-row {
    transition: all 0.2s ease;
    border-radius: 12px;
    padding: 10px !important;
}
.partner-row:hover {
    background: #fff5f5 !important;
    transform: translateX(4px);
}
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    padding: 20px;
}
.registration-card {
    background: white;
    width: 100%;
    border-radius: 30px;
    position: relative;
    border-top: 6px solid #E63946;
    max-height: 90vh;
    overflow-y: auto;
}
        /* PARTNER REQUESTS CENTER SPECIFIC */
.request-count-badge {
    background: var(--jd-red);
    color: white;
    font-size: 0.75rem;
    padding: 2px 8px;
    border-radius: 50px;
    vertical-align: middle;
}

.partner-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    transition: transform 0.2s ease;
    border: 2px solid var(--jd-soft-red);
}

.partner-avatar:hover {
    transform: scale(1.1);
}

/* Side Panel / Right Modal */
.offcanvas {
    border-top-left-radius: 30px;
    border-bottom-left-radius: 30px;
    border: none;
    box-shadow: -10px 0 40px rgba(0,0,0,0.1);
}

.map-placeholder {
    height: 150px;
    background: #e9ecef;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #adb5bd;
    background-image: url('https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?auto=format&fit=crop&q=80&w=400');
    background-size: cover;
}

.priority-emergency { background-color: #ffeded; color: #e63946; border: 1px solid #ffcfcf; }
.priority-high { background-color: #fff4e5; color: #f39c12; border: 1px solid #ffe8cc; }

@media (max-width: 768px) {
    .offcanvas {
        border-radius: 30px 30px 0 0 !important;
        height: 80% !important;
        width: 100% !important;
    }
}
        :root {
            --jd-red: #E63946;
            --jd-dark-red: #C1121F;
            --jd-soft-red: #fff5f5;
            --jd-gray: #f8f9fa;
            --jd-border-radius: 20px;
        }

        body {
            background-color: #fcfcfc;
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #2d3436;
        }

        /* NAVBAR */
        .navbar { background: white; border-bottom: 1px solid #eee; padding: 15px 0; }
        .nav-link { font-weight: 500; color: #636e72 !important; margin: 0 10px; }
        .nav-link:hover, .nav-link.active { color: var(--jd-red) !important; }
        .nav-icon { font-size: 1.2rem; color: #636e72; position: relative; }
        .notification-dot {
            position: absolute; top: 0; right: 0; width: 8px; height: 8px;
            background: var(--jd-red); border-radius: 50%; border: 2px solid white;
        }

        /* CARDS */
        .jd-card {
            background: white; border: none; border-radius: var(--jd-border-radius);
            box-shadow: 0 10px 30px rgba(0,0,0,0.03); transition: transform 0.3s ease;
            margin-bottom: 24px;
        }
        .jd-card:hover { transform: translateY(-5px); }

        /* HEADER & BADGES */
        .donor-badge {
            background: linear-gradient(135deg, #ffd700, #ffae00);
            color: white; padding: 5px 15px; border-radius: 50px; font-weight: 600; font-size: 0.8rem;
        }

        /* STAT CARDS */
        .stat-card { padding: 25px; text-align: center; }
        .stat-icon { 
            width: 50px; height: 50px; background: var(--jd-soft-red); 
            color: var(--jd-red); border-radius: 15px; display: flex;
            align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 1.5rem;
        }

        /* CALENDAR UI */
        .calendar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .pill-toggle { background: var(--jd-gray); border-radius: 50px; padding: 5px; display: inline-flex; }
        .pill-btn { border: none; background: none; padding: 6px 18px; border-radius: 50px; font-size: 0.85rem; transition: 0.3s; }
        .pill-btn.active { background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.05); color: var(--jd-red); font-weight: 600; }

        .calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; }
        .day-cell { height: 60px; display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: 12px; font-size: 0.9rem; position: relative; }
        .day-cell.active-camp::after {
            content: ''; width: 6px; height: 6px; background: var(--jd-red); 
            border-radius: 50%; position: absolute; bottom: 10px;
        }
        .day-cell:hover { background: var(--jd-soft-red); cursor: pointer; }

        /* SLIDER (NETFLIX STYLE) */
        .camp-slider { display: flex; overflow-x: auto; gap: 20px; padding-bottom: 15px; scrollbar-width: none; }
        .camp-slider::-webkit-scrollbar { display: none; }
        .camp-card { min-width: 280px; background: white; border-radius: 18px; overflow: hidden; border: 1px solid #f0f0f0; }
        .camp-img { height: 140px; background-size: cover; background-position: center; }

        /* EMERGENCY REQUEST */
        .emergency-banner {
            background: linear-gradient(135deg, var(--jd-red), var(--jd-dark-red));
            color: white; border-radius: var(--jd-border-radius); padding: 30px;
        }

        /* ELIGIBILITY CIRCLE */
        .eligibility-check {
            border: 4px solid #00b894; width: 100px; height: 100px; 
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-size: 2rem; color: #00b894; margin: 0 auto 15px;
        }
    </style>



<template>
  <div>
    <nav class="navbar navbar-expand-lg sticky-top">
      <div class="container">
        <img 
    src="@/assets/L1.png" 
    alt="JeevanDaan Logo" 
    width="32" 
    height="32" 
    class="me-2 d-inline-block align-top logo-icon"
  >
        <a class="navbar-brand fw-bold text-danger" href="#">JeevanDaan<span class="text-dark">+</span></a>
        <button class="navbar-toggler border-0 shadow-none" type="button" data-bs-toggle="collapse" data-bs-target="#dashboardNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="dashboardNav">
          <ul class="navbar-nav mx-auto">
            <li class="nav-item"><RouterLink class="nav-link active" to="/">Home</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/user_request">Raise a Request</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/profile">Profile Settings</RouterLink></li>
            <li class="nav-item"><a class="nav-link" href="#" @click.prevent="logout">Logout</a></li>
          </ul>
          <div class="d-flex align-items-center gap-4">
            <a href="#" class="nav-icon"><i class="fa-regular fa-bell"></i><span class="notification-dot"></span></a>
            <a href="#" class="nav-icon"><i class="fa-regular fa-circle-user"></i></a>
          </div>
        </div>
      </div>
    </nav>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-danger" role="status"></div>
      <p class="mt-3 text-muted">Loading your dashboard...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="container py-5 text-center">
      <i class="fa-solid fa-triangle-exclamation text-danger fs-1 mb-3"></i>
      <p class="text-danger">{{ error }}</p>
      <button class="btn btn-danger rounded-pill px-4" @click="fetchProfile">Retry</button>
    </div>

    <div v-else class="container py-4">

      <!-- Header — FROM API -->
      <header class="row align-items-center mb-5">
        <div class="col-md-8">
          <h2 class="fw-bold mb-1">Hi, {{ donor.name }} 👋</h2>
          <p class="text-muted">
            Your Lifesaver Dashboard |
            <span class="text-danger fw-medium">Every donation saves a life.</span>
          </p>
        </div>
        <div class="col-md-4 text-md-end">
          <!-- member_tag FROM API -->
          <span class="donor-badge shadow-sm">
            <i class="fa-solid fa-crown me-2"></i>{{ donor.member_tag }}
          </span>
        </div>
      </header>

      <!-- Stat Cards — FROM API -->
      <div class="row g-4 mb-2">
        <div class="col-6 col-lg-3">
          <div class="jd-card stat-card">
            <div class="stat-icon"><i class="fa-solid fa-droplet"></i></div>
            <h6 class="text-muted small mb-1">Blood Group</h6>
            <p class="fw-bold mb-0">{{ donor.blood_group }}</p>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="jd-card stat-card">
            <div class="stat-icon"><i class="fa-solid fa-droplet"></i></div>
            <h6 class="text-muted small mb-1">Total Donations</h6>
            <p class="fw-bold mb-0">{{ donor.total_donations }} Units</p>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="jd-card stat-card">
            <div class="stat-icon"><i class="fa-solid fa-heart-pulse"></i></div>
            <h6 class="text-muted small mb-1">Lives Impacted</h6>
            <!-- Each donation saves ~3 lives -->
            <p class="fw-bold mb-0">{{ donor.total_donations * 3 }} People</p>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="jd-card stat-card">
            <div class="stat-icon"><i class="fa-solid fa-shield-check"></i></div>
            <h6 class="text-muted small mb-1">Reliability</h6>
            <p class="fw-bold mb-0 text-success">{{ donor.reliability_score }} Score</p>
          </div>
        </div>
      </div>


      <div class="emergency-banner mb-5 text-center shadow-lg">
        <h3 class="fw-bold">In Need of Blood?</h3>
        <p class="mb-4">Raise a verified emergency request to reach 25,000+ donors instantly.</p>
        <router-link to="/user_request" class="btn btn-light btn-lg rounded-pill px-5 fw-bold text-danger">Start Emergency Request</router-link>
      </div>

      <div class="row">
        <div class="col-lg-8">

          <div class="mt-5 mb-4">

            <div class="jd-card p-4">
    <h5 class="fw-bold mb-3">Verified Partner Banks Nearby</h5>

    <!-- Loading -->
    <div v-if="partnersLoading" class="text-center py-3">
        <div class="spinner-border spinner-border-sm text-danger"></div>
        <span class="ms-2 text-muted small">Finding nearby banks...</span>
    </div>

    <!-- Empty -->
    <div v-else-if="nearbyPartners.length === 0" class="text-center py-3">
        <i class="fa-solid fa-hospital-slash text-danger mb-2" style="font-size:2rem"></i>
        <p class="text-muted small mb-0">No verified partners found near you.</p>
    </div>

    <!-- List -->
    <div v-else class="list-group list-group-flush">
        <div
            v-for="partner in nearbyPartners"
            :key="partner.id"
            class="list-group-item d-flex justify-content-between align-items-center px-0 py-3 bg-transparent partner-row"
            @click="openPartnerDetail(partner)"
            style="cursor:pointer"
        >
            <div>
                <p class="mb-0 fw-bold">{{ partner.hospital_name }}</p>
                <small class="text-muted">
                    {{ partner.partner_type === 'blood_bank' ? 'Blood Bank' : partner.partner_type === 'government' ? 'Govt Partner' : 'Private Partner' }}
                    • {{ partner.distance_km }} km away
                </small>
            </div>
            <div class="d-flex align-items-center gap-2">
                <span :class="['badge rounded-pill', getStockBadge(partner)]">
                    {{ getStockLabel(partner) }}
                </span>
                <i class="fa-solid fa-chevron-right text-muted small"></i>
            </div>
        </div>
    </div>
</div>
  <div class="d-flex justify-content-between align-items-end mb-3">
    <div>
      <h5 class="fw-bold mb-0">
        Pending Partner Requests
        <span class="request-count-badge ms-2">{{ partnerRequests?.length || 0 }} Pending</span>
      </h5>
      <p class="text-muted small mb-0">Requests raised by hospitals & partner organizations</p>
    </div>
    <div class="pill-toggle d-none d-md-flex">
      <button class="pill-btn active">All</button>
      <button class="pill-btn">Emergency</button>
      <button class="pill-btn">Normal</button>
    </div>
  </div>

  <!-- LOADING -->
  <div v-if="requestsLoading" class="text-center py-4">
    <div class="spinner-border spinner-border-sm text-danger"></div>
    <span class="ms-2 text-muted small">Loading requests...</span>
  </div>

  <!-- ✅ EMPTY STATE -->
  <div v-else-if="partnerRequests.length === 0" class="jd-card p-5 text-center">
    <i class="fa-solid fa-heart-crack text-danger mb-3" style="font-size: 2.5rem;"></i>
    <h6 class="fw-bold mb-1">No Pending Requests Right Now</h6>
    <p class="text-muted small mb-0">
      There are currently no open blood requests matching your profile.<br>
      Check back soon — every minute counts! 🩸
    </p>
  </div>

  <!-- REQUEST CARDS -->
  <div v-else class="row g-3">
    <div
      class="col-md-6 col-lg-4"
      v-for="req in partnerRequests"
      :key="req.id"
    >
      <div class="jd-card p-3 h-100">
        <div class="d-flex align-items-center gap-2 mb-3">
          <img
            :src="`https://ui-avatars.com/api/?name=${encodeURIComponent(req.hospital_name)}&background=E63946&color=fff`"
            class="partner-avatar"
            :alt="req.hospital_name"
          >
          <div>
            <h6 class="fw-bold mb-0">{{ req.hospital_name }}</h6>
            <span class="text-muted" style="font-size: 0.7rem;">
              {{ timeAgo(req.created_at) }}
            </span>
          </div>
        </div>
        <div class="mb-3">
          <p class="small text-muted mb-2">
            <i class="fa-solid fa-location-dot me-2 text-danger"></i>
            {{ req.city }}
          </p>
          <div class="d-flex flex-wrap gap-2">
            <span
              class="badge rounded-pill"
              :class="isExpiringSoon(req.expires_at) ? 'priority-emergency' : 'priority-high'"
            >
              {{ isExpiringSoon(req.expires_at) ? 'Urgent' : 'Normal' }}
            </span>
            <span class="badge rounded-pill bg-light text-dark border">
              {{ req.quantity }} Units • {{ req.blood_group }}
            </span>
            <span class="badge rounded-pill bg-light text-dark border">
              Expires: {{ formatDate(req.expires_at) }}
            </span>
          </div>
        </div>
        <div class="d-flex gap-2">
          <button class="btn btn-danger btn-sm rounded-pill flex-grow-1 py-2">Accept</button>
          <button class="btn btn-light btn-sm rounded-pill flex-grow-1 py-2 border">Decline</button>
        </div>
      </div>
    </div>
  </div>

</div>


          <!-- Calendar — HARDCODED (kept as is) -->
          <div class="jd-card p-4">
            <div class="calendar-header">
              <h5 class="fw-bold mb-0">Donation Camp Calendar</h5>
              <div class="pill-toggle">
                <button class="pill-btn active">Month</button>
                <button class="pill-btn">Week</button>
                <button class="pill-btn">List</button>
              </div>
            </div>
            <div class="calendar-grid text-center mb-3">
              <div class="text-muted small fw-bold">Mon</div><div class="text-muted small fw-bold">Tue</div><div class="text-muted small fw-bold">Wed</div><div class="text-muted small fw-bold">Thu</div><div class="text-muted small fw-bold">Fri</div><div class="text-muted small fw-bold">Sat</div><div class="text-muted small fw-bold">Sun</div>
              <div class="day-cell text-muted">28</div><div class="day-cell text-muted">29</div><div class="day-cell text-muted">30</div><div class="day-cell">1</div><div class="day-cell active-camp">2</div><div class="day-cell">3</div><div class="day-cell">4</div>
              <div class="day-cell">5</div><div class="day-cell active-camp">6</div><div class="day-cell">7</div><div class="day-cell">8</div><div class="day-cell">9</div><div class="day-cell active-camp">10</div><div class="day-cell">11</div>
            </div>
            <div class="p-3 bg-light rounded-4 d-flex justify-content-between align-items-center">
              <div>
                <span class="badge bg-danger rounded-pill mb-1">Recommended for You</span>
                <p class="mb-0 fw-bold">Mega Drive - Apollo Hospital</p>
                <small class="text-muted">10 Oct | 5.2 km away | Whole Blood & Platelets</small>
              </div>
              <button class="btn btn-danger btn-sm rounded-pill px-4">Register Slot</button>
            </div>
          </div>

          <!-- Nearby Camps — HARDCODED (kept as is) -->
          <h5 class="fw-bold mb-3 mt-4">Discover Nearby Camps</h5>
          <div class="camp-slider mb-4">
            <div class="camp-card shadow-sm">
              <div class="camp-img" style="background-image: url('https://images.unsplash.com/photo-1615461066841-6116e61058f4?auto=format&fit=crop&q=80&w=600');"></div>
              <div class="p-3">
                <span class="text-muted small fw-bold">RED CROSS SOCIETY</span>
                <h6 class="fw-bold mb-2">Corporate Drive, Sector 62</h6>
                <button class="btn btn-outline-danger btn-sm w-100 rounded-pill">Enroll Now</button>
              </div>
            </div>
            <div class="camp-card shadow-sm">
              <div class="camp-img" style="background-image: url('https://images.unsplash.com/photo-1579152276502-545a248a6a61?auto=format&fit=crop&q=80&w=600');"></div>
              <div class="p-3">
                <span class="text-muted small fw-bold">GOVT HOSPITAL</span>
                <h6 class="fw-bold mb-2">Weekend Rural Outreach</h6>
                <button class="btn btn-outline-danger btn-sm w-100 rounded-pill">Enroll Now</button>
              </div>
            </div>
          </div>

          <!-- Partner Banks — HARDCODED (kept as is) -->
          <!-- Verified Partner Banks — FROM API -->

</div>  

        <div class="col-lg-4">
        
          <div class="jd-card p-4">
            <h5 class="fw-bold mb-3">My Profile</h5>
            <div class="d-flex align-items-center gap-3 mb-3">
              <div class="stat-icon" style="width:55px;height:55px;font-size:1.4rem;flex-shrink:0;">
                <i class="fa-solid fa-user"></i>
              </div>
              <div>
                <p class="fw-bold mb-0">{{ donor.name }}</p>
                <small class="text-muted">@{{ donor.username }}</small>
              </div>
            </div>
            <div class="p-3 bg-light rounded-4">
              <div class="d-flex justify-content-between py-1 border-bottom">
                <small class="text-muted">Email</small>
                <small class="fw-bold">{{ donor.email }}</small>
              </div>
              <div class="d-flex justify-content-between py-1 border-bottom">
                <small class="text-muted">Phone</small>
                <small class="fw-bold">{{ donor.phone_number || 'Not set' }}</small>
              </div>
              <div class="d-flex justify-content-between py-1 border-bottom">
                <small class="text-muted">Blood Group</small>
                <small class="fw-bold text-danger">{{ donor.blood_group }}</small>
              </div>
              <div class="d-flex justify-content-between py-1 border-bottom">
                <small class="text-muted">Address</small>
                <small class="fw-bold">{{ donor.address || 'Not set' }}</small>
              </div>
              <div class="d-flex justify-content-between py-1">
                <small class="text-muted">Requests Raised</small>
                <small class="fw-bold">{{ donor.total_requests_raised }}</small>
              </div>
            </div>
          </div>

          
          <div class="jd-card p-4 text-center">
            <h5 class="fw-bold mb-3">Eligibility Status</h5>
            <div class="eligibility-check shadow-sm">
              <i class="fa-solid fa-check"></i>
            </div>
            <p class="fw-bold mb-1">Ready to Donate!</p>
            <p class="small text-muted mb-3">
              Reliability Score: <strong class="text-success">{{ donor.reliability_score }}</strong> |
              Aadhaar Verified: <strong>{{ donor.is_aadhaar_verified ? '✅' : '❌' }}</strong>
            </p>
            
          </div>

          <!-- Achievements — HARDCODED (kept as is) -->
          <div class="jd-card p-4">
    <h5 class="fw-bold mb-3">Achievements</h5>
    <div class="d-flex flex-wrap gap-3 justify-content-center">

        <!-- Hero — 0 to 20 donations -->
        <div class="text-center" style="width:70px">
            <img
                src="https://cdn-icons-png.flaticon.com/512/3112/3112946.png"
                class="img-fluid mb-1"
                :class="donor.total_donations >= 1 ? 'opacity-100' : 'opacity-25'"
                alt="Hero"
            >
            <small class="d-block fw-bold" :class="donor.total_donations >= 1 ? 'text-danger' : 'text-muted'">
                Hero
            </small>
            <small class="text-muted" style="font-size:0.65rem">1+ donations</small>
        </div>

        <!-- Reliable — reliability score > 60 -->
        <div class="text-center" style="width:70px">
            <img
                src="https://cdn-icons-png.flaticon.com/512/1828/1828640.png"
                class="img-fluid mb-1"
                :class="donor.reliability_score >= 60 ? 'opacity-100' : 'opacity-25'"
                alt="Reliable"
            >
            <small class="d-block fw-bold" :class="donor.reliability_score >= 60 ? 'text-warning' : 'text-muted'">
                Reliable
            </small>
            <small class="text-muted" style="font-size:0.65rem">Score 60+</small>
        </div>

        <!-- Fast Helper — 5+ donations -->
        <div class="text-center" style="width:70px">
            <img
                src="https://cdn-icons-png.flaticon.com/512/2583/2583434.png"
                class="img-fluid mb-1"
                :class="donor.total_donations >= 5 ? 'opacity-100' : 'opacity-25'"
                alt="Fast Help"
            >
            <small class="d-block fw-bold" :class="donor.total_donations >= 5 ? 'text-info' : 'text-muted'">
                Fast Help
            </small>
            <small class="text-muted" style="font-size:0.65rem">5+ donations</small>
        </div>

        <!-- Aadhaar Verified -->
        <div class="text-center" style="width:70px">
            <img
                src="https://cdn-icons-png.flaticon.com/512/6941/6941697.png"
                class="img-fluid mb-1"
                :class="donor.is_aadhaar_verified ? 'opacity-100' : 'opacity-25'"
                alt="Verified"
            >
            <small class="d-block fw-bold" :class="donor.is_aadhaar_verified ? 'text-success' : 'text-muted'">
                Verified
            </small>
            <small class="text-muted" style="font-size:0.65rem">Aadhaar done</small>
        </div>

        <!-- Platinum — 10+ donations -->
        <div class="text-center" style="width:70px">
            <img
                src="https://cdn-icons-png.flaticon.com/512/2583/2583454.png"
                class="img-fluid mb-1"
                :class="donor.total_donations >= 10 ? 'opacity-100' : 'opacity-25'"
                alt="Platinum"
            >
            <small class="d-block fw-bold" :class="donor.total_donations >= 10 ? 'text-danger' : 'text-muted'">
                Platinum
            </small>
            <small class="text-muted" style="font-size:0.65rem">10+ donations</small>
        </div>

    </div>

    
    <div class="mt-3 p-3 bg-light rounded-4 text-center">
        <small class="text-muted">
            Reliability Score:
            <strong :class="donor.reliability_score >= 80 ? 'text-success' : donor.reliability_score >= 50 ? 'text-warning' : 'text-danger'">
                {{ donor.reliability_score }}/100
            </strong>
            — Keep donating to unlock more badges! 🏆
        </small>
    </div>
</div>
        </div>
      </div>

    
      
    </div>

    <!-- Partner Detail Modal -->
<div v-if="selectedPartner" class="modal-overlay" @click.self="selectedPartner = null">
    <div class="registration-card shadow-lg" style="max-width:500px">
        <button class="close-btn" @click="selectedPartner = null">
            <i class="fas fa-times"></i>
        </button>

        <div class="card-body p-4">
            <!-- Header -->
            <div class="d-flex align-items-center gap-3 mb-4">
                <div class="stat-icon" style="width:55px;height:55px;font-size:1.4rem;flex-shrink:0">
                    <i class="fa-solid fa-hospital"></i>
                </div>
                <div>
                    <h5 class="fw-bold mb-0">{{ selectedPartner.hospital_name }}</h5>
                    <small class="text-muted">{{ selectedPartner.partner_type }}</small>
                    <span class="badge bg-success ms-2 rounded-pill small">Verified ✓</span>
                </div>
            </div>

            <!-- Details -->
            <div class="p-3 bg-light rounded-4 mb-3">
                <div class="d-flex justify-content-between py-2 border-bottom">
                    <small class="text-muted"><i class="fa-solid fa-location-dot me-2 text-danger"></i>Address</small>
                    <small class="fw-bold text-end" style="max-width:200px">{{ selectedPartner.address }}</small>
                </div>
                <div class="d-flex justify-content-between py-2 border-bottom">
                    <small class="text-muted"><i class="fa-solid fa-city me-2 text-danger"></i>City</small>
                    <small class="fw-bold">{{ selectedPartner.city }}, {{ selectedPartner.state }}</small>
                </div>
                <div class="d-flex justify-content-between py-2 border-bottom">
                    <small class="text-muted"><i class="fa-solid fa-phone me-2 text-danger"></i>Contact</small>
                    <small class="fw-bold">{{ selectedPartner.contact }}</small>
                </div>
                <div class="d-flex justify-content-between py-2 border-bottom">
                    <small class="text-muted"><i class="fa-solid fa-route me-2 text-danger"></i>Distance</small>
                    <small class="fw-bold text-danger">{{ selectedPartner.distance_km }} km away</small>
                </div>
                <div class="d-flex justify-content-between py-2 border-bottom">
                    <small class="text-muted"><i class="fa-solid fa-indian-rupee-sign me-2 text-danger"></i>Convenience Fee</small>
                    <small class="fw-bold">₹{{ selectedPartner.convenience_fee || '0' }}</small>
                </div>
                <div class="d-flex justify-content-between py-2">
                    <small class="text-muted"><i class="fa-solid fa-notes-medical me-2 text-danger"></i>Facility</small>
                    <small class="fw-bold text-end" style="max-width:200px">{{ selectedPartner.facility || 'N/A' }}</small>
                </div>
            </div>

            <!-- Stock availability -->
            <div class="mb-4">
                <p class="fw-bold small mb-2">Blood Stock Status:</p>
                <div class="d-flex flex-wrap gap-2">
                    <span
                        v-for="(qty, group) in selectedPartner.stock_summary"
                        :key="group"
                        :class="['badge rounded-pill px-3 py-2', qty > 5 ? 'bg-success' : qty > 0 ? 'bg-warning text-dark' : 'bg-danger']"
                    >
                        {{ group }}: {{ qty }} units
                    </span>
                    <span v-if="!selectedPartner.stock_summary" class="text-muted small">
                        Stock info not available
                    </span>
                </div>
            </div>

            <!-- Buttons -->
            <router-link to="/user_request" class="btn btn-danger w-100 py-3 fw-bold rounded-4 mb-2">
                <i class="fa-solid fa-file-medical me-2"></i> Raise Request Here
            </router-link>
            <button class="btn btn-light w-100 py-2 rounded-4" @click="selectedPartner = null">
                Close
            </button>
        </div>
    </div>
</div>



  </div>
</template>

<script>
import api from '@/api/index.js'
export default {
  name: 'Dashboard',

  data() {
    return {
      donor: {},
      loading: true,
      error: null,
      partnerRequests: [],
      requestsLoading: true,
      nearbyPartners: [],
partnersLoading: false,
selectedPartner: null,
    }
  },
  mounted() {
  this.fetchProfile()
  this.saveGPSLocation()
},

  methods: {
    async fetchNearbyPartners() {
    this.partnersLoading = true
    try {
        const coords = await this.getCoordinates()
        const lat = coords?.lat || ''
        const lng = coords?.lon || ''

        const url = `http://localhost:8000/api/partners/nearby/?lat=${lat}&lng=${lng}&radius=20`
        const response = await fetch(url)
        const data = await response.json()
        this.nearbyPartners = Array.isArray(data) ? data : []
    } catch (err) {
        this.nearbyPartners = []
        console.error(err)
    } finally {
        this.partnersLoading = false
    }
},
// In Dashboard.vue — mounted() or after login
async saveGPSLocation() {
    if (!navigator.geolocation) return

    navigator.geolocation.getCurrentPosition(
        async (pos) => {
            try {
                await api.put('/api/users/profile/', {
                    latitude: pos.coords.latitude,
                    longitude: pos.coords.longitude
                })
                console.log('GPS location saved ✅')
            } catch (err) {
                console.error('Failed to save GPS:', err)
            }
        },
        (err) => console.log('GPS denied:', err)
    )
},

openPartnerDetail(partner) {
    this.selectedPartner = partner
},

getStockBadge(partner) {
    const total = partner.available_units || 0
    if (total > 10) return 'bg-success'
    if (total > 0) return 'bg-warning text-dark'
    return 'bg-danger'
},

getStockLabel(partner) {
    const total = partner.available_units || 0
    if (total > 10) return 'Stock: High'
    if (total > 0) return 'Stock: Low'
    return 'Stock: Critical'
},
    async fetchProfile() {
      this.loading = true
      this.error = null

      const token = localStorage.getItem('access_token')

      if (!token) {
        this.$router.push('/')
        return
      }

      try {
        const response = await fetch('http://localhost:8000/api/users/profile/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (!response.ok) throw new Error('Failed to fetch profile')

        this.donor = await response.json()
        await this.fetchPartnerRequests() 
        await this.fetchNearbyPartners() 

      } catch (err) {
        this.error = 'Could not load your profile. Please try again.'
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    async fetchPartnerRequests() {
    const coords = await this.getCoordinates()
    const lat = coords?.lat || ''
    const lng = coords?.lon || ''
    const bg = this.donor.blood_group || ''

    // Backend filters by blood group
    // Frontend can additionally filter by distance
    const response = await api.get(
        `/api/requests/donor/list/?blood_group=${bg}`
    )

    // Filter by distance on frontend
    if (lat && lng && response.data.length > 0) {
        this.partnerRequests = response.data.filter(req => {
            if (!req.latitude || !req.longitude) return true
            const distance = this.calculateDistance(
                lat, lng,
                req.latitude, req.longitude
            )
            return distance <= 20  // ← 20km radius
        })
    } else {
        this.partnerRequests = response.data
    }
},

// Haversine formula on frontend
calculateDistance(lat1, lng1, lat2, lng2) {
    const R = 6371
    const dLat = (lat2 - lat1) * Math.PI / 180
    const dLng = (lng2 - lng1) * Math.PI / 180
    const a =
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(lat1 * Math.PI / 180) *
        Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLng/2) * Math.sin(dLng/2)
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
},

getCoordinates() {
  return new Promise((resolve) => {
    if (!navigator.geolocation) {
      resolve(null)
      return
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve({
        lat: pos.coords.latitude,
        lon: pos.coords.longitude
      }),
      () => resolve(null)  
    )
  })
},

    timeAgo(dateStr) {
      const diff = Math.floor((new Date() - new Date(dateStr)) / 60000)
      if (diff < 60) return `${diff} mins ago`
      if (diff < 1440) return `${Math.floor(diff / 60)} hrs ago`
      return `${Math.floor(diff / 1440)} days ago`
    },

    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('en-IN', {
        day: 'numeric', month: 'short', year: 'numeric'
      })
    },

    isExpiringSoon(dateStr) {
      const hoursLeft = (new Date(dateStr) - new Date()) / 36e5
      return hoursLeft < 12
    },

    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      this.$router.push('/')
    }
  },

  }
</script>
