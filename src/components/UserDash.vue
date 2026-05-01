
    <style>

    .blood-group-circle {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #E63946, #C1121F);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 0.85rem;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(230, 57, 70, 0.3);
}

.text-sky { color: #00AEEF !important; }
.smallest { font-size: 0.7rem; }

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
            
            <RouterLink to="/profile" class="nav-icon"><i class="fa-regular fa-circle-user"></i></RouterLink>
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
            <p class="fw-bold mb-0">{{ donor.total_donations }} People</p>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="jd-card stat-card">
            <div class="stat-icon"><i class="fa-solid fa-heart-pulse"></i></div>
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

                <a
  v-if="partner.latitude != null && partner.longitude != null"
  :href="getGoogleMapsLink(partner)"
  target="_blank"
  class="btn btn-sm btn-outline-success rounded-circle p-1"
  style="width:30px;height:30px;display:flex;
  align-items:center;justify-content:center"
  title="Navigate"
  @click.stop
>
  <i class="fas fa-location-arrow"></i>
</a>


                



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

  <!--   EMPTY STATE -->
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
<button
    class="btn btn-danger btn-sm rounded-pill flex-grow-1 py-2"
    @click="acceptRequest(req.id)"
    :disabled="acceptingId === req.id"
>
    <span v-if="acceptingId === req.id">
        <span class="spinner-border spinner-border-sm me-1"></span>
        Accepting...
    </span>
    <span v-else>Accept</span>
</button>
          
        </div>
      </div>
    </div>
  </div>

</div>


<!----My attenders request-->

<!-- My Raised Requests -->
<div class="mt-5 mb-4">
    <div class="d-flex justify-content-between align-items-end mb-3">
        <div>
            <h5 class="fw-bold mb-0">My Raised Requests</h5>
            <p class="text-muted small mb-0">
                Blood requests you have raised
            </p>
        </div>
        <button
            class="btn btn-outline-danger btn-sm rounded-pill px-3"
            @click="fetchMyRequests"
        >
            <i class="fa-solid fa-rotate-right me-1"></i> Refresh
        </button>
    </div>

    <!-- Loading -->
    <div v-if="myRequestsLoading" class="text-center py-4">
        <div class="spinner-border spinner-border-sm text-danger"></div>
        <span class="ms-2 text-muted small">Loading your requests...</span>
    </div>

    <!-- Empty -->
    <div v-else-if="myRequests.length === 0" class="jd-card p-5 text-center">
        <i class="fa-solid fa-file-medical text-danger mb-3"
            style="font-size:2.5rem;opacity:0.3"></i>
        <h6 class="fw-bold mb-1">No Requests Raised Yet</h6>
        <p class="text-muted small mb-0">
            When you raise a blood request it will appear here.
        </p>
        <router-link to="/user_request"
            class="btn btn-danger btn-sm rounded-pill px-4 mt-3">
            Raise a Request
        </router-link>
    </div>

    <!-- Request cards -->
    <div v-else class="row g-3">
        <div
            class="col-md-6 col-lg-4"
            v-for="req in myRequests"
            :key="req.reference_id"
        >
            <div class="jd-card p-3 h-100">

                <!-- Status badge + urgency -->
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <span :class="['badge rounded-pill px-3 py-2',
                        req.status === 'fulfilled' ? 'bg-success' :
                        req.status === 'pending' ? 'bg-warning text-dark' :
                        req.status === 'expired' ? 'bg-secondary' :
                        'bg-danger']">
                        <i :class="['me-1 small',
                            req.status === 'fulfilled' ? 'fas fa-check' :
                            req.status === 'pending' ? 'fas fa-clock' :
                            req.status === 'expired' ? 'fas fa-times' :
                            'fas fa-spinner']">
                        </i>
                        {{ req.status?.toUpperCase() }}
                    </span>
                    <span :class="['badge rounded-pill small',
                        req.urgency === 'critical' ? 'bg-danger' :
                        req.urgency === 'urgent' ? 'bg-warning text-dark' :
                        'bg-light text-muted border']">
                        {{ req.urgency?.toUpperCase() }}
                    </span>
                </div>

                <!-- Blood group + quantity -->
                <div class="d-flex align-items-center gap-3 mb-3">
                    <div class="blood-group-circle">
                        {{ req.blood_group }}
                    </div>
                    <div>
                        <h6 class="fw-bold mb-0">{{ req.patient_name }}</h6>
                        <small class="text-muted">
                            {{ req.quantity }} units needed
                        </small>
                    </div>
                </div>

                <!-- Details -->
                <div class="p-3 bg-light rounded-4 mb-3">
                    <div class="d-flex justify-content-between py-1 border-bottom">
                        <small class="text-muted">
                            <i class="fas fa-hospital me-1"></i>Hospital
                        </small>
                        <small class="fw-bold text-end"
                            style="max-width:140px;overflow:hidden;
                            text-overflow:ellipsis;white-space:nowrap">
                            {{ req.hospital_name }}
                        </small>
                    </div>
                    <div class="d-flex justify-content-between py-1 border-bottom">
                        <small class="text-muted">
                            <i class="fas fa-location-dot me-1"></i>City
                        </small>
                        <small class="fw-bold">{{ req.city }}</small>
                    </div>
                    <div class="d-flex justify-content-between py-1 border-bottom">
                        <small class="text-muted">
                            <i class="fas fa-calendar me-1"></i>Raised
                        </small>
                        <small class="fw-bold">{{ timeAgo(req.created_at) }}</small>
                    </div>

                    <!-- Fulfilled at — only show if fulfilled -->
                    <div v-if="req.status === 'fulfilled'"
                        class="d-flex justify-content-between py-1 border-bottom">
                        <small class="text-muted">
                            <i class="fas fa-check-circle me-1 text-success"></i>
                            Fulfilled
                        </small>
                        <small class="fw-bold text-success">
                            {{ formatDate(req.updated_at) }}
                        </small>
                    </div>

                    <!-- Expires at — only show if pending -->
                    <div v-if="req.status === 'pending'"
                        class="d-flex justify-content-between py-1 border-bottom">
                        <small class="text-muted">
                            <i class="fas fa-clock me-1 text-warning"></i>
                            Expires
                        </small>
                        <small :class="['fw-bold',
                            isExpiringSoon(req.expires_at) ?
                            'text-danger' : 'text-muted']">
                            {{ formatDate(req.expires_at) }}
                        </small>
                    </div>

                    <!-- Reference ID with copy -->
                    <div class="d-flex justify-content-between align-items-center py-1">
                        <small class="text-muted">
                            <i class="fas fa-hashtag me-1"></i>Ref ID
                        </small>
                        <div class="d-flex align-items-center gap-1">
                            <small class="fw-bold text-sky"
                                style="font-size:0.65rem;
                                max-width:100px;overflow:hidden;
                                text-overflow:ellipsis">
                                {{ req.reference_id?.substring(0, 12) }}...
                            </small>
                            <button
                                class="btn p-0 border-0"
                                style="background:none"
                                @click="copyRefId(req.reference_id)"
                                :title="'Copy: ' + req.reference_id"
                            >
                                <i :class="['fa-sm',
                                    copiedRefId === req.reference_id ?
                                    'fas fa-check text-success' :
                                    'far fa-copy text-muted']">
                                </i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Action buttons -->
                <div class="d-flex gap-2">
                    <!-- Rate button — only if fulfilled and not yet rated -->
                    <button
                        v-if="req.status === 'fulfilled' && !req.is_rated"
                        class="btn btn-outline-danger btn-sm rounded-pill flex-grow-1 py-2"
                        @click="openRatingModal(req)"
                    >
                        <i class="fas fa-star me-1"></i> Rate Partner
                    </button>

                    <!-- Rated badge -->
                    <span v-if="req.is_rated"
                        class="badge bg-success-subtle text-success
                        rounded-pill px-3 py-2 flex-grow-1 text-center">
                         Rated
                    </span>

                    <!-- Copy full ref ID -->
                    <button
                        class="btn btn-light btn-sm rounded-pill py-2 px-3"
                        @click="copyRefId(req.reference_id)"
                        :title="'Copy Reference ID'"
                    >
                        <i :class="[
                            copiedRefId === req.reference_id ?
                            'fas fa-check text-success' :
                            'far fa-copy text-muted']">
                        </i>
                    </button>
                </div>

                <!-- Copied toast -->
                <div v-if="copiedRefId === req.reference_id"
                    class="text-center mt-2">
                    <small class="text-success smallest fw-bold">
                         Reference ID copied!
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>


          <!-- Enrolled camps-->

          <div class="mt-5">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h4 class="fw-800 mb-0"><i class="fas fa-bookmark text-danger me-2"></i>My Enrolled Camps</h4>
    <span class="badge bg-danger-soft text-danger rounded-pill px-3">{{ enrolledCamps.length }} Enrolled</span>
  </div>

  <div v-if="enrolledLoading" class="text-center py-5">
    <div class="spinner-border text-danger"></div>
  </div>

  <div v-else-if="enrolledCamps.length === 0" class="card border-0 shadow-sm rounded-4 p-5 text-center bg-light">
    <i class="fas fa-calendar-times text-muted fa-3x mb-3"></i>
    <h6 class="fw-bold">No Enrollments Found</h6>
    <p class="text-muted small">Camps you register for will appear here.</p>
  </div>

  <div v-else class="row g-3">
    <div class="col-md-6 col-lg-4" v-for="camp in enrolledCamps" :key="camp.id">
      <div class="card border-0 shadow-sm rounded-4 overflow-hidden h-100 border-start border-danger border-4">
        <div class="card-body p-4">
          <div class="d-flex justify-content-between mb-2">
            <span class="badge bg-success-soft text-success smallest rounded-pill">Confirmed</span>
            <small class="text-muted"><i class="far fa-clock me-1"></i>{{ formatDate(camp.camp_date) }}</small>
          </div>
          <h6 class="fw-bold mb-2">{{ camp.title }}</h6>
          <p class="smallest text-muted mb-3"><i class="fas fa-map-marker-alt me-1 text-danger"></i>{{ camp.location }}</p>
          
          <div class="d-flex align-items-center justify-content-between mt-auto pt-3 border-top">
            <a :href="'https://maps.google.com/?q=' + camp.location" target="_blank" class="btn btn-link btn-sm text-sky p-0 text-decoration-none">
              <i class="fas fa-directions me-1"></i> Get Directions
            </a>
            
          </div>
        </div>
      </div>
    </div>
  </div>
