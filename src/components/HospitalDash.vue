<template>
  <div class="partner-portal d-flex flex-column flex-md-row min-vh-100">
    
    <div class="d-md-none bg-white border-bottom px-3 py-2 d-flex justify-content-between align-items-center sticky-top shadow-sm z-3">
      <div class="d-flex align-items-center">
        <div class="logo-box me-2">JD+</div>
        <span class="fw-bold text-dark">Partner<span class="text-sky">Hub</span></span>
      </div>
      <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="btn border-0 text-sky">
        <i :class="isMobileMenuOpen ? 'fas fa-times fs-3' : 'fas fa-bars fs-3'"></i>
      </button>
    </div>

    <aside :class="['sidebar bg-white border-end shadow-sm', isMobileMenuOpen ? 'show' : '']">
      <div class="p-4 d-none d-md-flex align-items-center mb-3">
        <div class="logo-box me-2">JD+</div>
        <h5 class="fw-bold mb-0">Partner<span class="text-sky">Hub</span></h5>
      </div>

      <nav class="nav flex-column gap-1 px-3">
        <button v-for="item in menuItems" :key="item.id" 
                @click="navigate(item.id)"
                :class="['nav-link menu-btn', activeTab === item.id ? 'active' : '']">
          <i :class="[item.icon, 'me-3']"></i> 
          <span>{{ item.label }}</span>
          <span v-if="item.id === 'notifications' && unreadNotifs > 0" class="badge rounded-pill bg-danger ms-auto">{{ unreadNotifs }}</span>
        </button>
      </nav>

      <div class="mt-auto p-4 border-top">
    <div class="license-status bg-light p-3 rounded-4 d-flex align-items-center">
        <i :class="['me-2', partner.is_live ? 'fas fa-check-circle text-success' : 'fas fa-clock text-warning']"></i>
        <div>
            <small class="text-muted d-block smallest">License Status</small>
            <span class="fw-bold small">
                {{ partner.is_live ? 'ACTIVE & VERIFIED' : 'PENDING VERIFICATION' }}
            </span>
        </div>
    </div>
</div>
    </aside>

    <main class="main-body flex-grow-1 bg-light-blue">

      <!-- Loading -->
<div v-if="loading" class="d-flex align-items-center justify-content-center min-vh-100">
    <div class="text-center">
        <div class="spinner-border text-sky mb-3" style="width:3rem;height:3rem"></div>
        <p class="text-muted fw-bold">Loading Partner Dashboard...</p>
    </div>
</div>

<!-- Error -->
<div v-else-if="error" class="d-flex align-items-center justify-content-center min-vh-100">
    <div class="text-center">
        <i class="fas fa-exclamation-triangle text-danger fs-1 mb-3"></i>
        <p class="text-danger fw-bold">{{ error }}</p>
        <button class="btn btn-sky rounded-pill px-4" @click="fetchProfile">
            <i class="fas fa-redo me-2"></i> Retry
        </button>
    </div>
</div>

<!-- Main content — only show when loaded -->


      <header class="bg-white px-4 py-3 border-bottom d-none d-md-flex justify-content-between align-items-center sticky-top z-2">
    <h4 class="fw-bold mb-0">{{ currentLabel }}</h4>
    <div class="d-flex align-items-center gap-3">

      
        <div v-if="loading" class="spinner-border spinner-border-sm text-sky"></div>

        <!-- Real partner data -->
        <div v-else class="text-end">
            <p class="mb-0 fw-bold small">{{ partner.hospital_name }}</p>
            <p class="mb-0 smallest text-muted">{{ partner.city }}, {{ partner.state }}</p>
        </div>

        <!-- Dynamic initials avatar -->
        <div class="avatar-circle shadow-sm">{{ partnerInitials }}</div>
    </div>
