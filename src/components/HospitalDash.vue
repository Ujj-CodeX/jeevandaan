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
          
          :class="[
            'nav-link menu-btn w-100 text-start d-flex align-items-center', 
            activeTab === item.id ? 'active' : ''

          ]">
    
    <i :class="[item.icon, 'me-3']" style="width: 20px;"></i> 
    <span class="flex-grow-1">{{ item.label }}</span>
    <span v-if="item.id === 'notifications' && unreadNotifs > 0" 
          class="badge rounded-pill bg-danger ms-2">
      {{ unreadNotifs }}
    </span>
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

      <header v-if="!loading && !error" class="bg-white px-4 py-3 border-bottom d-none d-md-flex justify-content-between align-items-center sticky-top z-2">
        <h4 class="fw-bold mb-0">{{ currentLabel }}</h4>
        <div class="d-flex align-items-center gap-3">
          <div class="text-end">
            <p class="mb-0 fw-bold small">{{ partner.hospital_name }}</p>
            <p class="mb-0 smallest text-muted">{{ partner.city }}, {{ partner.state }}</p>
          </div>
          <div class="avatar-circle shadow-sm">{{ partnerInitials }}</div>
        </div>
      </header>

      <div v-if="!loading && !error" class="p-3 p-md-4">
        

        <!-- ══════════════════════════════════ -->
        <!-- OVERVIEW                           -->
        <!-- ══════════════════════════════════ -->
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
                  <tr v-for="donation in recentDonations.slice(0,5)" :key="donation.id">
                    <td class="text-sky fw-bold">#JD-{{ donation.id }}</td>
                    <td class="small">{{ donation.donor_name || 'Anonymous' }}</td>
                    <td><span class="badge bg-light text-dark">{{ donation.blood_group }}</span></td>
                    <td><span class="badge bg-success-subtle text-success">Verified</span></td>
                  </tr>
                  <tr v-if="recentDonations.length === 0">
                    <td colspan="4" class="text-center text-muted small py-3">No donations yet</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- ══════════════════════════════════ -->
        <!-- STOCK MANAGEMENT                   -->
        <!-- ══════════════════════════════════ -->
        <section v-if="activeTab === 'stock'" class="animate-fade">
          <div class="card border-0 shadow-sm rounded-4 p-4 mb-4">
            <h5 class="fw-bold mb-4">Update Inventory Level</h5>
            <div class="row g-3">
              <div class="col-md-4 col-sm-6" v-for="(qty, group) in stock" :key="group">
                <div class="input-group mb-2">
                  <span class="input-group-text bg-sky text-white fw-bold" style="width:50px">{{ group }}</span>
                  <input type="number" v-model.number="stock[group]" class="form-control border-light-blue" placeholder="Qty" min="0">
                  <button class="btn btn-sky-outline fw-bold" @click="updateStock(group)" :disabled="updatingStock === group">
                    <span v-if="updatingStock === group"><span class="spinner-border spinner-border-sm"></span></span>
                    <span v-else>Update</span>
                  </button>
                </div>
              </div>
            </div>
            <div v-if="stockMessage" :class="['alert mt-3 rounded-4 border-0', stockMessage.type === 'success' ? 'alert-success' : 'alert-danger']">
              <i :class="['me-2', stockMessage.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle']"></i>
              {{ stockMessage.text }}
            </div>
          </div>

          <div class="card border-0 shadow-sm rounded-4 p-4">
            <h6 class="fw-bold text-muted mb-3"><i class="fas fa-history me-2"></i>Stock History Log</h6>
            <div v-if="stockHistory.length === 0" class="timeline-placeholder p-4 border-dashed rounded-4 text-center text-muted small">
              No recent changes logged in the last 24 hours.
            </div>
            <div v-else class="list-group list-group-flush">
              <div v-for="log in stockHistory" :key="log.id" class="list-group-item px-0 py-2 bg-transparent d-flex justify-content-between">
                <div>
                  <span class="badge bg-sky-soft text-sky me-2">{{ log.blood_group }}</span>
                  <small class="fw-bold">{{ log.quantity }} units</small>
                </div>
                <small class="text-muted">{{ timeAgo(log.updated_at) }}</small>
              </div>
            </div>
          </div>
        </section>

        <!-- ══════════════════════════════════ -->
        <!-- RAISE DONOR                        -->
        <!-- ══════════════════════════════════ -->
        <section v-if="activeTab === 'raise-donor'" class="animate-fade">
          <div class="row g-4">

            <!-- LEFT: Broadcast form -->
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
                  <input type="number" class="form-control border-0 bg-light py-3" placeholder="0" v-model.number="donorRequest.quantity" min="1">
                </div>
                <div v-if="donorRequestMessage" :class="['alert border-0 rounded-4 mb-3', donorRequestMessage.type === 'success' ? 'alert-success' : 'alert-danger']">
                  <i :class="['me-2', donorRequestMessage.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle']"></i>
                  {{ donorRequestMessage.text }}
                </div>
                <button class="btn btn-sky w-100 py-3 fw-bold rounded-3" @click="broadcastDonorRequest" :disabled="broadcastLoading || !donorRequest.blood_group || !donorRequest.quantity">
                  <span v-if="broadcastLoading"><span class="spinner-border spinner-border-sm me-2"></span>Broadcasting...</span>
                  <span v-else><i class="fas fa-bullhorn me-2"></i>BROADCAST NOTIFICATION</span>
                </button>
              </div>

              <!-- Active requests list with Open Chat button -->
              <div class="card border-0 shadow-sm rounded-4 p-4 mt-4" v-if="activeDonorRequests.length > 0">
                <h6 class="fw-bold mb-3">Your Active Requests</h6>
                <div v-for="req in activeDonorRequests" :key="req.id" class="p-3 bg-light rounded-4 mb-2">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <span class="badge bg-sky-soft text-sky fw-bold me-2">{{ req.blood_group }}</span>
                      <small class="fw-bold">{{ req.quantity }} units</small>
                      <small class="text-muted ms-2">{{ timeAgo(req.created_at) }}</small>
                    </div>
                    <span :class="['badge rounded-pill', req.status === 'open' ? 'bg-warning text-dark' : req.status === 'assigned' ? 'bg-success' : 'bg-danger']">
                      {{ req.status }}
                    </span>
                  </div>
                  <!-- Open Chat button — appears when donor accepts -->
                  <div v-if="req.status === 'assigned'" class="mt-2">
                    <button class="btn btn-sky btn-sm fw-bold rounded-3 w-100 py-2" @click="openChat(req.id)">
                      <i class="fas fa-comments me-2"></i>Open Chat with Donor
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- RIGHT: Status panel -->
            <div class="col-lg-7">
              <div class="card border-0 shadow-sm rounded-4 p-4 h-100">
                <h6 class="fw-bold mb-3">Accepted Donors / Live Chat</h6>

                <!-- No requests at all -->
                <div v-if="activeDonorRequests.length === 0" class="alert bg-sky-soft text-sky border-0 small rounded-4">
                  <i class="fas fa-info-circle me-2"></i>
                  No active donor responses yet. Broadcast a request first.
                </div>

                <!-- Has requests but waiting -->
                <div v-else-if="activeDonorRequests.length > 0 && !activeDonorRequests.some(r => r.status === 'assigned')">
                  <div class="alert bg-warning-subtle border-0 rounded-4 small">
                    <i class="fas fa-hourglass-half me-2 text-warning"></i>
                    <strong>Waiting for a donor to accept...</strong>
                    <div class="text-muted mt-1">You'll see a chat button here as soon as a donor accepts your request.</div>
                  </div>
                  <!-- Show open requests summary -->
                  <div v-for="req in activeDonorRequests.filter(r => r.status === 'open')" :key="req.id" class="p-3 bg-light rounded-4 mb-2 d-flex justify-content-between align-items-center">
                    <div>
                      <span class="badge bg-sky-soft text-sky fw-bold me-2">{{ req.blood_group }}</span>
                      <small class="fw-bold">{{ req.quantity }} units</small>
                    </div>
                    <span class="badge rounded-pill bg-warning text-dark">Waiting</span>
                  </div>
                </div>

                <!-- Donor accepted — show assigned requests with chat prompt -->
                <div v-else>
                  <div v-for="req in activeDonorRequests.filter(r => r.status === 'assigned')" :key="req.id" class="mb-3">
                    <div class="p-3 rounded-4" style="background: linear-gradient(135deg, #e8f5e9, #c8e6c9);">
                      <div class="d-flex justify-content-between align-items-center mb-2">
                        <div>
                          <span class="badge bg-success me-2">Donor Accepted  </span>
                          <small class="fw-bold">{{ req.blood_group }} — {{ req.quantity }} units</small>
                        </div>
                        <small class="text-muted">{{ timeAgo(req.created_at) }}</small>
                      </div>
                      <p class="small text-muted mb-3">A donor has accepted your request. Open the chat to communicate and verify their OTP when they arrive.</p>
                      <button class="btn btn-success fw-bold w-100 py-2 rounded-3" @click="openChat(req.id)">
                        <i class="fas fa-comments me-2"></i>Open Live Chat with Donor
                      </button>
                    </div>
                  </div>
                </div>

              </div>
            </div>

          </div>
        </section>

        <!-- ══════════════════════════════════ -->
        <!-- VIEW ATTENDER                      -->
        <!-- ══════════════════════════════════ -->
        <section v-if="activeTab === 'view-attender'" class="animate-fade">
  <div class="card border-0 shadow-sm rounded-4 p-4 p-md-5 mb-4 sky-gradient text-white">
            <h4 class="fw-800">Attender Request Lookup</h4>
            <p class="opacity-75">Search by Reference ID or browse all pending requests.</p>
            <div class="input-group mt-4 mx-auto shadow-lg rounded-pill overflow-hidden" style="max-width:500px">
              <input type="text" class="form-control border-0 px-4 py-3" placeholder="Reference ID (e.g. 550e8400-e29b...)" v-model="searchRefId">
              <button class="btn btn-white px-4 fw-bold text-sky" @click="searchByRefId" :disabled="searchLoading">
                <span v-if="searchLoading"><span class="spinner-border spinner-border-sm"></span></span>
                <span v-else>SEARCH</span>
              </button>
            </div>


            <div v-if="searchResult" class="mt-4 bg-white text-dark rounded-4 p-4">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="fw-bold mb-0"><i class="fas fa-file-medical text-sky me-2"></i>{{ searchResult.patient_name }}</h6>
                <span :class="['badge rounded-pill', searchResult.urgency === 'critical' ? 'bg-danger' : searchResult.urgency === 'urgent' ? 'bg-warning text-dark' : 'bg-success']">
                  {{ searchResult.urgency?.toUpperCase() }}
                </span>
              </div>
              <div class="row g-2 small text-muted">
                <div class="col-6"><i class="fas fa-tint text-danger me-1"></i><strong>{{ searchResult.blood_group }}</strong> — {{ searchResult.quantity }} units</div>
                <div class="col-6"><i class="fas fa-hospital me-1"></i>{{ searchResult.hospital_name }}</div>
                <div class="col-6"><i class="fas fa-user me-1"></i>{{ searchResult.attender_name }}</div>
                <div class="col-6"><i class="fas fa-phone me-1"></i>{{ searchResult.attender_phone }}</div>
              </div>
              <div class="mt-3 d-flex gap-2">
    <!-- NEW: opens the existing document-verification modal -->
    <button class="btn btn-light border fw-bold rounded-3" @click="selectedRequest = searchResult">
      <i class="fas fa-id-card-alt me-2"></i>Verify Documents
    </button>
    <button class="btn btn-sky fw-bold flex-grow-1 rounded-3" @click="fulfillAttenderRequest(searchResult.reference_id)" :disabled="fulfillingRequest">
      <span v-if="fulfillingRequest"><span class="spinner-border spinner-border-sm me-2"></span>Processing...</span>
      <span v-else><i class="fas fa-check me-2"></i>Mark as Fulfilled</span>
    </button>
    <button class="btn btn-light border rounded-3" @click="searchResult = null">Cancel</button>
  </div>
            </div>
            <div v-if="searchError" class="mt-3 alert alert-danger border-0 rounded-4">{{ searchError }}</div>
          </div>

 

  <div v-if="selectedRequest" class="modal-backdrop d-flex align-items-center justify-content-center p-3 z-3">
    <div class="card border-0 shadow-lg rounded-4 overflow-hidden w-100 animate-slide-up" style="max-width: 750px; max-height: 92vh;">
      
      <div class="bg-dark p-3 d-flex justify-content-between align-items-center text-white">
        <div>
          <small class="text-uppercase opacity-75 d-block" style="font-size: 0.65rem; letter-spacing: 1px;">Reference Key for Verification</small>
          <span class="fw-mono fw-bold text-sky-light">{{ selectedRequest.reference_id }}</span>
          <button @click="copyRef(selectedRequest.reference_id)" class="btn btn-sm btn-link text-sky p-0 ms-2">
            <i class="fas fa-copy"></i>
          </button>
        </div>
        <button class="btn btn-link text-white p-0" @click="selectedRequest = null"><i class="fas fa-times fs-4"></i></button>
      </div>
      
      <div class="card-body overflow-auto p-4">
        <div class="row g-4">
          <div class="col-md-6">
            <h6 class="fw-bold text-sky border-bottom pb-2 mb-3 small text-uppercase">Patient & Attender</h6>
            
            <div class="d-flex align-items-center mb-3 bg-light p-2 rounded-3 border">
              <img :src="selectedRequest.patient_photo" class="rounded-circle me-3 border" style="width:55px; height:55px; object-fit:cover;">
              <div>
                <h6 class="mb-0 fw-bold">{{ selectedRequest.patient_name }} ({{ selectedRequest.patient_age }}y)</h6>
                <p class="smallest text-muted mb-0">Needs {{ selectedRequest.blood_group }} at {{ selectedRequest.hospital_name }}</p>
              </div>
            </div>

            <div class="small p-2">
              <p class="mb-2"><strong>Attender:</strong> {{ selectedRequest.attender_name }}</p>
              <p class="mb-2"><strong>Contact:</strong> {{ selectedRequest.attender_phone }}</p>
              <p class="mb-2"><strong>{{ selectedRequest.id_type }}:</strong> {{ selectedRequest.id_no }}</p>
              <p class="mb-0"><strong>Doctor:</strong> Dr. {{ selectedRequest.doctor_name }} ({{ selectedRequest.doctor_phone }})</p>
            </div>
          </div>

          <div class="col-md-6">
            <h6 class="fw-bold text-muted border-bottom pb-2 mb-3 small text-uppercase">Document Verification</h6>
            <div class="row g-2">
              <div class="col-6">
                <label class="smallest text-muted d-block mb-1">Letterhead</label>
                <a :href="selectedRequest.doctor_letterhead" target="_blank">
                  <img :src="selectedRequest.doctor_letterhead" class="img-fluid rounded border hover-zoom shadow-sm">
                </a>
              </div>
              <div class="col-6">
                <label class="smallest text-muted d-block mb-1">ID Proof</label>
                <a :href="selectedRequest.attender_id_proof" target="_blank">
                  <img :src="selectedRequest.attender_id_proof" class="img-fluid rounded border hover-zoom shadow-sm">
                </a>
              </div>
            </div>
            <div class="alert alert-info py-2 px-3 mt-3 mb-0" style="font-size: 0.75rem;">
              <i class="fas fa-info-circle me-2"></i>Verify the physical documents against these uploads.
            </div>
          </div>
        </div>
      </div>

      <div class="card-footer bg-white p-3 border-top">
        <button class="btn btn-sky w-100 py-2 fw-bold rounded-3 shadow-sm" @click="selectedRequest = null">
          OK, I'VE VERIFIED THIS
        </button>
      </div>
    </div>
  </div>