</div>


          







          <!-- Nearby Camps — FROM API -->
<h5 class="fw-bold mb-3 mt-4">Discover Nearby Camps</h5>

<div v-if="campsLoading" class="text-center py-3">
    <div class="spinner-border spinner-border-sm text-danger"></div>
</div>

<div v-else-if="nearbyCamps.length === 0" class="jd-card p-4 text-center text-muted">
    <i class="fas fa-campground fa-2x mb-2 opacity-25"></i>
    <p class="small mb-0">No camps scheduled near you right now.</p>
</div>

<div v-else class="camp-slider mb-4">
    <div class="camp-card shadow-sm" v-for="camp in nearbyCamps" :key="camp.id">
        <div class="camp-img"
            style="background-image: url('https://images.unsplash.com/photo-1615461066841-6116e61058f4?auto=format&fit=crop&q=80&w=600')">
        </div>
        <div class="p-3">
            <span class="text-muted small fw-bold">{{ camp.organizer_name?.toUpperCase() }}</span>
            <h6 class="fw-bold mb-1 mt-1">{{ camp.title }}</h6>
            <p class="text-muted small mb-1">
                <i class="fas fa-calendar me-1 text-danger"></i>{{ camp.camp_date }}
            </p>
            <p class="text-muted small mb-2">
                <i class="fas fa-location-dot me-1 text-danger"></i>{{ camp.location }}
                <span v-if="camp.distance_km" class="ms-1 fw-bold text-danger">
                    ({{ camp.distance_km }}km)
                </span>
            </p>
            <div class="d-flex flex-wrap gap-1 mb-3">
                <span v-for="bg in camp.blood_groups_needed" :key="bg"
                    class="badge bg-danger bg-opacity-10 text-danger rounded-pill small">
                    {{ bg }}
                </span>
            </div>
            <button
                class="btn btn-outline-danger btn-sm w-100 rounded-pill fw-bold"
                @click="openEnrollModal(camp)"
            >
                <i class="fas fa-user-plus me-1"></i> Enroll Now
            </button>
        </div>
    </div>