</header>

      <div class="p-3 p-md-4">
        
        <section v-if="activeTab === 'overview'" class="animate-fade">
          <div class="row g-2 g-md-3 mb-4">
            <div class="col-6 col-lg-3" v-for="(qty, group) in stock" :key="group">
              <div class="card border-0 shadow-sm p-3 stock-card">
                <div class="d-flex justify-content-between">
                  <span class="badge bg-sky-soft text-sky fw-bold">{{ group }}</span>
                  <span v-if="qty < 5" class="text-danger smallest fw-bold"><i class="fas fa-arrow-down"></i> LOW</span>
                </div>
                <h3 class="fw-800 my-2">{{ qty }} <small class="text-muted h6">Units</small></h3>
                <div class="progress" style="height: 4px;">
                  <div class="progress-bar bg-sky" :style="{width: (qty/30)*100 + '%'}"></div>
                </div>
              </div>
            </div>
          </div>

          <div class="row g-3">
            <div class="col-12 col-md-6 col-lg-3" v-for="stat in overviewStats" :key="stat.label">
              <div class="card border-0 shadow-sm p-4 rounded-4 h-100">
                <h6 class="text-muted smallest fw-bold mb-1">{{ stat.label }}</h6>
                <h3 class="fw-bold mb-0" :class="stat.color">{{ stat.val }}</h3>
              </div>
            </div>
          </div>

          <div class="card border-0 shadow-sm rounded-4 p-4 mt-4">
            <h5 class="fw-bold mb-3">Recent Donations Received</h5>
            <div class="table-responsive">
              <table class="table table-hover align-middle">
                <thead class="bg-light">
                  <tr><th>Ref ID</th><th>Donor</th><th>Group</th><th>Fee Status</th></tr>
                </thead>
                <tbody>
                  <tr v-for="n in 3" :key="n">
                    <td class="text-sky fw-bold">#JD-88{{ n }}</td>
                    <td class="small">Donor_User_{{ n }}</td>
                    <td><span class="badge bg-light text-dark">O+</span></td>
                    <td><span class="badge bg-success-subtle text-success">Paid</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <section v-if="activeTab === 'stock'" class="animate-fade">
    <div class="card border-0 shadow-sm rounded-4 p-4 mb-4">
        <h5 class="fw-bold mb-4">Update Inventory Level</h5>

        <div class="row g-3">
            <div class="col-md-4 col-sm-6" v-for="(qty, group) in stock" :key="group">
                <div class="input-group mb-2">
                    <span class="input-group-text bg-sky text-white fw-bold" style="width:50px">
                        {{ group }}
                    </span>
                    <input
                        type="number"
                        v-model.number="stock[group]"
                        class="form-control border-light-blue"
                        placeholder="Qty"
                        min="0"
                    >
                    <button
                        class="btn btn-sky-outline fw-bold"
                        @click="updateStock(group)"
                        :disabled="updatingStock === group"
                    >
                        <span v-if="updatingStock === group">
                            <span class="spinner-border spinner-border-sm"></span>
                        </span>
                        <span v-else>Update</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- Success/Error message -->
        <div v-if="stockMessage" :class="['alert mt-3 rounded-4 border-0', stockMessage.type === 'success' ? 'alert-success' : 'alert-danger']">
            <i :class="['me-2', stockMessage.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle']"></i>
            {{ stockMessage.text }}
        </div>
    </div>

    <!-- Stock History -->
    <div class="card border-0 shadow-sm rounded-4 p-4">
        <h6 class="fw-bold text-muted mb-3">
            <i class="fas fa-history me-2"></i>Stock History Log
        </h6>

        <div v-if="stockHistory.length === 0" class="timeline-placeholder p-4 border-dashed rounded-4 text-center text-muted small">
            No recent changes logged in the last 24 hours.
        </div>

        <div v-else class="list-group list-group-flush">
            <div
                v-for="log in stockHistory"
                :key="log.id"
                class="list-group-item px-0 py-2 bg-transparent d-flex justify-content-between"
            >
                <div>
                    <span class="badge bg-sky-soft text-sky me-2">{{ log.blood_group }}</span>
                    <small class="fw-bold">{{ log.quantity }} units</small>
                </div>
                <small class="text-muted">{{ timeAgo(log.updated_at) }}</small>
            </div>
        </div>
    </div>