</section>

<!-- History---Section -->


<section v-if="activeTab === 'history'" class="animate-fade">
    <div class="d-flex gap-2 mb-3">
        <button class="btn btn-sm rounded-pill px-3"
            :class="historyTab === 'donor' ? 'btn-sky' : 'btn-sky-outline'"
            @click="historyTab = 'donor'">Donor Requests</button>
        <button class="btn btn-sm rounded-pill px-3"
            :class="historyTab === 'attender' ? 'btn-sky' : 'btn-sky-outline'"
            @click="historyTab = 'attender'">Attender Fulfilled</button>
        <button class="btn btn-sm rounded-pill px-3"
            :class="historyTab === 'inter' ? 'btn-sky' : 'btn-sky-outline'"
            @click="historyTab = 'inter'">Inter-Partner</button>
    </div>

    <div v-if="historyLoading" class="text-center py-4">
        <div class="spinner-border text-sky"></div>
    </div>

    <div v-else class="card border-0 shadow-sm rounded-4 p-3">
        <table class="table table-hover align-middle" v-if="historyTab === 'donor'">
            <thead><tr><th>Group</th><th>Qty</th><th>Donor</th><th>Status</th><th>Date</th></tr></thead>
            <tbody>
                <tr v-for="r in history.donor_requests" :key="r.id">
                    <td>{{ r.blood_group }}</td>
                    <td>{{ r.quantity }}</td>
                    <td>{{ r.assigned_donor || '-' }}</td>
                    <td><span class="badge bg-secondary">{{ r.status }}</span></td>
                    <td class="small text-muted">{{ timeAgo(r.updated_at) }}</td>
                </tr>
            </tbody>
        </table>

        <table class="table table-hover align-middle" v-if="historyTab === 'attender'">
            <thead><tr><th>Patient</th><th>Group</th><th>Qty</th><th>Status</th><th>Date</th></tr></thead>
            <tbody>
                <tr v-for="a in history.attender_fulfilled" :key="a.reference_id">
                    <td>{{ a.patient_name }}</td>
                    <td>{{ a.blood_group }}</td>
                    <td>{{ a.quantity }}</td>
                    <td><span class="badge bg-success">{{ a.status }}</span></td>
                    <td class="small text-muted">{{ timeAgo(a.updated_at) }}</td>
                </tr>
            </tbody>
        </table>

        <table class="table table-hover align-middle" v-if="historyTab === 'inter'">
            <thead><tr><th>Direction</th><th>Partner</th><th>Group</th><th>Qty</th><th>Status</th><th>Date</th></tr></thead>
            <tbody>
                <tr v-for="i in history.inter_partner_requests" :key="i.id">
                    <td><span class="badge" :class="i.direction === 'sent' ? 'bg-warning text-dark' : 'bg-info text-dark'">{{ i.direction }}</span></td>
                    <td>{{ i.direction === 'sent' ? i.fulfilling_partner : i.requesting_partner }}</td>
                    <td>{{ i.blood_group }}</td>
                    <td>{{ i.quantity }}</td>
                    <td><span class="badge bg-secondary">{{ i.status }}</span></td>
                    <td class="small text-muted">{{ timeAgo(i.updated_at) }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</section>

        <!-- ══════════════════════════════════ -->
        <!-- VERIFY DONATION                    -->
        <!-- ══════════════════════════════════ -->
        <section v-if="activeTab === 'verify'" class="animate-fade">
          <div class="card border-0 shadow-sm rounded-4 p-4 mb-4">
            <h5 class="fw-bold mb-4">Donation Verification Terminal</h5>
            <div class="row align-items-center bg-light p-4 rounded-4 mb-4">
              <div class="col-md-8">
                <h6 class="fw-bold">Enter Donor OTP Code</h6>
                <p class="text-muted small mb-3">Ask donor for their one-time code received after accepting request.</p>
                <input type="text" class="form-control form-control-lg border-0 shadow-sm" placeholder="Enter 6-digit OTP" v-model="otpCode" maxlength="6">
              </div>
              <div class="col-md-4 mt-3 mt-md-0">
                <button class="btn btn-sky w-100 py-3 fw-bold rounded-3" @click="verifyOTP" :disabled="otpLoading || !otpCode">
                  <span v-if="otpLoading"><span class="spinner-border spinner-border-sm me-2"></span>Verifying...</span>
                  <span v-else><i class="fas fa-check-double me-2"></i>VERIFY OTP</span>
                </button>
              </div>
            </div>
            <div v-if="otpResult" class="alert bg-success-subtle border-0 rounded-4 p-4">
              <div class="d-flex align-items-center gap-3 mb-3">
                <i class="fas fa-check-circle text-success fa-2x"></i>
                <div>
                  <h6 class="fw-bold mb-0 text-success">OTP Verified Successfully!  </h6>
                  <small class="text-muted">Donor identity confirmed</small>
                </div>
              </div>
              <div class="row g-2 small">
                <div class="col-6"><span class="text-muted">Blood Group:</span><strong class="text-danger ms-1">{{ otpResult.blood_group }}</strong></div>
                <div class="col-6"><span class="text-muted">Units:</span><strong class="ms-1">{{ otpResult.quantity }}</strong></div>
              </div>
              <button class="btn btn-success w-100 py-3 fw-bold rounded-3 mt-3" @click="confirmDonation(otpResult.request_id)" :disabled="confirmingDonation">
                <span v-if="confirmingDonation"><span class="spinner-border spinner-border-sm me-2"></span>Confirming...</span>
                <span v-else><i class="fas fa-heart me-2"></i>Confirm Donation Received</span>
              </button>
            </div>
            <div v-if="otpError" class="alert alert-danger border-0 rounded-4"><i class="fas fa-exclamation-circle me-2"></i>{{ otpError }}</div>
            <div v-if="verifySuccess" class="alert bg-success-subtle border-0 rounded-4 text-success"><i class="fas fa-check-circle me-2"></i>{{ verifySuccess }}</div>
          </div>

          <div class="card border-0 shadow-sm rounded-4 p-4">
            <h6 class="fw-bold mb-3"><i class="fas fa-history me-2 text-sky"></i>Recent Donations Verified</h6>
            <div v-if="recentDonations.length === 0" class="text-center py-3 text-muted small">No donations verified yet.</div>
            <div v-else class="table-responsive">
              <table class="table table-hover align-middle">
                <thead class="bg-light">
                  <tr><th>Donor</th><th>Group</th><th>Units</th><th>When</th><th>Status</th></tr>
                </thead>
                <tbody>
                  <tr v-for="donation in recentDonations" :key="donation.id">
                    <td class="small fw-bold">{{ donation.donor_name || 'Anonymous' }}</td>
                    <td><span class="badge bg-light text-dark border">{{ donation.blood_group }}</span></td>
                    <td class="small">{{ donation.units_donated }} units</td>
                    <td class="small text-muted">{{ timeAgo(donation.donated_at) }}</td>
                    <td>
                      <span :class="['badge rounded-pill', donation.is_verified_by_bank ? 'bg-success' : 'bg-warning text-dark']">
                        {{ donation.is_verified_by_bank ? 'Verified  ' : 'Pending' }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        

        <!-- ══════════════════════════════════ -->
        <!-- NOTIFICATIONS                      -->
        <!-- ══════════════════════════════════ -->
        <section v-if="activeTab === 'notifications'" class="animate-fade">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="fw-bold mb-0">Alerts & Notifications <span v-if="unreadNotifs > 0" class="badge bg-danger ms-2">{{ unreadNotifs }} New</span></h5>
            <button class="btn btn-sky-outline btn-sm rounded-pill px-3" @click="fetchNotifications"><i class="fas fa-sync me-1"></i> Refresh</button>
          </div>
          <div v-if="notifsLoading" class="text-center py-4"><div class="spinner-border text-sky"></div></div>
          <div v-else-if="notifs.length === 0" class="card border-0 shadow-sm rounded-4 p-5 text-center">
            <i class="fas fa-bell-slash text-muted fa-3x mb-3"></i>
            <h6 class="fw-bold">No Notifications Yet</h6>
            <p class="text-muted small">You'll be notified when donors respond or new requests arrive.</p>
          </div>
          <div v-else class="card border-0 shadow-sm rounded-4 overflow-hidden">
            <div v-for="n in notifs" :key="n.id" :class="['p-3 border-bottom d-flex align-items-start gap-3', n.status === 'pending' ? 'bg-sky-soft' : '']">
              <div :class="['notif-icon', getNotifBg(n.trigger)]"><i :class="getNotifIcon(n.trigger)"></i></div>
              <div class="flex-grow-1">
                <p class="mb-0 fw-bold small text-dark">{{ getNotifTitle(n.trigger) }}</p>
                <p class="mb-0 smallest text-muted"> {{ removeOTP(n.message) }}</p>
                <small class="smallest opacity-50">{{ timeAgo(n.created_at) }}</small>
              </div>
              <div v-if="n.status === 'pending'" class="mt-1"><span class="badge bg-danger rounded-pill smallest">New</span></div>
              <button v-if="n.status === 'pending'" class="btn btn-sm btn-light rounded-pill smallest" @click="markNotifRead(n.id)">✓</button>
            </div>
          </div>
        </section>


        <!-- ══════════════════════════════════ -->
        <!-- DONATION CAMPS                     --> 

<section v-if="activeTab === 'camps'" class="animate-fade">

    <!-- Freeze banner -->

  
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h5 class="fw-bold mb-0">Donation Camps</h5>
            <button
                class="btn btn-sky fw-bold btn-sm rounded-pill px-4"
                @click="showCreateCamp = true"
            >
                <i class="fas fa-plus me-2"></i> Schedule Camp
            </button>
        </div>

        <!-- Loading -->
        <div v-if="campsLoading" class="text-center py-4">
            <div class="spinner-border text-sky"></div>
        </div>

        <!-- Empty -->
        <div v-else-if="camps.length === 0" class="card border-0 shadow-sm rounded-4 p-5 text-center">
            <i class="fas fa-campground text-muted fa-3x mb-3"></i>
            <h6 class="fw-bold">No Camps Scheduled</h6>
            <p class="text-muted small">Schedule your first donation camp!</p>
        </div>

        <!-- Camp cards -->
        <div v-else class="row g-3">
            <div class="col-md-6 col-lg-4" v-for="camp in camps" :key="camp.id">
                <div class="card border-0 shadow-sm rounded-4 p-3 h-100">

                    <!-- Status badge -->
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <span :class="['badge rounded-pill', camp.status === 'scheduled' ? 'bg-success' : camp.status === 'completed' ? 'bg-secondary' : 'bg-warning text-dark']">
                            {{ camp.status }}
                        </span>
                        <small class="text-muted smallest">{{ camp.enrolled_count }} enrolled</small>
                    </div>

                    <!-- Camp info -->
                    <h6 class="fw-bold mb-1">{{ camp.title }}</h6>
                    <p class="text-muted small mb-2">
                        <i class="fas fa-calendar me-1 text-sky"></i>{{ camp.camp_date }}
                        <i class="fas fa-clock me-1 text-sky ms-2"></i>{{ camp.start_time }}
                    </p>
                    <p class="text-muted small mb-2">
                        <i class="fas fa-location-dot me-1 text-sky"></i>{{ camp.location }}
                    </p>

                    <!-- Blood groups -->
                    <div class="d-flex flex-wrap gap-1 mb-3">
                        <span
                            v-for="bg in camp.blood_groups_needed"
                            :key="bg"
                            class="badge bg-sky-soft text-sky rounded-pill small"
                        >
                            {{ bg }}
                        </span>
                    </div>

              


                    
                    
                    <!-- Buttons -->
                    <div class="d-flex gap-2 mt-auto">
    <!-- Notify — sirf scheduled camps ke liye -->
    <button
        v-if="camp.status === 'scheduled'"
        class="btn btn-sky btn-sm flex-grow-1 rounded-3 fw-bold"
        @click="scheduleAndNotify(camp.id)"
        :disabled="notifyingCamp === camp.id"
    >
        <span v-if="notifyingCamp === camp.id">
            <span class="spinner-border spinner-border-sm me-1"></span>
        </span>
        <span v-else>
            <i class="fas fa-bullhorn me-1"></i> Notify
        </span>
    </button>

    <!-- CSV download — camp aaj ya beet chuka ho toh milega -->
    <button
        v-if="isCampToday(camp) || isCampPast(camp)"
        class="btn btn-success btn-sm rounded-3 fw-bold"
        @click="downloadEnrollments(camp)"
        :disabled="downloadingCamp === camp.id"
        title="Download enrolled donors list"
    >
        <span v-if="downloadingCamp === camp.id">
            <span class="spinner-border spinner-border-sm"></span>
        </span>
        <span v-else>
            <i class="fas fa-download me-1"></i> CSV
        </span>
    </button>

    <!-- Completed badge — status ab Celery Beat se aata hai -->
    <span v-if="camp.status === 'completed'"
        class="badge bg-success rounded-3 p-2 flex-grow-1 text-center">
          Completed
    </span>
</div>
                </div>
            </div>
        </div>
    
</section>
<section v-if="activeTab === 'inter-partner'" class="animate-fade">
    <div class="row g-4">

        <!-- LEFT — Raise Request -->
        <div class="col-lg-5">
            <div class="card border-0 shadow-sm rounded-4 p-4">
                <h5 class="fw-bold mb-1">Raise Partner Request</h5>
                <p class="text-muted small mb-4">
                    Request blood stock from nearest verified partner bank.
                </p>

                <div class="mb-3">
                    <label class="small fw-bold text-muted">Blood Group *</label>
                    <select class="form-select border-0 bg-light py-3"
                        v-model="interForm.blood_group">
                        <option disabled value="">Select Blood Group</option>
                        <option v-for="(_, g) in stock" :key="g">{{ g }}</option>
                    </select>
                </div>

                <div class="mb-3">
                    <label class="small fw-bold text-muted">Units Needed *</label>
                    <input type="number"
                        class="form-control border-0 bg-light py-3"
                        v-model.number="interForm.quantity"
                        placeholder="0" min="1">
                </div>

                <div class="mb-4">
                    <label class="small fw-bold text-muted">Attender Reference ID *</label>
                    <input type="text"
                        class="form-control border-0 bg-light py-3"
                        v-model="interForm.attender_request_id"
                        placeholder="Enter reference ID">
                    <small class="text-muted">
                        Link this to an existing attender request
                    </small>
                </div>

                <!-- Result -->
                <div v-if="interResult" class="p-3 bg-success-subtle rounded-4 mb-3">
                    <p class="fw-bold text-success mb-1">
                          Request sent to {{ interResult.fulfilling_partner?.hospital_name }}
                    </p>
                    <small class="text-muted d-block">
                        Distance: {{ interResult.distance_km }} km away
                    </small>
                    <small class="text-muted d-block">
                        Convenience Fee: ₹{{ interResult.convenience_fee }}
                    </small>
                </div>

                <!-- Error -->
                <div v-if="interError" class="alert alert-danger border-0 rounded-4 mb-3 small">
                    {{ interError }}
                </div>

                <button
                    class="btn btn-sky w-100 py-3 fw-bold rounded-3"
                    @click="raiseInterPartnerRequest"
                    :disabled="interLoading || !interForm.blood_group || !interForm.quantity"
                >
                    <span v-if="interLoading">
                        <span class="spinner-border spinner-border-sm me-2"></span>
                        Finding nearest partner...
                    </span>
                    <span v-else>
                        <i class="fas fa-paper-plane me-2"></i>
                        Send Request to Nearest Partner
                    </span>
                </button>
            </div>
        </div>

        <!-- RIGHT — Incoming Requests -->
        <div class="col-lg-7">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="fw-bold mb-0">
                    Incoming Partner Requests
                    <span v-if="incomingInterRequests.length > 0"
                        class="badge bg-danger ms-2">
                        {{ incomingInterRequests.length }}
                    </span>
                </h5>
                <button class="btn btn-sky-outline btn-sm rounded-pill px-3"
                    @click="fetchIncomingInterRequests">
                    <i class="fas fa-sync me-1"></i> Refresh
                </button>
            </div>

            <!-- Loading -->
            <div v-if="interRequestsLoading" class="text-center py-4">
                <div class="spinner-border text-sky"></div>
            </div>

            <!-- Empty -->
            <div v-else-if="incomingInterRequests.length === 0"
                class="card border-0 shadow-sm rounded-4 p-5 text-center">
                <i class="fas fa-inbox text-muted fa-3x mb-3"></i>
                <h6 class="fw-bold">No Incoming Requests</h6>
                <p class="text-muted small">
                    When nearby partners need blood stock, requests will appear here.
                </p>
            </div>

            <!-- Request cards -->
            <div v-else class="d-flex flex-column gap-3">
                <div v-for="req in incomingInterRequests" :key="req.id"
                    class="card border-0 shadow-sm rounded-4 p-4">

                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div>
                            <h6 class="fw-bold mb-1">
                                <i class="fas fa-hospital text-sky me-2"></i>
                                {{ req.requesting_partner }}
                            </h6>
                            <small class="text-muted">
                                Needs
                                <strong class="text-danger">{{ req.blood_group }}</strong>
                                — {{ req.quantity }} units
                            </small>
                            <small class="d-block text-muted smallest mt-1">
                            <i class="fas fa-key me-1"></i> Ref: {{ req.reference_id?.substring(0, 8) }}...
                              <button class="btn btn-sm btn-link p-0 ms-1" @click="copyRef(req.reference_id)">
                            <i class="fas fa-copy"></i>
                            </button>
                            </small>
                        </div>
                        <span class="badge bg-warning text-dark rounded-pill">
                            Pending
                        </span>
                    </div>

                    <div class="p-3 bg-light rounded-4 mb-3">
                        <div class="d-flex justify-content-between small">
                            <span class="text-muted">Convenience Fee</span>
                            <strong class="text-success">₹{{ req.convenience_fee }}</strong>
                        </div>
                        <div class="d-flex justify-content-between small mt-1">
                            <span class="text-muted">Requested</span>
                            <strong>{{ timeAgo(req.created_at) }}</strong>
                        </div>
                    </div>

                    <div class="d-flex gap-2">
                        <button
                            class="btn btn-sky fw-bold flex-grow-1 rounded-3"
                            @click="acceptInterRequest(req.id)"
                            :disabled="acceptingInterReq === req.id"
                        >
                            <span v-if="acceptingInterReq === req.id">
                                <span class="spinner-border spinner-border-sm me-2"></span>
                            </span>
                            <span v-else>
                                <i class="fas fa-check me-2"></i> Accept & Fulfill
                            </span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>


<!-- Create Camp Modal -->
<div v-if="showCreateCamp" class="modal-overlay" @click.self="showCreateCamp = false">
    <div class="bg-white rounded-4 shadow-lg p-4" style="max-width:550px;width:100%;max-height:90vh;overflow-y:auto">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h5 class="fw-bold mb-0">Schedule Donation Camp</h5>
            <button class="btn btn-light rounded-circle" @click="showCreateCamp = false">
                <i class="fas fa-times"></i>
            </button>
        </div>

        <div class="row g-3">
            <div class="col-12">
                <label class="small fw-bold text-muted">Camp Title *</label>
                <input type="text" class="form-control border-light-blue"
                    v-model="campForm.title"
                    placeholder="e.g. Mega Blood Drive 2026">
            </div>

            <div class="col-12">
                <label class="small fw-bold text-muted">Description</label>
                <textarea class="form-control border-light-blue" rows="2"
                    v-model="campForm.description"
                    placeholder="Brief description of the camp"></textarea>
            </div>

            <div class="col-12">
                <label class="small fw-bold text-muted">Location / Venue *</label>
                <input type="text" class="form-control border-light-blue"
                    v-model="campForm.location"
                    placeholder="Full address of camp venue">
            </div>

            <div class="col-md-4">
                <label class="small fw-bold text-muted">Date *</label>
                <input type="date" class="form-control border-light-blue"
                    v-model="campForm.camp_date"
                    :min="today">
            </div>

            <div class="col-md-4">
                <label class="small fw-bold text-muted">Start Time *</label>
                <input type="time" class="form-control border-light-blue"
                    v-model="campForm.start_time">
            </div>

            <div class="col-md-4">
                <label class="small fw-bold text-muted">End Time *</label>
                <input type="time" class="form-control border-light-blue"
                    v-model="campForm.end_time">
            </div>

            <div class="col-md-6">
                <label class="small fw-bold text-muted">Expected Donors</label>
                <input type="number" class="form-control border-light-blue"
                    v-model.number="campForm.expected_donors"
                    placeholder="0" min="0">
            </div>

            <div class="col-12">
                <label class="small fw-bold text-muted">Blood Groups Needed</label>
                <div class="d-flex flex-wrap gap-2 mt-1">
                    <button
                        v-for="bg in allBloodGroups"
                        :key="bg"
                        type="button"
                        :class="['btn btn-sm rounded-pill fw-bold',
                            campForm.blood_groups_needed.includes(bg)
                            ? 'btn-sky' : 'btn-sky-outline']"
                        @click="toggleBloodGroup(bg)"
                    >
                        {{ bg }}
                    </button>
                </div>
            </div>
        </div>

        <!-- Error -->
        <div v-if="campError" class="alert alert-danger border-0 rounded-4 mt-3">
            {{ campError }}
        </div>

        <!-- Success -->
        <div v-if="campSuccess" class="alert alert-success border-0 rounded-4 mt-3">
            {{ campSuccess }}
        </div>

        <div class="d-flex gap-2 mt-4">
            <button
                class="btn btn-sky fw-bold flex-grow-1 py-3 rounded-3"
                @click="createCamp"
                :disabled="creatingCamp"
            >
                <span v-if="creatingCamp">
                    <span class="spinner-border spinner-border-sm me-2"></span>
                    Creating...
                </span>
                <span v-else>
                    <i class="fas fa-calendar-plus me-2"></i>
                    Create Camp
                </span>
            </button>
            <button class="btn btn-light flex-grow-1 py-3 rounded-3"
                @click="showCreateCamp = false">
                Cancel
            </button>
        </div>
    </div>
</div>



        <!-- ══════════════════════════════════ -->
        <!-- PROFILE                            -->
        <!-- ══════════════════════════════════ -->
        <section v-if="activeTab === 'profile'" class="animate-fade">
          <div class="row g-4">
            <div class="col-md-7">
              <div class="card border-0 shadow-sm rounded-4 p-4">
                <h5 class="fw-bold mb-4">Facility Information</h5>
                <div class="row g-3">
                  <div class="col-12">
                    <label class="smallest fw-bold text-muted">Facility Name</label>
                    <input type="text" class="form-control border-light-blue" v-model="profileForm.hospital_name">
                  </div>
                  <div class="col-md-6">
                    <label class="smallest fw-bold text-muted">Convenience Fee (₹)</label>
                    <input type="number" class="form-control border-light-blue" v-model="profileForm.convenience_fee">
                  </div>
                  <div class="col-md-6">
                    <label class="smallest fw-bold text-muted">Contact No.</label>
                    <input type="text" class="form-control border-light-blue" v-model="profileForm.contact">
                  </div>
                  <div class="col-12">
                    <label class="smallest fw-bold text-muted">Address</label>
                    <input type="text" class="form-control border-light-blue" v-model="profileForm.address">
                  </div>
                  <div class="col-md-6">
                    <label class="smallest fw-bold text-muted">City</label>
                    <input type="text" class="form-control border-light-blue" v-model="profileForm.city">
                  </div>
                  <div class="col-md-6">
                    <label class="smallest fw-bold text-muted">State</label>
                    <input type="text" class="form-control border-light-blue" v-model="profileForm.state">
                  </div>
                  <div class="col-12">
                    <label class="smallest fw-bold text-muted">Facility Description</label>
                    <textarea class="form-control border-light-blue" rows="3" v-model="profileForm.facility"></textarea>
                  </div>
                  <div class="col-12">
                    <label class="smallest fw-bold text-muted">Fee Description</label>
                    <input type="text" class="form-control border-light-blue" v-model="profileForm.fee_description" placeholder="What does the fee cover?">
                  </div>
                </div>
                <div v-if="profileMessage" :class="['alert border-0 rounded-4 mt-3', profileMessage.type === 'success' ? 'alert-success' : 'alert-danger']">{{ profileMessage.text }}</div>
                <button class="btn btn-sky mt-4 px-5 fw-bold rounded-3" @click="saveProfile" :disabled="savingProfile">
                  <span v-if="savingProfile"><span class="spinner-border spinner-border-sm me-2"></span>Saving...</span>
                  <span v-else><i class="fas fa-save me-2"></i> Save Changes</span>
                </button>
              </div>
            </div>

            <div class="col-md-5">
              <div class="card border-0 shadow-sm rounded-4 p-4 text-center mb-4">
                <h6 class="fw-bold text-muted mb-4">License & Verification</h6>
                <div :class="['p-3 rounded-4 mb-3', partner.is_verified ? 'bg-success-subtle' : 'bg-warning-subtle']">
                  <i :class="['fa-2x mb-2', partner.is_verified ? 'fas fa-file-contract text-success' : 'fas fa-clock text-warning']"></i>
                  <p class="mb-0 fw-bold small" :class="partner.is_verified ? 'text-success' : 'text-warning'">{{ partner.license_id }}</p>
                  <small :class="partner.is_verified ? 'text-success' : 'text-warning'">{{ partner.is_verified ? 'Verified & Active  ' : 'Pending Verification ⏳' }}</small>
                </div>
                <div class="p-3 bg-light rounded-4 text-start small">
                  <div class="d-flex justify-content-between py-1 border-bottom"><span class="text-muted">Partner Type</span><strong>{{ partner.partner_type }}</strong></div>
                  <div class="d-flex justify-content-between py-1 border-bottom"><span class="text-muted">Email</span><strong>{{ partner.email }}</strong></div>
                  <div class="d-flex justify-content-between py-1">
                    <span class="text-muted">Live Status</span>
                    <span :class="['badge rounded-pill', partner.is_live ? 'bg-success' : 'bg-warning text-dark']">{{ partner.is_live ? 'LIVE  ' : 'PENDING' }}</span>
                  </div>
                </div>
              </div>
              <div class="card border-0 shadow-sm rounded-4 p-4">
                <h6 class="fw-bold mb-3">Account Stats</h6>
                <div class="d-flex justify-content-between py-2 border-bottom small"><span class="text-muted">Total Donations Received</span><strong>{{ recentDonations.length }}</strong></div>
                <div class="d-flex justify-content-between py-2 border-bottom small"><span class="text-muted">Convenience Fee</span><strong class="text-success">₹{{ partner.convenience_fee || 0 }}</strong></div>
                <div class="d-flex justify-content-between py-2 small"><span class="text-muted">Member Since</span><strong>{{ formatDate(partner.created_at) }}</strong></div>
              </div>
            </div>
          </div>
        </section>


        

      </div>
    </main>

    <div v-if="isMobileMenuOpen" @click="isMobileMenuOpen = false" class="mobile-overlay">


    </div>

  


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
      partner: {},
      loading: true,
      error: null,
      updatingStock: null,
      stockMessage: null,
      stockHistory: [],
      notifs: [],
      overviewStats: [],
      partnerRequests: [],
      searchRefId: '',
      searchResult: null,
      searchError: null,
      searchLoading: false,
      attenderRequests: [],
      attenderLoading: false,
      fulfillingRequest: false,

      // Camp management

      camps: [],
campsLoading: false,
showCreateCamp: false,
creatingCamp: false,
notifyingCamp: null,
campError: null,
campSuccess: null,

// History data 
history: { donor_requests: [], attender_fulfilled: [], inter_partner_requests: [] },
        historyLoading: false,
        historyTab: 'donor',


campForm: {
    title: '',
    description: '',
    location: '',
    camp_date: '',
    start_time: '',
    end_time: '',
    expected_donors: 0,
    blood_groups_needed: []
},
downloadingCamp: null,

allBloodGroups: ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'],

today: new Date().toISOString().split('T')[0],



      // Verify donation
      selectedRequest: null,
      otpCode: '',
      otpResult: null,
      otpLoading: false,
      confirmingDonation: false,
      verifySuccess: null,
      recentDonations: [],

      // Notifications
      notifsLoading: false,

      // Profile
      profileForm: {
        hospital_name: '',
        contact: '',
        address: '',
        city: '',
        state: '',
        facility: '',
        convenience_fee: 0,
        fee_description: '',
      },
      savingProfile: false,
      profileMessage: null,

      // Stock
      stock: {
        'A+': 0, 'A-': 0,
        'B+': 0, 'B-': 0,
        'O+': 0, 'O-': 0,
        'AB+': 0, 'AB-': 0
      },

      // Raise donor
      donorRequest: { blood_group: '', quantity: 1 },
      broadcastLoading: false,
      donorRequestMessage: null,
      activeDonorRequests: [],

      menuItems: [
        { id: 'overview',      label: 'Overview',        icon: 'fas fa-th-large' },
        { id: 'stock',         label: 'Stock Mgmt',      icon: 'fas fa-boxes' },
        { id: 'raise-donor',   label: 'Raise Donor',     icon: 'fas fa-bullhorn' },
        { id: 'view-attender', label: 'Attender Feed',   icon: 'fas fa-user-injured' },
        { id: 'verify',        label: 'Verify Donation', icon: 'fas fa-check-double' },
        { id: 'notifications', label: 'Alerts',          icon: 'fas fa-bell' },
        { id: 'camps',         label: 'Camp Schedule',   icon: 'fas fa-campground' },
        { id: 'profile',       label: 'My Facility',     icon: 'fas fa-hospital-user' },
        { id: 'logout',        label: 'Logout',          icon: 'fas fa-sign-out-alt' },
        { id: 'inter-partner', label: 'Partner Requests', icon: 'fas fa-hospital-user' },
        { id: 'history', label: 'History', icon: 'fas fa-clock-rotate-left' },
      ],

      // Inter partner
interForm: {
    blood_group: '',
    quantity: 1,
    attender_request_id: ''
},
interLoading: false,
interResult: null,
interError: null,
incomingInterRequests: [],
interRequestsLoading: false,
acceptingInterReq: null,
    }
  },

  computed: {
    currentLabel() {
      return this.menuItems.find(i => i.id === this.activeTab)?.label || ''
    },
    partnerInitials() {
      if (!this.partner.hospital_name) return 'JD'
      return this.partner.hospital_name
        .split(' ').map(w => w[0]).join('')
        .substring(0, 2).toUpperCase()
    }
  },

  mounted() {
    this.checkAuth()
    this.savePartnerGPS()
  },

  methods: {

    checkAuth() {
      const token = localStorage.getItem('access_token')
      const userType = localStorage.getItem('user_type')
      if (!token || userType !== 'partner') {
        this.$router.push('/partners_login')
        return
      }
      this.fetchProfile()
    },

    async fetchProfile() {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('http://127.0.0.1:8000/api/partners/profile/', 
  )
       
        this.partner = response.data

      
        this.populateProfileForm()
        await this.fetchStock()
        await this.fetchNotifications()
        await this.buildOverviewStats()
        await this.fetchActiveDonorRequests()
        this.selectedRequest = null
        await this.fetchRecentDonations()
        await this.fetchCamps()
        await this.fetchIncomingInterRequests()  

        
      

      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.removeItem('access_token')
          this.$router.push('/partners_login')
        } else {
          this.error = 'Could not load your profile. Please try again.'
        }
      } finally {
        this.loading = false
      }
    },

    async fetchStock() {
      try {
        const response = await api.get(`http://127.0.0.1:8000/api/stock/partner/${this.partner.id}/`)
        Object.keys(this.stock).forEach(k => this.stock[k] = 0)
        response.data.forEach(item => {
          if (Object.prototype.hasOwnProperty.call(this.stock, item.blood_group)) {
            this.stock[item.blood_group] = item.quantity
          }
        })
      } catch (err) {
        console.error('Stock fetch failed:', err)
      }
    },

    async buildOverviewStats() {
      try {
        const donorReqs = await api.get('http://127.0.0.1:8000/api/requests/donor/list/')
        const activeDonorReqs = donorReqs.data.filter(r => r.status === 'open').length
        const attenderReqs = await api.get('http://127.0.0.1:8000/api/requests/attender/list/')
        const pendingAttenders = attenderReqs.data.length
        const donations = await api.get('http://127.0.0.1:8000/api/donations/partner-history/')
        const totalDonations = donations.data.length
        this.overviewStats = [
          { label: 'Active Donor Requests', val: `${activeDonorReqs} Active`,   color: 'text-sky' },
          { label: 'Pending Attenders',     val: `${pendingAttenders} Requests`, color: 'text-warning' },
          { label: 'Total Donations',        val: `${totalDonations} Received`,  color: 'text-success' },
          { label: 'Convenience Fee',        val: `₹${this.partner.convenience_fee || 0}`, color: 'text-dark' }
        ]
      } catch (err) {
        this.overviewStats = [
          { label: 'Active Donor Requests', val: '0 Active',    color: 'text-sky' },
          { label: 'Pending Attenders',     val: '0 Requests',  color: 'text-warning' },
          { label: 'Total Donations',        val: '0 Received', color: 'text-success' },
          { label: 'Convenience Fee',        val: `₹${this.partner.convenience_fee || 0}`, color: 'text-dark' }
        ]
      }
    },

    async updateStock(bloodGroup) {
  const token = localStorage.getItem('access_token')
  this.updatingStock = bloodGroup
  this.stockMessage = null

  try {
    await api.post(
      'http://127.0.0.1:8000/api/stock/update/',
      {
        blood_group: bloodGroup,
        quantity: this.stock[bloodGroup]
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    this.stockHistory.unshift({
      id: Date.now(),
      blood_group: bloodGroup,
      quantity: this.stock[bloodGroup],
      updated_at: new Date().toISOString()
    })

    await this.fetchProfile()

    this.stockMessage = {
      type: 'success',
      text: `${bloodGroup} stock updated to ${this.stock[bloodGroup]} units successfully!`
    }

    setTimeout(() => { this.stockMessage = null }, 3000)

  } catch (err) {
    console.log("ERROR:", err.response?.data)  
    this.stockMessage = {
      type: 'error',
      text: `Failed to update ${bloodGroup} stock. Please try again.`
    }
  } finally {
    this.updatingStock = null
  }
},

    async broadcastDonorRequest() {
      this.broadcastLoading = true
      this.donorRequestMessage = null
      try {
        await api.post('http://127.0.0.1:8000/api/requests/donor/create/', {
          blood_group: this.donorRequest.blood_group,
          quantity: this.donorRequest.quantity
        })
        this.donorRequestMessage = { type: 'success', text: `Request broadcasted! Nearby ${this.donorRequest.blood_group} donors notified via SMS + WhatsApp  ` }
        this.donorRequest.blood_group = ''
        this.donorRequest.quantity = 1
        await this.fetchActiveDonorRequests()
      } catch (err) {
        this.donorRequestMessage = { type: 'error', text: 'Failed to broadcast request. Please try again.' }
      } finally {
        this.broadcastLoading = false
      }
    },

    // ── KEY FIX: safe partner ID comparison handles both int and object formats
    async fetchActiveDonorRequests() {
  try {
    const response = await api.get('http://127.0.0.1:8000/api/requests/donor/detail/')

    console.log("FULL RESPONSE:", response.data)

    // If backend is correct → no need to filter by partner again
    this.activeDonorRequests = (response.data || []).filter(r =>
      ['open', 'assigned'].includes(r.status)
    )

  } catch (err) {
    console.error('fetchActiveDonorRequests failed:', err)
    this.activeDonorRequests = []
  }
},

    // ── Navigate to Chat.vue — works for both partner and donor since Chat.vue reads user_type from localStorage
    openChat(requestId) {
      this.$router.push(`/chat/${requestId}`)
    },

    async fetchAttenderRequests() {
      this.attenderLoading = true
      try {
        const response = await api.get(`http://127.0.0.1:8000/api/requests/attender/list/?city=${this.partner.city}`)
        this.attenderRequests = Array.isArray(response.data) ? response.data : []
      } catch (err) {
        this.attenderRequests = []
      } finally {
        this.attenderLoading = false
      }
    },
    copyRef(id) {
    navigator.clipboard.writeText(id);
    // You can use a toast or simple alert
    alert("Reference Key copied to clipboard!");
  },

    async searchByRefId() {
      if (!this.searchRefId) return
      this.searchLoading = true
      this.searchResult = null
      this.searchError = null
      try {
        const response = await api.get(`http://127.0.0.1:8000/api/requests/attender/${this.searchRefId}/`)
        this.searchResult = response.data
        if (this.searchResult.status === 'fulfilled') {
          this.searchError = 'This request has already been fulfilled.'
          this.searchResult = null
        } else if (this.searchResult.status === 'expired') {
          this.searchError = 'This request has expired.'
          this.searchResult = null
        }
      } catch (err) {
        this.searchError = 'Reference ID not found. Please check and try again.'
      } finally {
        this.searchLoading = false
      }
    },

    prefillSearch(refId) {
      this.searchRefId = refId
      this.searchByRefId()
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },

    async fulfillAttenderRequest(refId) {
      this.fulfillingRequest = true
      try {
        await api.post(`http://127.0.0.1:8000/api/requests/attender/${refId}/fulfill/`)
        this.searchResult = null
        this.searchRefId = ''
        this.donorRequestMessage = { type: 'success', text: 'Request marked as fulfilled successfully!  ' }
        await this.fetchAttenderRequests()
        await this.buildOverviewStats()
      } catch (err) {
        this.searchError = 'Failed to fulfill request. Please try again.'
      } finally {
        this.fulfillingRequest = false
      }
    },

    async verifyOTP() {
      this.otpLoading = true
      this.otpResult = null
      this.otpError = null
      try {
        const response = await api.post('http://127.0.0.1:8000/api/requests/verify-otp/', { otp_code: this.otpCode })
        this.otpResult = response.data
      } catch (err) {
        this.otpError = err.response?.data?.error || 'Invalid OTP. Please try again.'
      } finally {
        this.otpLoading = false
      }
    },

    async confirmDonation(requestId) {
      this.confirmingDonation = true
      try {
        await api.post(`http://127.0.0.1:8000/api/donations/verify/${requestId}/`)
        this.verifySuccess = 'Donation confirmed successfully! Stock updated automatically '
        this.otpResult = null
        this.otpCode = ''
        await this.fetchStock()
        await this.fetchRecentDonations()
        await this.buildOverviewStats()
        setTimeout(() => { this.verifySuccess = null }, 4000)
      } catch (err) {
        this.otpError = 'Confirmation failed. Please try again.'
      } finally {
        this.confirmingDonation = false
      }
    },

    async fetchRecentDonations() {
      try {
        const response = await api.get('http://127.0.0.1:8000/api/donations/partner-history/')
        this.recentDonations = Array.isArray(response.data) ? response.data : []
      } catch (err) {
        this.recentDonations = []
      }
    },

    async fetchNotifications() {
      this.notifsLoading = true
      try {
        const response = await api.get('http://127.0.0.1:8000/api/notifications/partner/')
        this.notifs = Array.isArray(response.data) ? response.data : []
        this.unreadNotifs = this.notifs.filter(n => n.status === 'pending').length
      } catch (err) {
        this.notifs = []
      } finally {
        this.notifsLoading = false
      }
    },

    async markNotifRead(notifId) {
      try {
        await api.post(`http://127.0.0.1:8000/api/notifications/${notifId}/read/`)
        const notif = this.notifs.find(n => n.id === notifId)
        if (notif) notif.status = 'delivered'
        this.unreadNotifs = this.notifs.filter(n => n.status === 'pending').length
      } catch (err) {
        console.error(err)
      }
    },

    getNotifIcon(trigger) {
      const icons = { donor_request: 'fas fa-user-plus', donor_accepted: 'fas fa-map-marker-alt', bank_verified: 'fas fa-check-circle', request_expiry: 'fas fa-clock', request_fulfilled: 'fas fa-heart', account_locked: 'fas fa-lock', score_updated: 'fas fa-star' }
      return icons[trigger] || 'fas fa-bell'
    },

    getNotifBg(trigger) {
      const bgs = { donor_request: 'bg-warning', donor_accepted: 'bg-sky', bank_verified: 'bg-success', request_expiry: 'bg-danger', request_fulfilled: 'bg-success', account_locked: 'bg-danger', score_updated: 'bg-sky' }
      return bgs[trigger] || 'bg-secondary'
    },

    getNotifTitle(trigger) {
      const titles = { donor_request: 'New Donor Request', donor_accepted: 'Donor Accepted Request', bank_verified: 'Donation Verified', request_expiry: 'Request Expired', request_fulfilled: 'Request Fulfilled', account_locked: 'Account Locked', score_updated: 'Score Updated' }
      return titles[trigger] || 'Notification'
    },

    populateProfileForm() {
      this.profileForm = {
        hospital_name:    this.partner.hospital_name    || '',
        contact:          this.partner.contact          || '',
        address:          this.partner.address          || '',
        city:             this.partner.city             || '',
        state:            this.partner.state            || '',
        facility:         this.partner.facility         || '',
        convenience_fee:  this.partner.convenience_fee  || 0,
        fee_description:  this.partner.fee_description  || '',
      }
    },

    async saveProfile() {
      this.savingProfile = true
      this.profileMessage = null
      try {
        const response = await api.put('http://127.0.0.1:8000/api/partners/profile/', this.profileForm)
        this.partner = { ...this.partner, ...response.data }
        this.profileMessage = { type: 'success', text: 'Profile updated successfully!  ' }
        setTimeout(() => { this.profileMessage = null }, 3000)
      } catch (err) {
        this.profileMessage = { type: 'error', text: 'Failed to save profile. Please try again.' }
      } finally {
        this.savingProfile = false
      }
    },

    async savePartnerGPS() {
      if (!navigator.geolocation) return
      navigator.geolocation.getCurrentPosition(async (pos) => {
        try {
          await api.post('http://127.0.0.1:8000/api/partners/update-location/', { latitude: pos.coords.latitude, longitude: pos.coords.longitude })
        } catch (err) {
          console.error('Failed to save partner GPS:', err)
        }
      })
    },

    timeAgo(dateStr) {
      const diff = Math.floor((new Date() - new Date(dateStr)) / 60000)
      if (diff < 1) return 'Just now'
      if (diff < 60) return `${diff} mins ago`
      if (diff < 1440) return `${Math.floor(diff / 60)} hrs ago`
      return `${Math.floor(diff / 1440)} days ago`
    },

    formatDate(dateStr) {
      if (!dateStr) return 'N/A'
      return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
    },

    navigate(id) {
      if (id === 'logout') {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user_type')
        localStorage.removeItem('partner')
        this.$router.push('/')
        return
      }

      if (id === 'history' && this.history.donor_requests.length === 0) {
        this.fetchHistory()
    }

       



      this.activeTab = id
      this.isMobileMenuOpen = false
    },

    

    // ── CAMP MANAGEMENT METHODS

    // ── Toggle blood group selection ─────────
toggleBloodGroup(bg) {
    const idx = this.campForm.blood_groups_needed.indexOf(bg)
    if (idx === -1) {
        this.campForm.blood_groups_needed.push(bg)
    } else {
        this.campForm.blood_groups_needed.splice(idx, 1)
    }
},

// ── Create camp ──────────────────────────
async createCamp() {
    if (!this.campForm.title || !this.campForm.camp_date ||
        !this.campForm.start_time || !this.campForm.end_time) {
        this.campError = 'Please fill all required fields.'
        return
    }

    this.creatingCamp = true
    this.campError = null

    try {
        await api.post('http://127.0.0.1:8000/api/partners/camps/create/', this.campForm)

        this.campSuccess = 'Camp created! Click Notify to alert nearby donors.'

        // Reset form
        this.campForm = {
            title: '', description: '', location: '',
            camp_date: '', start_time: '', end_time: '',
            expected_donors: 0, blood_groups_needed: []
        }

        // Refresh camps
        await this.fetchCamps()

        setTimeout(() => {
            this.campSuccess = null
            this.showCreateCamp = false
        }, 2000)

    } catch (err) {
        this.campError = err.response?.data?.error || 'Failed to create camp.'
    } finally {
        this.creatingCamp = false
    }
},

// ── Fetch camps ──────────────────────────
async fetchCamps() {
    this.campsLoading = true
    try {
        const response = await api.get('http://127.0.0.1:8000/api/partners/camps/')
        this.camps = Array.isArray(response.data) ? response.data : []
    } catch (err) {
        this.camps = []
    } finally {
        this.campsLoading = false
    }
},

// ── Schedule & Notify ────────────────────
async scheduleAndNotify(campId) {
    this.notifyingCamp = campId
    try {
        const response = await api.post(`http://127.0.0.1:8000/api/partners/camps/${campId}/notify/`)
        alert(`  ${response.data.message}`)
        await this.fetchCamps()
    } catch (err) {
        alert('Failed to notify. Please try again.')
    } finally {
        this.notifyingCamp = null
    }
},


// ── Check camp date passed ───────────────
isCampPast(camp) {
    return new Date(camp.camp_date) < new Date()
},

// ── Check if camp is today ───────────────
isCampToday(camp) {
    const today = new Date().toISOString().split('T')[0]
    return camp.camp_date === today
},

removeOTP(text) {
  if (!text) return ''

  // remove OTP patterns like "OTP: 123456" or "OTP 123456"
  return text.replace(/otp[:\s]*\d+/gi, '').trim()
},

// inter partner request

// ── Raise inter partner request ──────────
async raiseInterPartnerRequest() {
    this.interLoading = true
    this.interResult = null
    this.interError = null

    try {
        const response = await api.post(
            'http://127.0.0.1:8000/api/partners/inter-request/',
            this.interForm
        )
        this.interResult = response.data
        this.interForm = {
            blood_group: '',
            quantity: 1,
            attender_request_id: ''
        }
        await this.fetchIncomingInterRequests()
    } catch (err) {
        this.interError = err.response?.data?.error ||
            'Failed to raise request. Try again.'
    } finally {
        this.interLoading = false
    }
},

// ── Fetch incoming inter requests ────────
async fetchIncomingInterRequests() {
    this.interRequestsLoading = true
    try {
        const response = await api.get('http://127.0.0.1:8000/api/partners/inter-requests/')
        this.incomingInterRequests = Array.isArray(response.data)
            ? response.data : []
    } catch (err) {
        this.incomingInterRequests = []
    } finally {
        this.interRequestsLoading = false
    }
},

// ── Accept inter partner request ─────────
async acceptInterRequest(reqId) {
    this.acceptingInterReq = reqId
    try {
        await api.post(`http://127.0.0.1:8000/api/partners/inter-requests/${reqId}/accept/`)
        alert('Request fulfilled! Stock updated  ')
        await this.fetchIncomingInterRequests()
        await this.fetchStock()
    } catch (err) {
        alert(err.response?.data?.error || 'Failed to accept.')
    } finally {
        this.acceptingInterReq = null
    }
},

// ── Download CSV ─────────────────────────
async downloadEnrollments(camp) {
    this.downloadingCamp = camp.id

    try {
        const token = localStorage.getItem('access_token')

        const response = await fetch(
            `http://127.0.0.1:8000/api/partners/camps/${camp.id}/download/`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        )

        if (!response.ok) {
            const err = await response.json()
            alert(err.error || 'Download failed.')
            return
        }

        // Create download link
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `JeevanDaan_${camp.title}_${camp.camp_date}.csv`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)

    } catch (err) {
        alert('Download failed. Please try again.')
        console.error(err)
    } finally {
        this.downloadingCamp = null
    }
},

// fetch history
async fetchHistory() {
    this.historyLoading = true
    try {
        const response = await api.get('http://127.0.0.1:8000/api/requests/partner/history/')
        this.history = response.data
    } catch (err) {
        console.error('History fetch failed:', err)
    } finally {
        this.historyLoading = false
    }
},




// ── Go to stock update ───────────────────
goToStockUpdate() {
    this.activeTab = 'stock'
},



  }
}
</script>