</div>

<!-- Enroll Modal -->
<div v-if="showEnrollModal" class="modal-overlay" @click.self="showEnrollModal = false">
    <div class="registration-card shadow-lg" style="max-width:450px">

        <button class="close-btn" @click="showEnrollModal = false">
            <i class="fas fa-times"></i>
        </button>
        <div class="card-body p-4">
            <h5 class="fw-bold mb-1">Enroll in Camp</h5>
            <p class="text-muted small mb-4">{{ selectedCamp?.title }}</p>
            <h6 class="text-danger fw-bold small mb-4">
    <i class="fas fa-exclamation-triangle me-1"></i> 
    Note: Cancellation is not allowed after the request is accepted.
</h6>

            <div class="mb-3">
                <label class="small fw-bold text-muted">Your Name</label>
                <input type="text" class="form-control" v-model="enrollForm.name">
            </div>
            <div class="mb-3">
                <label class="small fw-bold text-muted">Phone Number</label>
                <input type="tel" class="form-control" v-model="enrollForm.phone">
            </div>
            <div class="mb-4">
                <label class="small fw-bold text-muted">Blood Group</label>
                <select class="form-select" v-model="enrollForm.blood_group">
                    <option v-for="bg in ['A+','A-','B+','B-','O+','O-','AB+','AB-']" :key="bg">
                        {{ bg }}
                    </option>
                </select>
            </div>

            <button
                class="btn btn-danger w-100 py-3 fw-bold rounded-4"
                @click="enrollInCamp"
                :disabled="enrolling"
            >
                <span v-if="enrolling">
                    <span class="spinner-border spinner-border-sm me-2"></span>
                    Enrolling...
                </span>
                <span v-else>
                    <i class="fas fa-check me-2"></i> Confirm Enrollment
                </span>
            </button>
        </div>
    </div>