</section>

        <section v-if="activeTab === 'raise-donor'" class="animate-fade">
    <div class="row g-4">
        <div class="col-lg-5">
            <div class="card border-0 shadow-sm rounded-4 p-4">
                <h5 class="fw-bold mb-4">Find Emergency Donors</h5>

                <div class="mb-3">
                    <label class="small fw-bold mb-1">Blood Group</label>
                    <select class="form-select border-0 bg-light py-3" v-model="donorRequest.blood_group">
                        <option disabled value="">Select Blood Group</option>
                        <option v-for="(_, g) in stock" :key="g">{{ g }}</option>
                    </select>
                </div>

                <div class="mb-4">
                    <label class="small fw-bold mb-1">Units Needed</label>
                    <input
                        type="number"
                        class="form-control border-0 bg-light py-3"
                        placeholder="0"
                        v-model.number="donorRequest.quantity"
                        min="1"
                    >
                </div>

                <!-- Success/Error -->
                <div v-if="donorRequestMessage" :class="['alert border-0 rounded-4 mb-3', donorRequestMessage.type === 'success' ? 'alert-success' : 'alert-danger']">
                    <i :class="['me-2', donorRequestMessage.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle']"></i>
                    {{ donorRequestMessage.text }}
                </div>

                <button
                    class="btn btn-sky w-100 py-3 fw-bold rounded-3"
                    @click="broadcastDonorRequest"
                    :disabled="broadcastLoading || !donorRequest.blood_group || !donorRequest.quantity"
                >
                    <span v-if="broadcastLoading">
                        <span class="spinner-border spinner-border-sm me-2"></span>
                        Broadcasting...
                    </span>
                    <span v-else>
                        <i class="fas fa-bullhorn me-2"></i>
                        BROADCAST NOTIFICATION
                    </span>
                </button>
            </div>

            <!-- Active requests list -->
            <div class="card border-0 shadow-sm rounded-4 p-4 mt-4" v-if="activeDonorRequests.length > 0">
                <h6 class="fw-bold mb-3">Your Active Requests</h6>
                <div
                    v-for="req in activeDonorRequests"
                    :key="req.id"
                    class="p-3 bg-light rounded-4 mb-2 d-flex justify-content-between align-items-center"
                >
                    <div>
                        <span class="badge bg-sky-soft text-sky fw-bold me-2">{{ req.blood_group }}</span>
                        <small class="fw-bold">{{ req.quantity }} units</small>
                        <small class="text-muted ms-2">{{ timeAgo(req.created_at) }}</small>
                    </div>
                    <span :class="['badge rounded-pill', req.status === 'open' ? 'bg-warning text-dark' : req.status === 'assigned' ? 'bg-success' : 'bg-danger']">
                        {{ req.status }}
                    </span>
                </div>
            </div>
        </div>

        <div class="col-lg-7">
            <div class="card border-0 shadow-sm rounded-4 p-4 h-100">
                <h6 class="fw-bold mb-3">
                    Accepted Donors / Live Chat
                    <span v-if="selectedDonorRequest" class="badge bg-sky ms-2">
                        {{ selectedDonorRequest.blood_group }} — {{ selectedDonorRequest.quantity }} units
                    </span>
                </h6>

                <!-- No request selected -->
                <div v-if="!selectedDonorRequest" class="alert bg-sky-soft text-sky border-0 small">
                    <i class="fas fa-info-circle me-2"></i>
                    No active donor responses yet. Broadcast a request first.
                </div>

                <!-- Chat section -->
                <div v-else>
                    <!-- Chat messages -->
                    <div class="chat-area bg-light rounded-4 p-3 mb-3" style="height:300px;overflow-y:auto">
                        <div v-if="chatMessages.length === 0" class="text-center text-muted small py-5">
                            No messages yet — waiting for donor response
                        </div>
                        <div
                            v-for="msg in chatMessages"
                            :key="msg.id"
                            :class="['d-flex mb-3', msg.sender_type === 'partner' ? 'justify-content-end' : 'justify-content-start']"
                        >
                            <div :class="['chat-bubble px-3 py-2 rounded-4', msg.sender_type === 'partner' ? 'bg-sky text-white' : 'bg-white border']">
                                <small class="fw-bold">{{ msg.message_display }}</small>
                                <div class="smallest opacity-75">{{ timeAgo(msg.sent_at) }}</div>
                            </div>
                        </div>
                    </div>

                    <!-- Default message buttons -->
                    <div class="d-flex flex-wrap gap-2">
                        <button
                            v-for="msg in defaultMessages"
                            :key="msg.value"
                            class="btn btn-sky-outline btn-sm rounded-pill"
                            @click="sendChatMessage(msg.value)"
                            :disabled="sendingMessage"
                        >
                            {{ msg.label }}
                        </button>
                    </div>

                    <!-- Verify donation button -->
                    <div class="mt-3" v-if="selectedDonorRequest.status === 'assigned'">
                        <button
                            class="btn btn-success w-100 py-3 fw-bold rounded-3"
                            @click="verifyDonation(selectedDonorRequest.id)"
                            :disabled="verifyingDonation"
                        >
                            <span v-if="verifyingDonation">
                                <span class="spinner-border spinner-border-sm me-2"></span>
                                Verifying...
                            </span>
                            <span v-else>
                                <i class="fas fa-check-double me-2"></i>
                                Confirm Donation Received
                            </span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

        <section v-if="activeTab === 'view-attender'" class="animate-fade">
          <div class="card border-0 shadow-sm rounded-4 p-4 p-md-5 text-center mb-4 sky-gradient text-white">
            <h4 class="fw-800">Regional Attender Lookup</h4>
            <p class="opacity-75">Enter the Reference Number to find blood requests in Varanasi.</p>
            <div class="input-group mt-4 mx-auto shadow-lg rounded-pill overflow-hidden" style="max-width: 500px;">
              <input type="text" class="form-control border-0 px-4 py-3" placeholder="Reference Number (e.g. JD-2026-X89)">
              <button class="btn btn-white px-4 fw-bold text-sky">SEARCH</button>
            </div>
          </div>
          <div class="d-flex gap-2 mb-3 overflow-auto pb-2">
            <button class="btn btn-white btn-sm shadow-sm rounded-pill px-3 fw-bold">All Groups</button>
            <button class="btn btn-white btn-sm shadow-sm rounded-pill px-3 fw-bold text-danger">Critical Only</button>
          </div>
          <div class="row g-3">
            <div class="col-md-6" v-for="req in [1, 2]" :key="req">
              <div class="card border-0 shadow-sm rounded-4 p-3">
                <div class="d-flex justify-content-between mb-2">
                  <span class="badge bg-light text-sky border">REF: JD-102{{ req }}</span>
                  <span class="badge bg-warning rounded-pill">Urgent</span>
                </div>
                <h6 class="fw-bold mb-1">Hospital Request: Heritage Varanasi</h6>
                <p class="smallest text-muted mb-3">O+ Needed | 2 Units | Document Verified</p>
                <button class="btn btn-sky btn-sm w-100 fw-bold">Accept Request (Fulfilling)</button>
              </div>
            </div>
          </div>
        </section>

        <section v-if="activeTab === 'verify'" class="animate-fade">
          <div class="card border-0 shadow-sm rounded-4 p-4">
            <h5 class="fw-bold mb-4">Donation Verification Terminal</h5>
            <div class="row align-items-center bg-light p-4 rounded-4">
              <div class="col-md-8">
                <h6 class="fw-bold">Scan QR or Enter Donor Code</h6>
                <input type="text" class="form-control form-control-lg border-0 shadow-sm mt-3" placeholder="Enter Code">
              </div>
              <div class="col-md-4 mt-3 mt-md-0">
                <button class="btn btn-success w-100 py-3 fw-bold rounded-3">VERIFY & CONFIRM</button>
              </div>
            </div>
          </div>
        </section>

        <section v-if="activeTab === 'notifications'" class="animate-fade">
          <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
            <div v-for="n in notifs" :key="n.id" class="p-3 border-bottom d-flex align-items-start gap-3">
              <div :class="['notif-icon', n.bg]"><i :class="n.icon"></i></div>
              <div>
                <p class="mb-0 fw-bold small text-dark">{{ n.title }}</p>
                <p class="mb-0 smallest text-muted">{{ n.desc }}</p>
                <small class="smallest opacity-50">{{ n.time }}</small>
              </div>
            </div>
          </div>
        </section>

        <section v-if="activeTab === 'profile'" class="animate-fade">
          <div class="row g-4">
            <div class="col-md-7">
              <div class="card border-0 shadow-sm rounded-4 p-4">
                <h5 class="fw-bold mb-4">Facility Information</h5>
                <div class="row g-3">
                  <div class="col-12"><label class="smallest fw-bold text-muted">Facility Name</label><input type="text" class="form-control border-light-blue" value="City General Bank"></div>
                  <div class="col-md-6"><label class="smallest fw-bold text-muted">Convenience Fee (₹)</label><input type="number" class="form-control border-light-blue" value="250"></div>
                  <div class="col-md-6"><label class="smallest fw-bold text-muted">Contact No.</label><input type="text" class="form-control border-light-blue" value="+91 9988776655"></div>
                </div>
                <button class="btn btn-sky mt-4 px-5 fw-bold">Save Changes</button>
              </div>
            </div>
            <div class="col-md-5">
              <div class="card border-0 shadow-sm rounded-4 p-4 text-center h-100">
                <h6 class="fw-bold text-muted mb-4">License & Documents</h6>
                <div class="bg-success-subtle p-3 rounded-4 mb-3">
                  <i class="fas fa-file-contract text-success fa-2x mb-2"></i>
                  <p class="mb-0 fw-bold small text-success">UP-BAN-82192-B</p>
                  <small class="smallest text-success">Validated till 2028</small>
                </div>
                <button class="btn btn-light-blue text-sky btn-sm fw-bold w-100">View Digital License</button>
              </div>
            </div>
          </div>
        </section>

        <section v-if="activeTab === 'camps'" class="animate-fade">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h5 class="fw-bold mb-0">Upcoming Donation Camps</h5>
            <button class="btn btn-sky fw-bold btn-sm rounded-pill px-4">+ Schedule Camp</button>
          </div>
          <div class="row g-3">
            <div class="col-md-6 col-lg-4" v-for="c in [1, 2]" :key="c">
              <div class="card border-0 shadow-sm rounded-4 p-3">
                <div class="d-flex align-items-center gap-3 mb-3">
                  <div class="date-box">15<br><small>APR</small></div>
                  <div>
                    <h6 class="fw-bold mb-0">Bishnu Plaza Mega Camp</h6>
                    <p class="smallest text-muted mb-0">Location: Varanasi Cantt</p>
                  </div>
                </div>
                <div class="d-flex gap-2">
                  <button class="btn btn-sky-outline btn-sm flex-grow-1">Edit</button>
                  <button class="btn btn-sky btn-sm flex-grow-1">Share Info</button>
                </div>
              </div>
            </div>
          </div>
        </section>

      </div>
    </main>

    <div v-if="isMobileMenuOpen" @click="isMobileMenuOpen = false" class="mobile-overlay"></div>
  </div>
