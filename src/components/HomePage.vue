<template>
  <div class="jeevandaan-platform">
    <nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top py-3">
  <div class="container">
    <a class="navbar-brand fw-bold text-danger d-flex align-items-center" href="#">

      <img 
    src="@/assets/L1.png" 
    alt="JeevanDaan Logo" 
    width="32" 
    height="32" 
    class="me-2 d-inline-block align-top logo-icon"
  >
  
  <span>JeevanDaan<span class="text-dark">+</span></span>
    </a>

    <button 
      class="navbar-toggler border-0 shadow-none" 
      type="button" 
      data-bs-toggle="collapse" 
      data-bs-target="#navbarNav" 
      aria-controls="navbarNav" 
      aria-expanded="false" 
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav mx-auto gap-lg-4 py-3 py-lg-0">
        <router-link to="/learn" class="nav-link fw-semibold">Learn More</router-link>
<a href="javascript:void(0)" @click="showRaiseModal = true" class="nav-link fw-semibold">Raise a Request</a>
<router-link to="/partnersreg" class="nav-link fw-semibold">Join as Partner</router-link>
<router-link to="/partners_login" class="nav-link fw-semibold">Partners Login</router-link>
      </ul>
      
      <div class="d-flex flex-column flex-lg-row align-items-lg-center gap-3">
        <router-link to="/login" class="text-dark text-decoration-none fw-bold small text-center text-lg-start">Login</router-link>
        <router-link to="/register" class="btn btn-danger px-4 py-2 fw-bold rounded-3">Register</router-link>
      </div>
    </div>
  </div>
</nav>

    <header class="hero-bg py-5">
      <div class="container py-lg-5">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <div class="emergency-tag mb-3">
              <span class="dot"></span> EMERGENCY NETWORK ACTIVE
            </div>
            <h1 class="display-3 fw-800 mb-4">
              Every Second <span class="text-danger">Counts.</span><br />
              Every Drop Matters.
            </h1>
            <p class="lead text-muted mb-5 pe-lg-5">
              India's real-time blood donation network — connecting donors, hospitals and blood banks instantly.
            </p>
            <div class="d-flex gap-3">
              <button
    class="btn btn-danger btn-lg px-4 fw-bold shadow-sm"
    @click="openBloodBankFinder">
    Donate Blood <i class="fas fa-arrow-right ms-2"></i>
</button>

<button
    class="btn btn-outline-dark btn-lg px-4 fw-bold bg-white"
    @click="openBloodBankFinder">
    Need Blood Urgently <i class="fas fa-tint ms-2"></i>