</div>
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

  <div :class="[
    'eligibility-check shadow-sm mb-3', 
    donor.is_aadhaar_verified ? 'bg-success text-white' : 'bg-danger text-white'
  ]">
  
    <i :class="donor.is_aadhaar_verified ? 'fa-solid fa-check' : 'fa-solid fa-xmark'"></i>
  </div>
  

  <p :class="['fw-bold mb-1', donor.is_aadhaar_verified ? 'text-success' : 'text-danger']">
    {{ donor.is_aadhaar_verified ? 'Ready to Donate!' : 'Verification Pending' }}
  </p>

  <div class="alert alert-light border-0 small text-muted mb-0">
    <i class="fa-solid fa-info-circle me-1 text-primary"></i>
    Quick Tip: Ensure you are feeling healthy and have maintained a 
    safe gap since your last donation.
  </div>
  <p class="small text-muted mb-3">
    Reliability Score: <strong class="text-success">{{ donor.reliability_score }}</strong> |
    Aadhaar Verified: <strong>{{ donor.is_aadhaar_verified ? '✔️' : '❌' }}</strong>
  </p>

  <div v-if="!donor.is_aadhaar_verified" class="alert alert-danger py-2 px-3 small border-0 mb-0">
    <i class="fa-solid fa-triangle-exclamation me-1"></i>
    Please verify your Aadhaar to participate in camps.
  </div>
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
                        v-for="(qty, group) in selectedPartner.available_units"
                        :key="group"
                        :class="['badge rounded-pill px-3 py-2', qty > 5 ? 'bg-success' : qty > 0 ? 'bg-warning text-dark' : 'bg-danger']"
                    >
                        {{ group }}: {{ qty }} units
                    </span>
                    <span v-if="!selectedPartner.available_units" class="text-muted small">
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