</template>

<script>
import api from '@/api/index.js'

export default {
    data() {
        return {
            activeTab: 'overview',
            isMobileMenuOpen: false,
            unreadNotifs: 0,
            partner: {},          // ← real partner data from API
            loading: true,
            error: null,
            updatingStock: null,     
            stockMessage: null,       
            stockHistory: [],  
            notifs: [],              
        overviewStats: [],       
        partnerRequests: [],      

            // Stock from API
            stock: {
                'A+': 0, 'A-': 0,
                'B+': 0, 'B-': 0,
                'O+': 0, 'O-': 0,
                'AB+': 0, 'AB-': 0
            },
                                            // Raise donor request
            donorRequest: {
                 blood_group: '',
                  quantity: 1
                  },
                broadcastLoading: false,
                donorRequestMessage: null,
                activeDonorRequests: [],
                selectedDonorRequest: null,

// Chat
chatMessages: [],
sendingMessage: false,
verifyingDonation: false,

// Default chat messages
defaultMessages: [
    { value: 'on_the_way', label: '🚗 On my way' },
    { value: 'reached', label: '📍 Reached' },
    { value: 'unable_to_come', label: '❌ Unable to come' },
    { value: 'delayed', label: '⏰ Running late' },
    { value: 'donated', label: '✅ Donation done' },
],

            

            
            menuItems: [
                { id: 'overview', label: 'Overview', icon: 'fas fa-th-large' },
                { id: 'stock', label: 'Stock Mgmt', icon: 'fas fa-boxes' },
                { id: 'raise-donor', label: 'Raise Donor', icon: 'fas fa-bullhorn' },
                { id: 'view-attender', label: 'Attender Feed', icon: 'fas fa-user-injured' },
                { id: 'verify', label: 'Verify Donation', icon: 'fas fa-check-double' },
                { id: 'notifications', label: 'Alerts', icon: 'fas fa-bell' },
                { id: 'camps', label: 'Camp Schedule', icon: 'fas fa-campground' },
                { id: 'profile', label: 'My Facility', icon: 'fas fa-hospital-user' },
                { id: 'logout', label: 'Logout', icon: 'fas fa-sign-out-alt' },
            ],

            
        }
    },

    computed: {
        currentLabel() {
            return this.menuItems.find(i => i.id === this.activeTab)?.label || ''
        },

        // Partner initials for avatar
        partnerInitials() {
            if (!this.partner.hospital_name) return 'JD'
            return this.partner.hospital_name
                .split(' ')
                .map(w => w[0])
                .join('')
                .substring(0, 2)
                .toUpperCase()
        }
    },

    mounted() {
        this.checkAuth()
        this.savePartnerGPS()
    },

    methods: {
        // ── Auth guard ──────────────────────────
        checkAuth() {
            const token = localStorage.getItem('access_token')
            const userType = localStorage.getItem('user_type')

            if (!token || userType !== 'partner') {
                this.$router.push('/partners/login')
                return
            }
            this.fetchProfile()
        },
        

        // ── Fetch partner profile ────────────────
        async fetchProfile() {
            this.loading = true
            this.error = null

            try {
                const response = await api.get('/api/partners/profile/')
                this.partner = response.data

                // Update header initials
                // Fetch stock after profile
                await this.fetchStock()
                await this.fetchNotifications()
                await this.buildOverviewStats()
                await this.fetchActiveDonorRequests() 

            } catch (err) {
                if (err.response?.status === 401) {
                    // Token expired → redirect to login
                    localStorage.removeItem('access_token')
                    localStorage.removeItem('refresh_token')
                    this.$router.push('/partners/login')
                } else {
                    this.error = 'Could not load your profile. Please try again.'
                }
                console.error(err)
            } finally {
                this.loading = false
            }
        },
        

        // ── Fetch stock ──────────────────────────
        async fetchStock() {
            try {
                const response = await api.get(`/api/stock/partner/${this.partner.id}/`)
                const stockData = response.data

                
                Object.keys(this.stock).forEach(k => this.stock[k] = 0)

                // Map API response to stock object
                stockData.forEach(item => {
                    if (Object.prototype.hasOwnProperty.call(this.stock, item.blood_group)) {
                    this.stock[item.blood_group] = item.quantity
}
                })
            } catch (err) {
                console.error('Stock fetch failed:', err)
            }
        },

        // ── Fetch notifications ──────────────────
        async fetchNotifications() {
            try {
                const response = await api.get('/api/notifications/partner/')
                this.notifs = response.data
                this.unreadNotifs = response.data.filter(n => n.status === 'pending').length
            } catch (err) {
                console.error('Notifications fetch failed:', err)
            }
        },

        // ── Build overview stats ─────────────────
        async buildOverviewStats() {
            try {
                // Fetch active donor requests
                const donorReqs = await api.get('/api/requests/donor/list/')
                const activeDonorReqs = donorReqs.data.filter(r => r.status === 'open').length

                // Fetch attender requests
                const attenderReqs = await api.get('/api/requests/attender/list/')
                const pendingAttenders = attenderReqs.data.length

                // Fetch donation history
                const donations = await api.get('/api/donations/partner-history/')
                const totalDonations = donations.data.length

                this.overviewStats = [
                    { label: 'Active Donor Requests', val: `${activeDonorReqs} Active`, color: 'text-sky' },
                    { label: 'Pending Attenders', val: `${pendingAttenders} Requests`, color: 'text-warning' },
                    { label: 'Total Donations', val: `${totalDonations} Received`, color: 'text-success' },
                    { label: 'Convenience Fee', val: `₹${this.partner.convenience_fee || 0}`, color: 'text-dark' }
                ]
            } catch (err) {
                console.error('Stats fetch failed:', err)
                // Fallback stats
                this.overviewStats = [
                    { label: 'Active Donor Requests', val: '0 Active', color: 'text-sky' },
                    { label: 'Pending Attenders', val: '0 Requests', color: 'text-warning' },
                    { label: 'Total Donations', val: '0 Received', color: 'text-success' },
                    { label: 'Convenience Fee', val: `₹${this.partner.convenience_fee || 0}`, color: 'text-dark' }
                ]
            }
        },

        // ── Update stock ─────────────────────────
async updateStock(bloodGroup) {
    this.updatingStock = bloodGroup
    this.stockMessage = null

    try {
        await api.post('/api/stock/update/', {
            blood_group: bloodGroup,
            quantity: this.stock[bloodGroup]
        })

        // Add to local history log
        this.stockHistory.unshift({
            id: Date.now(),
            blood_group: bloodGroup,
            quantity: this.stock[bloodGroup],
            updated_at: new Date().toISOString()
        })

        this.stockMessage = {
            type: 'success',
            text: `${bloodGroup} stock updated to ${this.stock[bloodGroup]} units successfully!`
        }

        // Clear message after 3 seconds
        setTimeout(() => {
            this.stockMessage = null
        }, 3000)

    } catch (err) {
        this.stockMessage = {
            type: 'error',
            text: `Failed to update ${bloodGroup} stock. Please try again.`
        }
        console.error(err)
    } finally {
        this.updatingStock = null
    }
},

// ── Broadcast donor request ──────────────
async broadcastDonorRequest() {
    this.broadcastLoading = true
    this.donorRequestMessage = null

    try {
        await api.post('/api/requests/donor/create/', {
            blood_group: this.donorRequest.blood_group,
            quantity: this.donorRequest.quantity
        })

        this.donorRequestMessage = {
            type: 'success',
            text: `Request broadcasted! Nearby ${this.donorRequest.blood_group} donors notified via SMS + WhatsApp ✅`
        }

        // Reset form
        this.donorRequest.blood_group = ''
        this.donorRequest.quantity = 1

        // Refresh active requests
        await this.fetchActiveDonorRequests()

    } catch (err) {
        this.donorRequestMessage = {
            type: 'error',
            text: 'Failed to broadcast request. Please try again.'
        }
        console.error(err)
    } finally {
        this.broadcastLoading = false
    }
},

// ── Fetch active donor requests ──────────
async fetchActiveDonorRequests() {
    try {
        const response = await api.get('/api/requests/donor/list/')
        // Filter only this partner's requests
        this.activeDonorRequests = response.data.filter(
            r => r.partner === this.partner.id &&
            ['open', 'assigned'].includes(r.status)
        )

        // Auto select assigned request for chat
        const assigned = this.activeDonorRequests.find(r => r.status === 'assigned')
        if (assigned) {
            this.selectedDonorRequest = assigned
            await this.fetchChatMessages(assigned.id)
        }
    } catch (err) {
        console.error(err)
    }
},

// ── Fetch chat messages ──────────────────
async fetchChatMessages(requestId) {
    try {
        const response = await api.get(`/api/chat/${requestId}/history/`)
        this.chatMessages = response.data
    } catch (err) {
        console.error(err)
    }
},

// ── Send chat message ────────────────────
async sendChatMessage(message) {
    if (!this.selectedDonorRequest) return
    this.sendingMessage = true

    try {
        await api.post(`/api/chat/${this.selectedDonorRequest.id}/send/`, {
            message: message
        })
        // Refresh chat
        await this.fetchChatMessages(this.selectedDonorRequest.id)
    } catch (err) {
        console.error(err)
    } finally {
        this.sendingMessage = false
    }
},

// ── Verify donation ──────────────────────
async verifyDonation(requestId) {
    this.verifyingDonation = true

    try {
        await api.post(`/api/donations/verify/${requestId}/`)

        this.donorRequestMessage = {
            type: 'success',
            text: 'Donation verified successfully! Stock updated automatically ✅'
        }

        // Refresh everything
        await this.fetchStock()
        await this.fetchActiveDonorRequests()
        this.selectedDonorRequest = null
        this.chatMessages = []

    } catch (err) {
        this.donorRequestMessage = {
            type: 'error',
            text: 'Verification failed. Please try again.'
        }
        console.error(err)
    } finally {
        this.verifyingDonation = false
    }
},

// ── Time ago helper ──────────────────────
timeAgo(dateStr) {
    const diff = Math.floor((new Date() - new Date(dateStr)) / 60000)
    if (diff < 1) return 'Just now'
    if (diff < 60) return `${diff} mins ago`
    if (diff < 1440) return `${Math.floor(diff / 60)} hrs ago`
    return `${Math.floor(diff / 1440)} days ago`
},

// Save partner GPS location after login
async savePartnerGPS() {
    if (!navigator.geolocation) return

    navigator.geolocation.getCurrentPosition(
        async (pos) => {
            try {
                await api.put('/api/partners/profile/', {
                    latitude: pos.coords.latitude,
                    longitude: pos.coords.longitude
                })
                console.log('Partner GPS saved ✅')
            } catch (err) {
                console.error('Failed to save partner GPS:', err)
            }
        }
    )
},




        // ── Navigate ─────────────────────────────
        navigate(id) {
            if (id === 'logout') {
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                localStorage.removeItem('user_type')
                localStorage.removeItem('partner')
                this.$router.push('/')
                return
            }
            this.activeTab = id
            this.isMobileMenuOpen = false
        }
    }
}
</script>

