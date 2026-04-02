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
  <div class="profile-page animate-fade p-3 p-md-4">
    <div class="row g-4">
      
      <div class="col-lg-4">
        <div class="card border-0 shadow-sm rounded-4 text-center p-4 mb-4">
          <div class="position-relative d-inline-block mx-auto mb-3">
            <div class="avatar-circle shadow-sm bg-sky-soft d-flex align-items-center justify-content-center">
              <span class="h1 mb-0 text-sky fw-bold">{{ user.name?.charAt(0) }}</span>
            </div>
            <span v-if="user.is_aadhaar_verified" class="position-absolute bottom-0 end-0 bg-success rounded-circle p-1 border border-white" title="Verified">
              <i class="fas fa-check text-white smallest"></i>
            </span>
          </div>
          <h5 class="fw-800 mb-0">{{ user.name }}</h5>
          <p class="text-muted small">@{{ user.username }}</p>
          <span class="badge bg-danger-soft text-danger px-3 py-2 rounded-pill fw-bold">
            <i class="fas fa-medal me-1"></i> {{ user.member_tag }}
          </span>
        </div>

        <div class="card border-0 shadow-sm rounded-4 p-4">
          <h6 class="fw-bold mb-3">Donation Impact</h6>
          <div class="row g-3">
            <div class="col-6">
              <div class="bg-light rounded-3 p-3 text-center">
                <small class="text-muted d-block">Score</small>
                <span class="fw-bold h5 text-sky">{{ user.reliability_score }}%</span>
              </div>
            </div>
            <div class="col-6">
              <div class="bg-light rounded-3 p-3 text-center">
                <small class="text-muted d-block">Donations</small>
                <span class="fw-bold h5 text-danger">{{ user.total_donations }}</span>
              </div>
            </div>
          </div>
          <div class="mt-3 small text-muted text-center">
            <i class="fas fa-info-circle me-1"></i> 
            Raised {{ user.total_requests_raised }} requests for others.
          </div>
        </div>
      </div>

      <div class="col-lg-8">
        <div class="card border-0 shadow-sm rounded-4 p-4">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h5 class="fw-bold mb-0">Personal Information</h5>
            <button class="btn btn-sky-outline btn-sm" @click="showPasswordModal = true">
              <i class="fas fa-key me-1"></i> Change Password
            </button>
          </div>

          <form @submit.prevent="saveProfile">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="small text-muted fw-bold">Full Name</label>
                <input type="text" v-model="user.name" class="form-control rounded-3">
              </div>
              <div class="col-md-6">
                <label class="small text-muted fw-bold">Email (Static)</label>
                <input type="text" :value="user.email" class="form-control rounded-3 bg-light" disabled>
              </div>
              <div class="col-md-6">
                <label class="small text-muted fw-bold">Phone Number</label>
                <input type="text" v-model="user.phone_number" class="form-control rounded-3">
              </div>
              <div class="col-md-6">
                <label class="small text-muted fw-bold">Blood Group</label>
                <select v-model="user.blood_group" class="form-select rounded-3">
                  <option v-for="g in ['A+','A-','B+','B-','O+','O-','AB+','AB-']" :key="g">{{g}}</option>
                </select>
              </div>
              <div class="col-12">
                <label class="small text-muted fw-bold">Home Address</label>
                <textarea v-model="user.address" class="form-control rounded-3" rows="2"></textarea>
              </div>

              <div class="col-12 mt-4" v-if="!user.is_aadhaar_verified">
                <div class="p-3 border-dashed rounded-4 bg-light">
                  <h6 class="fw-bold small mb-2"><i class="fas fa-id-card me-2"></i>Link Aadhaar Card</h6>
                  <p class="smallest text-muted mb-3">Required for "Verified" badge and emergency network priority.</p>
                  <div class="input-group input-group-sm mb-2" style="max-width: 350px;">
                    <input type="text" v-model="aadhaarInput" class="form-control" placeholder="12 Digit Number" maxlength="12">
                    <button class="btn btn-dark" type="button" @click="submitAadhaar" :disabled="aadhaarLoading">Verify</button>
                  </div>
                  <small v-if="user.aadhaar_number" class="text-warning">Status: Pending Verification</small>
                </div>
              </div>

              <div class="col-12 mt-3">
                <div class="d-flex justify-content-between align-items-center bg-sky-soft p-3 rounded-3">
                  <div class="small">
                    <i class="fas fa-map-marker-alt text-danger me-2"></i>
                    <strong>Live Location:</strong> {{ user.latitude ? 'GPS Linked' : 'Allow Location Access' }}
                  </div>
                  
                </div>
              </div>

              <div class="col-12 text-end mt-4">
                <button type="submit" class="btn btn-success px-5 py-2 fw-800 rounded-pill shadow" :disabled="saving">
                  <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                  SAVE CHANGES
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showPasswordModal" class="modal-backdrop d-flex align-items-center justify-content-center p-3 z-3">
      <div class="card border-0 shadow-lg rounded-4 overflow-hidden w-100 animate-slide-up" style="max-width: 420px;">
        <div class="bg-dark p-3 text-white d-flex justify-content-between align-items-center">
          <h6 class="mb-0 fw-bold"><i class="fas fa-lock me-2"></i>Security Check</h6>
          <i class="fas fa-times pointer" @click="closePasswordModal"></i>
        </div>
        <div class="card-body p-4">
          <div v-if="!identityVerified">
            <p class="small text-muted mb-3">To change password, confirm your <strong>Email or Username</strong>.</p>
            <input type="text" v-model="verifyField" class="form-control mb-3" placeholder="Enter Email or Username">
            <button class="btn btn-sky w-100 fw-bold" @click="checkIdentity">Continue</button>
          </div>
          <div v-else>
            <label class="smallest text-muted fw-bold">NEW PASSWORD</label>
            <input type="password" v-model="passForm.new" class="form-control mb-2" placeholder="••••••••">
            <label class="smallest text-muted fw-bold">CONFIRM NEW PASSWORD</label>
            <input type="password" v-model="passForm.confirm" class="form-control mb-3" placeholder="••••••••">
            <button class="btn btn-success w-100 fw-bold" @click="confirmPasswordChange" :disabled="savingPass">
              Update Securely
            </button>
          </div>
          <div v-if="passError" class="alert alert-danger smallest py-2 mt-3">{{ passError }}</div>
        </div>
      </div>
    </div>
  </div>
  
  </div>
