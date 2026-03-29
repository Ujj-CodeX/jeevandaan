<template>
  <div class="admin-panel bg-light min-vh-100">
    <nav class="navbar navbar-dark bg-dark-red shadow-sm py-3 sticky-top">
      <div class="container-fluid px-4">
        <span class="navbar-brand fw-800 fs-4">
          <i class="fas fa-user-shield me-2"></i> JEEVANDAAN+ <span class="fw-light">ADMIN</span>
        </span>
        <div class="d-flex align-items-center gap-3">
          <span class="text-white-50 small">Varanasi Hub Active</span>
          <div class="admin-avatar shadow-sm">JD</div>
        </div>
      </div>
    </nav>

    <div class="container-fluid px-4 mt-4">
      <ul class="nav nav-pills admin-tabs p-2 bg-white rounded-4 shadow-sm mb-4">
        <li class="nav-item flex-fill">
          <button @click="activeTab = 'users'" :class="['nav-link w-100 fw-bold', activeTab === 'users' ? 'active' : '']">
            <i class="fas fa-users me-2"></i> User Management
          </button>
        </li>
        <li class="nav-item flex-fill">
          <button @click="activeTab = 'partners'" :class="['nav-link w-100 fw-bold', activeTab === 'partners' ? 'active' : '']">
            <i class="fas fa-hospital-user me-2"></i> Partner Management
          </button>
        </li>
        <li class="nav-item flex-fill">
          <button @click="activeTab = 'actions'" :class="['nav-link w-100 fw-bold', activeTab === 'actions' ? 'active' : '']">
            <i class="fas fa-bolt me-2"></i> Critical Actions
          </button>
        </li>
      </ul>

      <div v-if="activeTab === 'users'" class="animate__animated animate__fadeIn">
        <div class="row g-4 mb-4">
          <div class="col-md-4" v-for="stat in userStats" :key="stat.label">
            <div class="stat-card p-4 rounded-4 bg-white shadow-sm border-start border-5 border-danger">
              <h6 class="text-muted fw-bold text-uppercase smaller mb-1">{{ stat.label }}</h6>
              <h2 class="fw-800 mb-0">{{ stat.val }}</h2>
            </div>
          </div>
        </div>

        <div class="row g-4 mb-4">
          <div class="col-lg-6">
            <div class="card border-0 shadow-sm rounded-4 p-4">
              <h5 class="fw-800 mb-4">Requests by Region</h5>
              <div class="chart-placeholder bg-light rounded-4 d-flex align-items-center justify-content-center">
                <p class="text-muted small">[ Bar Chart: Varanasi, Deoria, Lucknow, Delhi ]</p>
              </div>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="card border-0 shadow-sm rounded-4 p-4">
              <h5 class="fw-800 mb-4">Donor Distribution</h5>
              <div class="chart-placeholder bg-light rounded-4 d-flex align-items-center justify-content-center">
                <p class="text-muted small">[ Pie Chart: Regional Donor Densities ]</p>
              </div>
            </div>
          </div>
        </div>

        <div class="card border-0 shadow-sm rounded-4 p-4 mb-5">
          <h5 class="fw-800 mb-3">Lookup User Details</h5>
          <div class="input-group input-group-lg search-box">
            <span class="input-group-text bg-white border-end-0"><i class="fas fa-search text-muted"></i></span>
            <input type="text" class="form-control border-start-0 ps-0" placeholder="Enter Username (e.g. prince_babu)">
            <button class="btn btn-danger px-5 fw-bold">SEARCH</button>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'partners'" class="animate__animated animate__fadeIn">
        <div class="row g-4 mb-4">
          <div class="col-md-6">
            <div class="card border-0 shadow-sm rounded-4 p-4 bg-jd-red text-white">
              <h6>ACTIVE PARTNERS</h6>
              <h1 class="display-4 fw-800">142</h1>
            </div>
          </div>
          <div class="col-md-6">
            <div class="card border-0 shadow-sm rounded-4 p-4">
              <h5 class="fw-800 mb-3">Camp Frequency by Region</h5>
              <div class="chart-placeholder-sm bg-light rounded-3"></div>
            </div>
          </div>
        </div>

        <h5 class="fw-800 mb-3 px-2">Partners Needing Verification</h5>
        <div class="row g-3 mb-4">
          <div class="col-md-6" v-for="p in pendingPartners" :key="p.name">
            <div class="card border-0 shadow-sm rounded-4 p-3 partner-verify-card" @click="openPartnerModal(p)">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="fw-800 mb-0">{{ p.name }}</h6>
                  <small class="text-muted">{{ p.location }} • {{ p.type }}</small>
                </div>
                <span class="badge bg-warning-subtle text-warning px-3 py-2 rounded-pill">PENDING</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="card border-0 shadow-sm rounded-4 p-4">
          <h5 class="fw-800 mb-3">Search Partner Database</h5>
          <div class="input-group">
            <input type="text" class="form-control" placeholder="Enter License No or Partner Name">
            <button class="btn btn-dark fw-bold">LOOKUP</button>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'actions'" class="animate__animated animate__fadeIn">
        <div class="row g-4">
          <div class="col-lg-4">
            <div class="card border-0 shadow-sm rounded-4 p-4 h-100">
              <h5 class="fw-800 text-danger mb-4"><i class="fas fa-id-card me-2"></i>Aadhar Verification</h5>
              <div class="mb-3">
                <label class="small fw-bold mb-1">Enter 12 Digit Aadhar</label>
                <input type="text" class="form-control bg-light border-0" placeholder="XXXX XXXX XXXX">
              </div>
              <button class="btn btn-outline-danger w-100 fw-bold">VERIFY IDENTITY</button>
            </div>
          </div>

          <div class="col-lg-8">
            <div class="card border-0 shadow-sm rounded-4 p-4 mb-4">
              <h5 class="fw-800 mb-4">Quick Governance</h5>
              <div class="table-responsive">
                <table class="table table-hover align-middle">
                  <thead class="bg-light">
                    <tr>
                      <th>Entity Name</th>
                      <th>Type</th>
                      <th>Risk Level</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in flaggedEntities" :key="item.name">
                      <td><strong>{{ item.name }}</strong></td>
                      <td><span class="badge bg-light text-dark border">{{ item.type }}</span></td>
                      <td><span :class="['small fw-bold', item.risk === 'High' ? 'text-danger' : 'text-warning']">{{ item.risk }}</span></td>
                      <td>{{ item.status }}</td>
                      <td>
                        <button v-if="item.status === 'Active'" class="btn btn-sm btn-danger rounded-3 fw-bold">BLOCK</button>
                        <button v-else class="btn btn-sm btn-success rounded-3 fw-bold px-3">UNBLOCK</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div class="card border-0 shadow-sm rounded-4 p-4">
              <h5 class="fw-800 mb-4">User Feedback & Disputes</h5>
              <div class="complaint-item border-bottom pb-3 mb-3" v-for="c in complaints" :key="c.id">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <h6 class="fw-bold text-danger mb-0">#{{ c.id }} - {{ c.subject }}</h6>
                  <small class="text-muted">{{ c.date }}</small>
                </div>
                <p class="small text-secondary mb-1">"{{ c.msg }}"</p>
                <small class="fw-bold">From: {{ c.from }} | Reported Entity: {{ c.target }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showPModal" class="modal-overlay" @click.self="showPModal = false">
      <div class="partner-card-modal shadow-lg p-5 rounded-5 animate__animated animate__zoomIn">
        <h3 class="fw-800 mb-4">{{ selectedPartner.name }}</h3>
        <div class="row mb-4">
          <div class="col-6">
            <small class="text-muted d-block">License Number</small>
            <p class="fw-bold">UP-8921-BLOOD-B</p>
          </div>
          <div class="col-6">
            <small class="text-muted d-block">Owner/Admin</small>
            <p class="fw-bold">Mr. Rajesh Upadhyay</p>
          </div>
        </div>
        <div class="bg-light p-3 rounded-4 mb-4">
          <small class="text-muted d-block">Full Address</small>
          <p class="mb-0">Civil Lines, Near DM Office, Deoria, UP 274001</p>
        </div>
        <div class="d-flex gap-2">
          <button class="btn btn-success flex-grow-1 fw-bold py-3 rounded-4" @click="showPModal = false">APPROVE PARTNER</button>
          <button class="btn btn-outline-danger fw-bold py-3 px-4 rounded-4" @click="showPModal = false">REJECT</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeTab: 'users',
      showPModal: false,
      selectedPartner: {},
      userStats: [
        { label: 'Active Users', val: '8,421' },
        { label: 'Weekly Requests', val: '154' },
        { label: 'Monthly Growth', val: '+22%' }
      ],
      pendingPartners: [
        { name: 'Upadhyay Blood Care', location: 'Deoria', type: 'Private Bank' },
        { name: 'City Hospital Varanasi', location: 'Varanasi', type: 'Hospital' }
      ],
      flaggedEntities: [
        { name: 'Rahul_99', type: 'User', risk: 'High', status: 'Blocked' },
        { name: 'Apex Diagnostic', type: 'Partner', risk: 'Medium', status: 'Active' }
      ],
      complaints: [
        { id: '402', subject: 'Extra Charges', from: 'Amit K.', target: 'XYZ Center', msg: 'They asked for more than processing fees.', date: 'Mar 26' },
        { id: '399', subject: 'Donation Denial', from: 'Sana R.', target: 'City Bank', msg: 'Donor was ready but they refused to scan QR.', date: 'Mar 25' }
      ]
    }
  },
  methods: {
    openPartnerModal(partner) {
      this.selectedPartner = partner;
      this.showPModal = true;
    }
  }
}
</script>

<style scoped>
.fw-800 { font-weight: 800; }
.bg-dark-red { background: #9b1c1c; }
.bg-jd-red { background: #D32F2F; }
.admin-tabs .nav-link { color: #666; transition: 0.3s; padding: 12px; border-radius: 12px; }
.admin-tabs .nav-link.active { background: #D32F2F !important; color: white !important; }
.admin-avatar { width: 40px; height: 40px; background: white; color: #D32F2F; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: 900; }

.chart-placeholder { height: 300px; border: 2px dashed #eee; }
.chart-placeholder-sm { height: 120px; border: 2px dashed #eee; }

.partner-verify-card { cursor: pointer; border-left: 4px solid #ffc107; transition: 0.2s; }
.partner-verify-card:hover { transform: scale(1.02); box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important; }

.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); backdrop-filter: blur(5px); z-index: 3000; display: flex; align-items: center; justify-content: center; }
.partner-card-modal { background: white; width: 100%; max-width: 500px; border-top: 10px solid #2ECC71; }

.smaller { font-size: 0.7rem; }
.table th { font-size: 0.8rem; text-transform: uppercase; color: #888; }
</style>