<style scoped>
/* Sky Blue & White Professional Palette */
.chat-bubble {
    max-width: 250px;
    word-break: break-word;
}
.chat-area {
    scrollbar-width: thin;
}
.chat-area::-webkit-scrollbar {
    width: 4px;
}
.chat-area::-webkit-scrollbar-thumb {
    background: #B3E5FC;
    border-radius: 10px;
}
.text-sky { color: #00AEEF !important; }
.bg-sky { background-color: #00AEEF !important; }
.bg-sky-soft { background-color: #E1F5FE !important; }
.bg-light-blue { background-color: #F0F8FF !important; }
.btn-sky { background-color: #00AEEF; color: white; border: none; }
.btn-sky:hover { background-color: #008cc0; color: white; transform: translateY(-2px); }
.btn-sky-outline { border: 2px solid #00AEEF; color: #00AEEF; background: transparent; }
.btn-white { background: white; border: none; }
.sky-gradient { background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%); }
.border-light-blue { border-color: #B3E5FC; }

/* Responsive Layout */
.sidebar {
  width: 280px;
  height: 100vh;
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: 0.3s;
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: -280px;
    top: 0;
  }
  .sidebar.show { left: 0; }
  .mobile-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(4px);
    z-index: 999;
  }
}

/* Custom UI Elements */
.logo-box { width: 40px; height: 40px; background: #00AEEF; color: white; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 900; }
.menu-btn { padding: 14px 20px; border-radius: 12px; font-weight: 500; color: #666; transition: 0.2s; border: none; background: transparent; text-align: left; }
.menu-btn.active { background: #E1F5FE; color: #00AEEF; font-weight: 700; }
.stock-card { border-top: 4px solid #00AEEF !important; transition: transform 0.2s; }
.stock-card:hover { transform: translateY(-5px); }
.avatar-circle { width: 40px; height: 40px; background: #00AEEF; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; }
.date-box { background: #00AEEF; color: white; border-radius: 10px; width: 50px; text-align: center; font-weight: 900; line-height: 1; padding: 10px 0; }
.notif-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; }

.fw-800 { font-weight: 800; }
.smallest { font-size: 0.7rem; }
.animate-fade { animation: fadeIn 0.4s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.border-dashed { border: 2px dashed #B3E5FC; }
</style>