<!-- Partner Request Detail Modal -->
<div v-if="selectedRequest" class="modal-overlay" @click.self="selectedRequest = null">
    <div class="registration-card shadow-lg" style="max-width:480px">
        <button class="close-btn" @click="selectedRequest = null">
            <i class="fas fa-times"></i>
        </button>

        <div class="card-body p-4">
            <!-- Header -->
            <div class="d-flex align-items-center gap-3 mb-4">
                <img
                    :src="`https://ui-avatars.com/api/?name=${encodeURIComponent(selectedRequest.hospital_name)}&background=E63946&color=fff`"
                    class="partner-avatar"
                    :alt="selectedRequest.hospital_name"
                    @click="openRequestDetail(selectedRequest)"
                    style="width:55px;height:55px;border-radius:14px"
                >
                <div>
                    <h5 class="fw-bold mb-0">{{ selectedRequest.hospital_name }}</h5>
                    <small class="text-muted">
                        <i class="fa-solid fa-location-dot me-1 text-danger"></i>
                        {{ selectedRequest.city }}
                        <span v-if="selectedRequest.distance_km" class="ms-2 text-danger fw-bold">
                            {{ selectedRequest.distance_km }} km away
                        </span>
                    </small>
                </div>
            </div>

            <!-- Request details -->
            <div class="p-3 bg-light rounded-4 mb-4">
                <div class="d-flex justify-content-between py-2 border-bottom">
                    <small class="text-muted">Blood Group Needed</small>
                    <strong class="text-danger">{{ selectedRequest.blood_group }}</strong>
                </div>
                <div class="d-flex justify-content-between py-2 border-bottom">
                    <small class="text-muted">Units Required</small>
                    <strong>{{ selectedRequest.quantity }} units</strong>
                </div>
                <div class="d-flex justify-content-between py-2 border-bottom">
                    <small class="text-muted">Status</small>
                    <span class="badge bg-warning text-dark rounded-pill">{{ selectedRequest.status }}</span>
                </div>
                <div class="d-flex justify-content-between py-2 border-bottom">
                    <small class="text-muted">Posted</small>
                    <small class="fw-bold">{{ timeAgo(selectedRequest.created_at) }}</small>
                </div>
                <div class="d-flex justify-content-between py-2">
                    <small class="text-muted">Expires</small>
                    <small :class="['fw-bold', isExpiringSoon(selectedRequest.expires_at) ? 'text-danger' : 'text-success']">
                        {{ formatDate(selectedRequest.expires_at) }}
                    </small>
                </div>
            </div>

            <!-- Urgency indicator -->
            <div :class="['p-3 rounded-4 mb-4 text-center', isExpiringSoon(selectedRequest.expires_at) ? 'bg-danger bg-opacity-10' : 'bg-success bg-opacity-10']">
                <i :class="['me-2', isExpiringSoon(selectedRequest.expires_at) ? 'fas fa-exclamation-triangle text-danger' : 'fas fa-clock text-success']"></i>
                <small :class="['fw-bold', isExpiringSoon(selectedRequest.expires_at) ? 'text-danger' : 'text-success']">
                    {{ isExpiringSoon(selectedRequest.expires_at) ? 'URGENT — Expiring soon!' : 'Normal priority' }}
                </small>
            </div>

            <!-- OTP info (shown after accept) -->
            <div v-if="acceptedOTP" class="p-3 bg-danger bg-opacity-10 rounded-4 mb-4 text-center">
                <p class="fw-bold mb-1 text-danger">Your One-Time Code</p>
                <h2 class="fw-800 text-danger mb-1 display-5">{{ acceptedOTP }}</h2>
                <small class="text-muted">Show this code at the blood bank — keep it safe!</small>
            </div>

            <!-- Buttons -->
            <div v-if="!acceptedOTP">
                <button
                    class="btn btn-danger w-100 py-3 fw-bold rounded-4 shadow mb-2"
                    @click="acceptRequest(selectedRequest.id)"
                    :disabled="acceptingId === selectedRequest.id"
                >
                    <span v-if="acceptingId === selectedRequest.id">
                        <span class="spinner-border spinner-border-sm me-2"></span>
                        Accepting...
                    </span>
                    <span v-else>
                        <i class="fas fa-heart me-2"></i>
                        Accept & Donate
                    </span>
                </button>
                <button class="btn btn-light w-100 py-2 rounded-4" @click="selectedRequest = null">
                    Cancel
                </button>
            </div>

            <!-- After accepted — go to chat -->
            <div v-else>
                <button
                    class="btn btn-danger w-100 py-3 fw-bold rounded-4 shadow mb-2"
                    @click="goToChat"
                >
                    <i class="fas fa-comments me-2"></i>
                    Open Chat with Bank
                </button>
                <button class="btn btn-light w-100 py-2 rounded-4" @click="selectedRequest = null">
                    Close
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Rating & Complaint Modal -->
<!-- Rating Modal -->
<div v-if="showRatingModal" class="modal-overlay"
    @click.self="showRatingModal = false">
    <div class="registration-card shadow-lg" style="max-width:450px">
        <button class="close-btn" @click="showRatingModal = false">
            <i class="fas fa-times"></i>
        </button>

        <div class="card-body p-4">
            <h5 class="fw-bold mb-1">Rate Partner</h5>
            <p class="text-muted small mb-4">{{ ratingPartner?.hospital_name }}</p>

            <!-- Reference ID input -->
            <div class="mb-3">
                <label class="small fw-bold text-muted">
                    Your Request Reference ID *
                </label>
                <input type="text"
                    class="form-control"
                    v-model="ratingForm.reference_id"
                    placeholder="Enter reference ID of your request">
                <small class="text-muted">
                    Rate only after your request is fulfilled
                </small>
            </div>

            <!-- Stars -->
            <div class="mb-3">
                <label class="small fw-bold text-muted">Rating *</label>
                <div class="d-flex gap-2 mt-1">
                    <button
                        v-for="star in 5"
                        :key="star"
                        type="button"
                        class="btn p-0 fs-4"
                        @click="ratingForm.stars = star"
                    >
                        <i :class="['fas fa-star',
                            star <= ratingForm.stars ? 'text-warning' : 'text-muted']">
                        </i>
                    </button>
                </div>
            </div>

            <!-- Review -->
            <div class="mb-3">
                <label class="small fw-bold text-muted">Review</label>
                <textarea class="form-control" rows="2"
                    v-model="ratingForm.review"
                    placeholder="Share your experience (optional)">
                </textarea>
            </div>

            <!-- Complaint -->
            <div class="mb-3">
                <div class="form-check">
                    <input class="form-check-input" type="checkbox"
                        id="hasComplaint"
                        v-model="ratingForm.has_complaint">
                    <label class="form-check-label small text-muted"
                        for="hasComplaint">
                        File a complaint against this partner
                    </label>
                </div>
            </div>

            <div v-if="ratingForm.has_complaint">
                <div class="mb-2">
                    <label class="small fw-bold text-muted">Complaint Type</label>
                    <select class="form-select" v-model="ratingForm.complaint_type">
                        <option disabled value="">Select type</option>
                        <option value="exchange_condition">
                            Asked for blood exchange
                        </option>
                        <option value="overcharging">Charged extra fees</option>
                        <option value="misbehavior">Staff misbehavior</option>
                        <option value="fake_stock">Wrong stock shown</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="small fw-bold text-muted">Complaint Detail</label>
                    <textarea class="form-control" rows="2"
                        v-model="ratingForm.complaint_detail"
                        placeholder="Describe what happened">
                    </textarea>
                </div>
            </div>

            <!-- Error/Success -->
            <div v-if="ratingError"
                class="alert alert-danger border-0 rounded-4 small mb-3">
                {{ ratingError }}
            </div>
            <div v-if="ratingSuccess"
                class="alert alert-success border-0 rounded-4 small mb-3">
                {{ ratingSuccess }}
            </div>

            <button
                class="btn btn-danger w-100 py-3 fw-bold rounded-4"
                @click="submitRating"
                :disabled="submittingRating || !ratingForm.stars || !ratingForm.reference_id"
            >
                <span v-if="submittingRating">
                    <span class="spinner-border spinner-border-sm me-2"></span>
                </span>
                <span v-else>
                    <i class="fas fa-star me-2"></i> Submit Rating
                </span>
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
selectedRequest: null,
acceptingId: null,
acceptedOTP: null,
acceptedRequestId: null,
nearbyCamps: [],
campsLoading: false,
showEnrollModal: false,
selectedCamp: null,
enrollForm: {
    name: '',
    phone: '',
    blood_group: '',

    user: {},
    enrolledCamps: [],
    enrolledLoading: false,
    
    
  

},