</button>
            </div>
          </div>
          <div class="col-lg-6 position-relative mt-5 mt-lg-0">
            <div class="hero-img-wrapper shadow-lg">
              <img src="../assets/d3.jpg" alt="Medical professional" class="img-fluid rounded-4">
              <div class="verified-badge d-flex align-items-center shadow">
                <div class="badge-icon me-3"><i class="fas fa-shield-heart"></i></div>
                <div>
                  <div class="fw-bold small">VERIFIED DONORS</div>
                  <div class="text-muted smaller">1.2k Lives Saved Today</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    

   <section class="mobile-stats-wrapper py-4 px-3">
      <div class="container">

        <div class="row row-cols-2 row-cols-md-4 g-4 text-center stats-grid">
          <div class="col" v-for="stat in tickerStats" :key="stat.label">
            <h2 class="stat-number fw-800 text-danger mb-0">{{ stat.val }}</h2>
            <p class="stat-label text-muted small fw-bold text-uppercase ls-1 mt-1">{{ stat.label }}</p>
          </div>
        </div>
        
      </div>
    </section>


    <section class="py-5 bg-white">
      <div class="container py-lg-5">
        <div class="row g-5">
          <div class="col-md-4" v-for="(step, index) in howItWorksSteps" :key="index">
            <div class="step-item">
              <div class="icon-box mb-4">
                <i :class="step.icon"></i>
              </div>
              <h4 class="fw-800 mb-3">{{ index + 1 }}. {{ step.title }}</h4>
              <p class="text-muted step-desc mb-0">
                {{ step.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="routing-section py-5 text-center text-white">
      <div class="container py-5">
        <span class="badge rounded-pill bg-light text-danger mb-3 px-3 py-2 text-uppercase">The Safety Net</span>
        <h2 class="fw-800 display-5 mb-3">Intelligent Routing Engine</h2>
        <p class="mb-5 opacity-75 mx-auto" style="max-width: 700px;">
          When every second counts, our autonomous system takes over to ensure zero failures in life-saving transfers.
        </p>
        <div class="row g-4 mt-4">
          <div class="col-md-4" v-for="(feat, i) in routingFeatures" :key="i">
            <div class="routing-card text-start">
              <div class="step-num">{{ i+1 }}</div>
              <div class="icon mb-3"><i :class="feat.icon"></i></div>
              <h6 class="fw-bold text-uppercase">{{ feat.title }}</h6>
              <p class="small opacity-75">{{ feat.desc }}</p>
            </div>
          </div>
        </div>
        <div class="mt-5 pt-3">
          <div class="ticker-pill d-inline-block p-2 px-4 rounded-pill">
            <small>Over <strong>120+ successful automated reroutes</strong> completed this week alone.</small>
          </div>
        </div>
      </div>
    </section>

    <section class="py-5 bg-white">
  <div class="container py-lg-4">
    <div class="row g-4">
      <div class="col-lg-8">
        <div class="card border-0 shadow-sm rounded-4 h-100 overflow-hidden">
          <div class="p-4 pb-0">
            <h5 class="fw-800 mb-1">Blood Availability Map</h5>
            <p class="text-muted small">Real-time inventory status across India's network</p>
          </div>
          
          <div class="map-wrapper m-4 mt-2 bg-light rounded-4 position-relative overflow-hidden border">
            <img 
              src="https://simplemaps.com/static/svg/country/in/admin1/in.svg" 
              alt="India Map" 
              class="img-fluid w-100 opacity-75"
              style="object-fit: contain; min-height: 400px; padding: 20px;"
            >
            
            <div class="position-absolute top-50 start-50 translate-middle w-100 text-center px-3">
              <button class="btn btn-white blur-btn shadow fw-bold px-4 py-3 rounded-3">
                <i class="fas fa-search-location text-danger me-2"></i> 
                Find nearest blood bank
              </button>
            </div>

            <div class="map-legend d-flex flex-wrap gap-3 position-absolute bottom-0 start-0 p-3 bg-white bg-opacity-75 w-100 border-top">
              <small class="d-flex align-items-center fw-bold">
                <span class="status-dot bg-success me-2"></span> HIGH STOCK
              </small>
              <small class="d-flex align-items-center fw-bold">
                <span class="status-dot bg-warning me-2"></span> LOW STOCK
              </small>
              <small class="d-flex align-items-center fw-bold">
                <span class="status-dot bg-danger pulse-red me-2"></span> CRITICAL
              </small>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-4">
        <div class="d-flex justify-content-between align-items-center mb-3 px-1">
          <h5 class="fw-800 mb-0">Live Requests</h5>
          <div class="d-flex align-items-center">
            <span class="pulse-red me-2"></span>
            <span class="text-danger smaller fw-800 text-uppercase tracking-wider">Real-time</span>
          </div>
        </div>

        <div class="request-scroll-area pe-1">
          <div 
            v-for="req in requests" 
            :key="req.id" 
            class="card request-item border-0 shadow-sm mb-3 rounded-4 transition-hover"
          >
            <div class="card-body p-3">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <h2 class="fw-800 text-danger mb-0 h3">{{ req.group }}</h2>
                <span :class="['badge rounded-pill smaller-badge px-3', urgencyClass(req.urgency)]">
                  {{ req.urgency }}
                </span>
              </div>
              
              <h6 class="fw-bold mb-1 text-dark">{{ req.hospital }}</h6>
              <div class="d-flex justify-content-between align-items-center text-muted smaller mb-3">
                <span><i class="fas fa-map-marker-alt me-1"></i> {{ req.city }}</span>
                <span><i class="far fa-clock me-1"></i> {{ req.time }}</span>
              </div>
              
              <router-link :to="`/login`"
                class="btn w-100 fw-800 py-2 rounded-3 transition-all"
                :class="req.urgency === 'CRITICAL' ? 'btn-danger shadow-sm' : 'btn-outline-danger'"
              >
                I Can Help <i class="fas fa-chevron-right ms-1 small"></i>
              </router-link>
            </div>
          </div>
        </div>

        <div class="text-center mt-3">
          <router-link to="/login" class="btn btn-light w-100 py-2 rounded-4">
            View All Requests
          </router-link>
        </div>
      </div>
    </div>
  </div>
</section>

    <section class="py-5 bg-white">
      <div class="container py-5 text-center">
        <h2 class="fw-800 display-5 mb-3">Built for Trust & Reliability</h2>
        <p class="text-muted mb-5">Securing India's healthcare infrastructure with data-driven blood management.</p>
        
        <div class="row g-4">
          <div class="col-md-6 col-lg-3" v-for="trust in trustCards" :key="trust.title">
            <div class="trust-card h-100 p-4 rounded-5 border border-light shadow-sm">
              <div class="trust-icon mb-4">
                <i :class="trust.icon"></i>
              </div>
              <h5 class="fw-bold mb-3">{{ trust.title }}</h5>
              <p class="text-muted small px-2">{{ trust.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-5 bg-white">
        <div class="container text-center">
            <h3 class="fw-bold mb-5">Top Impact Makers</h3>
            <div class="row justify-content-center g-3">
                <div class="col-md-8" v-for="donor in donors" :key="donor.id">
                    <div class="donor-leader-card shadow-sm text-start d-flex align-items-center p-3 rounded-4">
                        <div class="rank-box me-4">{{ donor.id }}</div>
                        <div class="flex-grow-1">
                            <div class="d-flex align-items-center">
                                <h6 class="fw-bold mb-0 me-2">Donor {{ donor.tag }}</h6>
                                <span class="badge rounded-pill bg-danger-soft text-danger smaller">{{ donor.tier }}</span>
                            </div>
                            <small class="text-muted">Member since {{ donor.year }} • {{ donor.donations }} Donations</small>
                        </div>
                        <div class="icon text-muted opacity-25"><i class="fas fa-ribbon fa-2x"></i></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="py-5 impact-section">
      <div class="container py-4">
        <div class="row text-center gy-4">
          <div class="col-6 col-md-3" v-for="impact in impactStats" :key="impact.label">
            <h2 class="display-4 fw-800 mb-0">{{ impact.val }}</h2>
            <p class="text-muted small fw-bold text-uppercase tracking-wider">{{ impact.label }}</p>
          </div>
        </div>
      </div>
    </section>

   
    

    <section class="container py-5 mb-5">
      <div class="cta-banner rounded-5 p-5 text-center text-white position-relative overflow-hidden">
        <div class="pattern-overlay"></div>
        
        <div class="position-relative z-index-1">
          <h2 class="display-4 fw-800 mb-4">Someone near you needs<br>blood right now</h2>
          <p class="lead mb-5 opacity-75 mx-auto" style="max-width: 600px;">
            Join 10,000+ Indians in building the world's most responsive life-saving network. Registration takes 60 seconds.
          </p>
          
          <div class="d-flex flex-column flex-md-row justify-content-center gap-3">
            <router-link to="/register" class="btn btn-light text-danger btn-lg px-5 py-3 fw-bold rounded-3">Register as Donor</router-link>
            <button
    class="btn btn-white blur-btn shadow fw-bold px-4 py-3 rounded-3"
    @click="openBloodBankFinder">
    <i class="fas fa-search-location text-danger me-2"></i>
    Find nearest blood bank
</button>
          </div>
        </div>
      </div>
    </section>

    <div v-if="showRaiseModal" class="modal-overlay">
  <div class="registration-card shadow-lg animate__animated animate__zoomIn">
    <button class="close-btn" @click="showRaiseModal = false">
      <i class="fas fa-times"></i>
    </button>

    <div class="card-body p-4 p-md-5">
      <div class="text-center mb-4">
        <div class="icon-circle mb-3">
          <i class="fas fa-file-medical text-danger"></i>
        </div>
        <h3 class="fw-800 mb-1">To Raise a Request Go with Simple Registration Steps</h3>
        <h4 class="fw-bold text-muted h6">अनुरोध करने के लिए सरल पंजीकरण प्रक्रिया का पालन करें</h4>
      </div>

      <div class="steps-container my-5">
        <div class="row g-3">
          <div class="col-md-4">
            <div class="mini-step text-center">
              <div class="step-num shadow-sm">1</div>
              <p class="fw-bold mb-0">Add Quick Details</p>
              <small class="text-muted">त्वरित विवरण जोड़ें</small>
            </div>
          </div>
          <div class="col-md-4">
            <div class="mini-step text-center">
              <div class="step-num shadow-sm">2</div>
              <p class="fw-bold mb-0">Register Yourself</p>
              <small class="text-muted">अपना पंजीकरण करें</small>
            </div>
          </div>
          <div class="col-md-4">
            <div class="mini-step text-center">
              <div class="step-num shadow-sm">3</div>
              <p class="fw-bold mb-0">Verify Phone Number</p>
              <small class="text-muted">फोन नंबर सत्यापित करें</small>
            </div>
          </div>
        </div>
      </div>

      <div class="text-center">
        <router-link to="/register" class="btn btn-danger btn-lg w-100 py-3 fw-800 rounded-4 shadow">
          PROCEED TO REGISTER <i class="fas fa-arrow-right ms-2"></i>
        </router-link>
        <p class="mt-3 smaller text-muted italic">Registration takes less than 60 seconds.</p>
      </div>
    </div>
  </div>
</div>


<!-- Blood Bank Finder Modal -->
<div v-if="showBloodBankModal" class="modal-overlay" @click.self="showBloodBankModal = false">
  <div class="registration-card shadow-lg">
    <button class="close-btn" @click="showBloodBankModal = false">
      <i class="fas fa-times"></i>
    </button>

    <div class="card-body p-4 p-md-5">

      <!-- Step 1 — Asking for location -->
      <div v-if="locationStep === 'ask'" class="text-center">
        <div class="icon-circle mb-3">
          <i class="fas fa-map-marker-alt text-danger"></i>
        </div>
        <h3 class="fw-800 mb-2">Find Nearest Blood Bank</h3>
        <p class="text-muted small mb-4">
          Allow location access to find verified blood banks and hospitals near you in real time.
        </p>
        <button class="btn btn-danger btn-lg w-100 py-3 fw-800 rounded-4 shadow" @click="getLocation">
          <i class="fas fa-location-arrow me-2"></i> Allow Location Access
        </button>
        <button class="btn btn-light w-100 py-2 mt-3 rounded-4" @click="showBloodBankModal = false">
          Cancel
        </button>
      </div>

      <!-- Step 2 — Loading -->
      <div v-if="locationStep === 'loading'" class="text-center py-4">
        <div class="spinner-border text-danger mb-3" role="status"></div>
        <p class="fw-bold">Finding blood banks near you...</p>
        <p class="text-muted small">Please wait while we search our network</p>
      </div>

      <!-- Step 3 — Results -->
      <div v-if="locationStep === 'results'">
        <div class="d-flex align-items-center mb-4">
          <i class="fas fa-map-marker-alt text-danger me-2"></i>
          <h5 class="fw-800 mb-0">Nearest Blood Banks</h5>
          <span class="badge bg-danger ms-auto">{{ nearbyBanks.length }} Found</span>
        </div>

        <!-- Banks list -->
        <div v-if="nearbyBanks.length > 0" class="bank-list mb-4">
          <div
            v-for="bank in nearbyBanks"
            :key="bank.id"
            class="bank-card d-flex align-items-center p-3 mb-3 rounded-4 border shadow-sm"
          >
            <div class="bank-icon me-3">
              <i class="fas fa-hospital text-danger fa-lg"></i>
            </div>
            <div class="flex-grow-1">
              <h6 class="fw-bold mb-0">{{ bank.hospital_name }}</h6>
              <small class="text-muted">
                <i class="fas fa-map-marker-alt me-1"></i>{{ bank.city }}
                <span class="ms-2 text-danger fw-bold">
                  <i class="fas fa-route me-1"></i>{{ bank.distance_km }} km away
                </span>
              </small>
              <div class="mt-1">
                <span
                  v-for="(qty, group) in bank.stock"
                  :key="group"
                  :class="['badge rounded-pill me-1 small', qty > 5 ? 'bg-success' : qty > 0 ? 'bg-warning text-dark' : 'bg-danger']"
                >
                  {{ group }}: {{ qty }}u
                </span>
              </div>
            </div>
            <div class="ms-2 text-muted">
              <i class="fas fa-chevron-right"></i>
            </div>
          </div>
        </div>

        <!-- Not available -->
        <div v-else class="text-center py-4 mb-3">
          <div class="icon-circle mb-3 mx-auto" style="background:#fff1f1">
            <i class="fas fa-hospital-slash text-danger"></i>
          </div>
          <h5 class="fw-bold">No Blood Banks Found Nearby</h5>
          <p class="text-muted small">
            No verified partners found within 20km of your location.
            Raise a request and our network will find donors for you!
          </p>
        </div>

        <!-- Bottom buttons -->
        <router-link to="/register" class="btn btn-danger w-100 py-3 fw-800 rounded-4 shadow mb-2">
          <i class="fas fa-arrow-right me-2"></i>
          Proceed to Register / Login to Raise a Request
        </router-link>
        <button class="btn btn-light w-100 py-2 rounded-4" @click="showBloodBankModal = false">
          Cancel
        </button>
      </div>

      <!-- Step 4 — Location denied -->
      <div v-if="locationStep === 'denied'" class="text-center py-4">
        <div class="icon-circle mb-3 mx-auto" style="background:#fff1f1">
          <i class="fas fa-location-slash text-danger"></i>
        </div>
        <h5 class="fw-bold">Location Access Denied</h5>
        <p class="text-muted small mb-4">
          Please allow location access in your browser settings to find nearby blood banks.
        </p>
        <button class="btn btn-danger w-100 py-3 fw-800 rounded-4" @click="getLocation">
          <i class="fas fa-redo me-2"></i> Try Again
        </button>
        <button class="btn btn-light w-100 py-2 mt-2 rounded-4" @click="showBloodBankModal = false">
          Cancel
        </button>
      </div>

    </div>
  </div>
</div>

    
  </div>
</template>

<script>
export default {
    methods: {
  urgencyClass(level) {
    switch(level) {
      case 'CRITICAL': return 'bg-danger text-white';
      case 'URGENT': return 'bg-warning text-dark';
      default: return 'bg-light text-muted border';
    }
  },
  toggleRaiseModal() {
    this.showRaiseModal = !this.showRaiseModal;
  },
  openBloodBankFinder() {
    this.showBloodBankModal = true
    this.locationStep = 'ask'
    this.nearbyBanks = []
},

getLocation() {
    if (!navigator.geolocation) {
        this.locationStep = 'denied'
        return
    }

    this.locationStep = 'loading'

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            this.userLat = position.coords.latitude
            this.userLng = position.coords.longitude
            await this.fetchNearbyBanks()
        },
        (error) => {
            console.error('Location error:', error)
            this.locationStep = 'denied'
        }
    )
},

async fetchNearbyBanks() {
    try {
        const response = await fetch(
            `http://127.0.0.1:8000/api/partners/nearby/?lat=${this.userLat}&lng=${this.userLng}&radius=20`
        )
        const data = await response.json()
        this.nearbyBanks = data
        this.locationStep = 'results'
    } catch (error) {
        console.error('Error fetching banks:', error)
        this.nearbyBanks = []
        this.locationStep = 'results'
    }
},
},
  data() {
    
    return {
        showRaiseModal: false,
        showBloodBankModal: false,
locationStep: 'ask',    
nearbyBanks: [],
userLat: null,
userLng: null,
      tickerStats: [
        { val: '1,243', label: 'Donors Online' },
        { val: '34', label: 'Active Requests' },
        { val: '12', label: 'Blood Banks' },
        { val: '2.4K', label: 'Daily Insured' }
      ],
      howItWorksSteps: [
  { 
    icon: 'fas fa-user-plus', 
    title: 'Register', 
    description: 'Join the network as a verified donor in less than 2 minutes. Your data is encrypted and secure.' 
  },
  { 
    icon: 'fas fa-bell', 
    title: 'Get Notified', 
    description: 'Receive instant WhatsApp and SMS alerts only when someone in your vicinity needs your blood type.' 
  },
  { 
    icon: 'fas fa-hand-holding-heart', 
    title: 'Donate & Save', 
    description: 'Coordinate via our secure platform, visit the hospital, and save a life. Every drop creates an impact.' 
  }
],
      trustCards: [
        { 
          icon: 'fas fa-user-shield', 
          title: 'Anonymous Donation', 
          desc: 'Your identity is protected until you choose to reveal it to the medical facility.' 
        },
        { 
          icon: 'fas fa-comment-dots', 
          title: 'Real-time Alerts', 
          desc: 'Instant multi-channel notifications ensure zero delay in emergency situations.' 
        },
        { 
          icon: 'fas fa-check-square', 
          title: 'Verified Partners', 
          desc: 'We only connect with NABH-accredited hospitals and certified blood banks.' 
        },
        { 
          icon: 'fas fa-award', 
          title: 'Reliability Score', 
          desc: 'Transparent metrics for banks and donors to maintain highest network standards.' 
        }
      ],
      steps: [
        { icon: 'fas fa-user-plus', title: 'Register', desc: 'Join the network as a verified donor in less than 2 minutes. Your data is encrypted and secure.' },
        { icon: 'fas fa-bullhorn', title: 'Get Notified', desc: 'Receive instant WhatsApp and SMS alerts only when someone in your vicinity needs your blood type.' },
        { icon: 'fas fa-hand-holding-heart', title: 'Donate & Save', desc: 'Coordinate via our secure platform, visit the hospital, and save a life. Every drop creates an impact.' }
      ],
      routingFeatures: [
        { icon: 'fas fa-link', title: 'Instant Reference', desc: 'A donor finds a blood bank and receives a unique Life-Link Reference Number for verification.' },
        { icon: 'fas fa-database', title: 'Smart Stock Backup', desc: 'Low stock triggers an automatic Instant Broadcast to all verified donors within a 5km radius.' },
        { icon: 'fas fa-hospital', title: 'Partner Bridge', desc: 'Simultaneously, the system contacts the nearest partner hospitals to facilitate automated emergency stock transfer.' }
      ],
      requests: [
        { id: 1, group: 'O-', urgency: 'CRITICAL', hospital: 'AIIMS Trauma Center', city: 'New Delhi', time: '2 mins ago' },
        { id: 2, group: 'B+', urgency: 'URGENT', hospital: 'Apollo Hospital', city: 'Hyderabad', time: '15 mins ago' }
      ],
      donors: [
        { id: '01', tag: '#7721', tier: 'PLATINUM', year: '2022', donations: '24' },
        { id: '02', tag: '#8904', tier: 'GOLD', year: '2023', donations: '16' }
      ],
      impactStats: [
        { val: '10,000+', label: 'Verified Donors' },
        { val: '500+', label: 'Blood Banks' },
        { val: '2,400+', label: 'Lives Impacted' },
        { val: '28', label: 'States Active' }
      ],
      
    }
  }
}
</script>

<style scoped>
/* GENERAL STYLES */
.fw-800 { font-weight: 800; }
.smaller { font-size: 0.75rem; }
.jeevandaan-platform { font-family: 'Inter', sans-serif; background-color: #fcfcfc; }

/* Typography & Spacing */
.fw-800 { font-weight: 800; }
.smaller-badge { font-size: 0.65rem; letter-spacing: 0.5px; }

/* Map Specifics */
.map-wrapper { min-height: 450px; }
.blur-btn {
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}
.blur-btn:hover {
  transform: scale(1.05);
  background: #fff !important;
}

/* Status Dots */
.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

/* Red Pulse for Critical Requests */
.pulse-red {
  background: #D32F2F;
  box-shadow: 0 0 0 rgba(211, 47, 47, 0.4);
  animation: pulse-red 2s infinite;
}

@keyframes pulse-red {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(211, 47, 47, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(211, 47, 47, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(211, 47, 47, 0); }
}

/* Hover Effects */
.transition-hover {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.transition-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
}

/* Scroll Area for Live Requests (if there are many) */
.request-scroll-area {
  max-height: 550px;
  overflow-y: auto;
}
.request-scroll-area::-webkit-scrollbar {
  width: 4px;
}
.request-scroll-area::-webkit-scrollbar-thumb {
  background: #e0e0e0;
  border-radius: 10px;
}

/* HERO */
.hero-bg { background-color: #fafafa; }
.emergency-tag {
  display: inline-flex;
  align-items: center;
  background: #fff;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 900;
  color: #D32F2F;
  border: 1px solid #eee;
}
.emergency-tag .dot {
  width: 6px; height: 6px; background: #D32F2F; border-radius: 50%; margin-right: 8px;
}

.hero-img-wrapper { position: relative; border-radius: 20px; }
.hero-img-wrapper img { width: 100%; border-radius: 20px; filter: grayscale(20%); }

.verified-badge {
  position: absolute; bottom: 20px; left: 20px; right: 20px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  padding: 15px; border-radius: 12px;
}
.badge-icon { background: #E8F5E9; color: #2ECC71; padding: 10px; border-radius: 10px; }

/* ROUTING ENGINE */
.routing-section { background: #D32F2F; }
.routing-card {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 30px; border-radius: 20px; height: 100%;
}
.step-num { width: 30px; height: 30px; background: #fff; color: #D32F2F; border-radius: 5px; display: flex; align-items: center; justify-content: center; font-weight: 900; margin-bottom: 20px; }
.ticker-pill { background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.1); }

/* MAP */
.map-container { height: 450px; background: url('https://upload.wikimedia.org/wikipedia/commons/e/ea/BlankMap-World6.svg') center; background-size: cover; }
.map-legend .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }

/* PULSING ANIMATIONS */
.pulse-red {
  width: 8px; height: 8px; background: #D32F2F; border-radius: 50%;
  box-shadow: 0 0 0 rgba(211, 47, 47, 0.4); animation: pulse 2s infinite;
}


/* IMPACT SECTION */
.tracking-wider { letter-spacing: 0.1rem; }
.tracking-widest { letter-spacing: 0.2rem; }

/* LOGOS */
.logo-placeholder {
  height: 40px;
  background: #eee;
  border-radius: 4px;
  opacity: 0.6;
}
.italic { font-style: italic; }

/* LEADERBOARD */
.donor-row { transition: transform 0.2s; cursor: pointer; }
.donor-row:hover { transform: scale(1.01); }
.rank-badge {
  width: 45px; height: 45px;
  background: #f8f9fa;
  border-radius: 12px;
  color: #adb5bd;
}
.smaller-badge { font-size: 0.65rem; padding: 4px 10px; font-weight: 800; }
.bg-danger-light { background-color: #ffebee; }
.bg-info-light { background-color: #e0f7fa; }

/* EMERGENCY CTA */
.cta-banner {
  background-color: #D32F2F;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.pattern-overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0);
  background-size: 24px 24px;
}
.btn-dark-red {
  background-color: #9b1c1c;
  color: white;
  border: 1px solid rgba(255,255,255,0.2);
}
.btn-dark-red:hover { background-color: #7a1515; color: white; }

/* Styling for the Trust Cards */
.trust-card {
  transition: all 0.3s ease;
  background-color: #fff;
  /* Matching the image's extra-rounded look */
  border-radius: 2rem !important; 
  border: 1px solid #f1f1f1 !important;
}

.trust-card:hover {
  transform: translateY(-8px);
  border-color: #D32F2F !important;
}

.trust-icon {
  font-size: 2rem;
  color: #D32F2F;
  /* Container for icon alignment */
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Matching the bold typography from the screenshot */
.fw-800 {
  font-weight: 800;
  letter-spacing: -0.02em;
}

.text-muted {
  color: #6c757d !important;
  line-height: 1.6;
}
.step-item {
  /* Added padding for mobile stacking */
  padding: 10px;
}

.icon-box {
  width: 80px;
  height: 80px;
  background-color: #f0f0f0; /* Soft gray from your design */
  border-radius: 20px; /* Modern rounded corners */
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  color: #D32F2F; /* Primary Deep Red */
}

.fw-800 {
  font-weight: 800;
  letter-spacing: -0.02em;
}

.step-desc {
  font-size: 1rem;
  line-height: 1.6;
  color: #6c757d;
  max-width: 90%; /* Keeps text blocks from getting too wide */
}

/* Modal Overlay Background */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000; /* Higher than sticky-top navbar */
  padding: 20px;
}

/* The Card Styling */
.registration-card {
  background: white;
  width: 100%;
  max-width: 700px;
  border-radius: 30px;
  position: relative;
  border-top: 8px solid #D32F2F;
}

/* Close Button (Upper Right) */
.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: #f8f9fa;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: #666;
  transition: all 0.2s;
}
.close-btn:hover {
  background: #D32F2F;
  color: white;
  transform: rotate(90deg);
}

/* Step Circles */
.icon-circle {
  width: 60px;
  height: 60px;
  background: #fff1f1;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  font-size: 1.5rem;
}

.step-num {
  width: 35px;
  height: 35px;
  background: white;
  border: 2px solid #D32F2F;
  color: #D32F2F;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  font-weight: 800;
}

.mini-step {
  padding: 15px;
  border-radius: 20px;
  transition: background 0.3s;
}
.mini-step:hover {
  background: #fafafa;
}

/* Animations (Optional: requires Animate.css) */
.animate__animated {
  animation-duration: 0.4s;
}

.bank-card {
    transition: all 0.2s ease;
    cursor: pointer;
}
.bank-card:hover {
    transform: translateY(-2px);
    border-color: #D32F2F !important;
    box-shadow: 0 8px 20px rgba(211, 47, 47, 0.1) !important;
}
.bank-icon {
    width: 45px;
    height: 45px;
    background: #fff1f1;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.bank-list {
    max-height: 350px;
    overflow-y: auto;
}
.bank-list::-webkit-scrollbar {
    width: 4px;
}
.bank-list::-webkit-scrollbar-thumb {
    background: #e0e0e0;
    border-radius: 10px;
}

/* Responsive adjustment for center alignment on mobile if needed */
@media (max-width: 768px) {
  .step-item {
    text-align: center;
  }
  .icon-box {
    margin-left: auto;
    margin-right: auto;
  }
  .step-desc {
    margin-left: auto;
    margin-right: auto;
  }
}

.z-index-1 { z-index: 1; }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(211, 47, 47, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(211, 47, 47, 0); } 100% { box-shadow: 0 0 0 0 rgba(211, 47, 47, 0); } }

/* FINAL CTA */
.final-cta-card { background: #D32F2F; }
.btn-dark-red { background: #a32424; color: white; border: 1px solid rgba(255,255,255,0.2); }
.bg-danger-soft { background: #fff1f1; }
.donor-leader-card .rank-box { background: #f0f0f0; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 900; color: #666; }
</style>