</template>
<script>
import api from '@/api/index.js';

export default {
  data() {
    return {
      user: {},
      updating: false,
      aadhaarNumber: '',
      showPasswordModal: false,
      identityConfirmed: false,
      confirmIdentifier: '',
      newPassword: '',
      confirmNewPassword: '',
      authError: '',
    }
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      const res = await api.get('/api/users/profile/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      this.user = res.data;
    },
    async submitAadhaar() {
      if(this.aadhaarNumber.length !== 12) return alert("Invalid Aadhaar Number");
      try {
        await api.post('/api/users/verify-aadhaar/', { aadhaar_no: this.aadhaarNumber });
        this.user.aadhaar_status = 'pending';
        alert("Aadhaar submitted. Verification is pending.");
      } catch (err) { alert("Submission failed."); }
    },
    verifyIdentity() {
      if (this.confirmIdentifier === this.user.email || this.confirmIdentifier === String(this.user.id)) {
        this.identityConfirmed = true;
        this.authError = '';    
      } else {
        this.authError = "Identity match failed. Check your Email/ID.";
      }
    },
    async updatePassword() {
      if(this.newPassword !== this.confirmNewPassword) return this.authError = "Passwords do not match";
      try {
        await api.post('/api/users/change-password/', { password: this.newPassword });
        alert("Password updated successfully!");
        this.showPasswordModal = false;
        this.identityConfirmed = false;
      } catch (err) { this.authError = "Update failed."; }
    }
  }
}
</script>