<style scoped>
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

.sidebar { width: 280px; height: 100vh; position: sticky; top: 0; z-index: 1000; transition: 0.3s; }
@media (max-width: 768px) {
  .sidebar { position: fixed; left: -280px; top: 0; }
  .sidebar.show { left: 0; }
  .mobile-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); z-index: 999; }
}

.logo-box { width: 40px; height: 40px; background: #00AEEF; color: white; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 900; }
.menu-btn { padding: 14px 20px; border-radius: 12px; font-weight: 500; color: #666; transition: 0.2s; border: none; background: transparent; text-align: left; }
.menu-btn.active { background: #E1F5FE; color: #00AEEF; font-weight: 700; }
.stock-card { border-top: 4px solid #00AEEF !important; transition: transform 0.2s; }
.stock-card:hover { transform: translateY(-5px); }
.avatar-circle { width: 40px; height: 40px; background: #00AEEF; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; }
.notif-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; }

.fw-800 { font-weight: 800; }
.smallest { font-size: 0.7rem; }
.animate-fade { animation: fadeIn 0.4s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.border-dashed { border: 2px dashed #B3E5FC; }


.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.7); /* Darker backdrop */
  backdrop-filter: blur(5px);
  z-index: 2000;
}

.hover-zoom {
  transition: transform 0.2s ease;
  cursor: zoom-in;
}

.hover-zoom:hover {
  transform: scale(1.03);
}

.fw-mono {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
}

.text-sky-light {
  color: #a5f3fc;
}

/* Frozen state for Sidebar Buttons */
.menu-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed !important;
  pointer-events: none; /* Isse click bilkul block ho jayega */
  filter: grayscale(0.8);
}

/* Sidebar mein lock icon ke liye thodi styling */
.fa-lock {
  font-size: 0.75rem;
  color: #dc3545; /* Red color for lock */
}
</style>