//attender_card
myRequests: [],
myRequestsLoading: false,
copiedRefId: null,

// Rating
showRatingModal: false,
ratingPartner: null,
ratingForm: {
    reference_id: '',
    stars: 0,
    review: '',
    has_complaint: false,
    complaint_type: '',
    complaint_detail: ''
},
submittingRating: false,
ratingError: null,
ratingSuccess: null,
enrolling: false,
    }
  },
  mounted() {
  this.fetchProfile()
  this.saveGPSLocation()
  this.fetchEnrolledCamps()
},

  methods: {
    async fetchNearbyPartners() {
    this.partnersLoading = true
    try {
        const coords = await this.getCoordinates() 
        const lat = coords?.lat || ''
        const lng = coords?.lon || ''

        const url = `https://jeevandaan-yaal.onrender.com/api/partners/nearby/?lat=${lat}&lng=${lng}&radius=20`
        const response = await fetch(url)
        const data = await response.json()
        console.log('Nearby partners data:', data)
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
                await api.post('https://jeevandaan-yaal.onrender.com/api/users/update-location/', {
                    latitude: pos.coords.latitude,
                    longitude: pos.coords.longitude
                })
                console.log('GPS location saved  ')
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
        console.log("TOKEN BEFORE API CALL:", token)
        const response = await fetch('https://jeevandaan-yaal.onrender.com/api/users/profile/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (!response.ok) throw new Error('Failed to fetch profile')

        this.donor = await response.json()
        await this.fetchPartnerRequests() 
        await this.fetchNearbyPartners() 
        await this.fetchNearbyCamps()
        await this.fetchMyRequests()

      } catch (err) {
        this.error = 'Could not load your profile. Please try again.'
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    async fetchPartnerRequests() {
    this.requestsLoading = true

    try {
        // 1. Get coordinates once
        const coords = await this.getCoordinates()

        if (!coords) {
            console.warn("GPS not available")
        }

        const lat = coords?.lat || ''
        const lng = coords?.lon || ''
        const bg = encodeURIComponent(this.donor?.blood_group || '')

        // 2. Call API (backend already handles distance filtering)
        const url = `https://jeevandaan-yaal.onrender.com/api/requests/donor/list/?blood_group=${bg}&lat=${lat}&lon=${lng}`
          console.log('CALLING URL:', url)    // ← add this

        const response = await api.get(url)
          console.log('RESPONSE:', response.data)

        // 3. Direct assign (NO frontend filtering)
        this.partnerRequests = Array.isArray(response.data) ? response.data : []

    } catch (err) {
        console.error("Failed to fetch partner requests:", err)
        this.partnerRequests = []
    } finally {
        // 4. ALWAYS stop loading
        this.requestsLoading = false
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

    // ── Open request detail modal ────────────
openRequestDetail(req) {
    this.selectedRequest = req
    this.acceptedOTP = null
    this.acceptedRequestId = null
},

// ── Accept request ────────────────────────
async acceptRequest(requestId) {
    this.acceptingId = requestId

    try {

      const selected = this.partnerRequests.find(r => r.id === requestId)
        const response = await api.post(
            `https://jeevandaan-yaal.onrender.com/api/requests/donor/${requestId}/accept/`
        )



        // Store OTP — show to donor ONCE
        this.acceptedOTP = response.data.otp_code
        this.acceptedRequestId = requestId

        

        

        this.selectedRequest = selected

        // Refresh requests list
        await this.fetchPartnerRequests()

    } catch (err) {
        const msg = err.response?.data?.error || 'Failed to accept. Try again.'
        alert(msg)
        console.error(err)
    } finally {
        this.acceptingId = null
    }
},

// ── Go to chat page ───────────────────────
goToChat() {
    if (!this.acceptedRequestId) return
    localStorage.setItem(`otp_${this.acceptedRequestId}`, this.acceptedOTP)
    this.$router.push({
        path: `/chat/${this.acceptedRequestId}`,
        query: { otp: this.acceptedOTP }
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
    },
    // ── Open camp enrollment modal ───────────────────────
    async fetchNearbyCamps() {
    this.campsLoading = true
    try {
        const coords = await this.getCoordinates()
        const lat = coords?.lat || ''
        const lng = coords?.lon || ''

        const response = await api.get(
            `https://jeevandaan-yaal.onrender.com/api/partners/camps/nearby/?lat=${lat}&lng=${lng}`
        )
        this.nearbyCamps = Array.isArray(response.data) ? response.data : []
    } catch (err) {
        this.nearbyCamps = []
    } finally {
        this.campsLoading = false
    }
},

openEnrollModal(camp) {
    this.selectedCamp = camp
    this.enrollForm = {
        name: this.donor.name || '',
        phone: this.donor.phone_number || '',
        blood_group: this.donor.blood_group || ''
    }
    this.showEnrollModal = true
},

async enrollInCamp() {
    this.enrolling = true
    try {
        await api.post(
            `https://jeevandaan-yaal.onrender.com/api/partners/camps/${this.selectedCamp.id}/enroll/`,
            this.enrollForm
        )
        alert('Enrolled successfully! See you at the camp 🩸')
        this.showEnrollModal = false
        await this.fetchNearbyCamps()
    } catch (err) {
        alert(err.response?.data?.error || 'Enrollment failed.')
    } finally {
        this.enrolling = false
    }
},


// ... enrolled camps ...

  async fetchEnrolledCamps() {
  this.enrolledLoading = true;
  try {
    const res = await api.get('https://jeevandaan-yaal.onrender.com/api/partners/camps/enrolled/');
    
    this.enrolledCamps = res.data || []; 
  } catch (err) {
    this.enrolledCamps = []; // Reset to empty array on error
    console.error(err);
  } finally {
    this.enrolledLoading = false;
  }
},

  async cancelEnrollment(campId) {
    if (!confirm("Are you sure you want to cancel your enrollment for this camp?")) return;
    
    try {
      await api.post(`https://jeevandaan-yaal.onrender.com/api/camps/${campId}/cancel/`, {}, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      alert("Enrollment cancelled successfully.");
      // Refresh both lists
      this.fetchEnrolledCamps();
      if (this.fetchAvailableCamps) this.fetchAvailableCamps(); 
    } catch (err) {
      alert("Failed to cancel enrollment.");
    }
  },


  
openRatingModal(partner) {
    this.ratingPartner = partner
    this.ratingForm = {
        reference_id: '',
        stars: 0,
        review: '',
        has_complaint: false,
        complaint_type: '',
        complaint_detail: ''
    }
    this.ratingError = null
    this.ratingSuccess = null
    this.showRatingModal = true
},

async submitRating() {
    if (!this.ratingForm.stars) {
        this.ratingError = 'Please select star rating.'
        return
    }
    if (!this.ratingForm.reference_id) {
        this.ratingError = 'Reference ID is required.'
        return
    }

    this.submittingRating = true
    this.ratingError = null

    try {
        await api.post(
            `https://jeevandaan-yaal.onrender.com/api/requests/attender/${this.ratingForm.reference_id}/rate/`,
            {
                stars: this.ratingForm.stars,
                review: this.ratingForm.review,
                has_complaint: this.ratingForm.has_complaint,
                complaint_type: this.ratingForm.complaint_type,
                complaint_detail: this.ratingForm.complaint_detail
            }
        )

        this.ratingSuccess = 'Rating submitted successfully!  '
        setTimeout(() => {
            this.showRatingModal = false
            this.ratingSuccess = null
        }, 2000)

    } catch (err) {
        this.ratingError = err.response?.data?.error ||
            'Failed to submit. Make sure request is fulfilled.'
    } finally {
        this.submittingRating = false
    }
},

// Attnder opening card 
// ── Fetch my raised requests ─────────────
async fetchMyRequests() {
    this.myRequestsLoading = true
    try {
        const response = await api.get('https://jeevandaan-yaal.onrender.com/api/requests/attender/my-requests/')
        this.myRequests = Array.isArray(response.data) ? response.data : []
    } catch (err) {
        console.error('My requests fetch failed:', err)
        this.myRequests = []
    } finally {
        this.myRequestsLoading = false
    }
},

// ── Copy reference ID ────────────────────
async copyRefId(refId) {
    try {
        await navigator.clipboard.writeText(refId)
        this.copiedRefId = refId

        // Reset after 2 seconds
        setTimeout(() => {
            this.copiedRefId = null
        }, 2000)
    } catch (err) {
        // Fallback for older browsers
        const el = document.createElement('textarea')
        el.value = refId
        document.body.appendChild(el)
        el.select()
        document.execCommand('copy')
        document.body.removeChild(el)

        this.copiedRefId = refId
        setTimeout(() => {
            this.copiedRefId = null
        }, 2000)
    }
},

getGoogleMapsLink(partner) {
    const lat = partner.latitude
    const lng = partner.longitude
    const name = encodeURIComponent(partner.hospital_name)

    // This opens Google Maps with:
    // → Destination = partner location
    // → Label = hospital name
    // → Navigation mode = driving
    return `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}&destination_place_id=${name}&travelmode=driving`
},
}
}

  
 
</script>
