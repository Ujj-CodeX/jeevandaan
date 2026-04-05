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
            <li class="nav-item"><RouterLink class="nav-link active" to="/user">Dashboard</RouterLink></li>
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
                    <input type="text" v-model="aadhaarNumber" class="form-control" placeholder="12 Digit Number" maxlength="12">
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
      <!-- Add in profile section right side card -->
<div class="card border-0 shadow-sm rounded-4 p-4 mt-4">
    <h6 class="fw-bold mb-4">Change Password</h6>

    <div class="mb-3">
        <label class="smallest fw-bold text-muted">Current Password</label>
        <input type="password" class="form-control"
            v-model="passwordForm.current_password"
            placeholder="Enter current password">
    </div>
    <div class="mb-3">
        <label class="smallest fw-bold text-muted">New Password</label>
        <input type="password" class="form-control"
            v-model="passwordForm.new_password"
            placeholder="Min 8 chars, alphanumeric">
    </div>
    <div class="mb-4">
        <label class="smallest fw-bold text-muted">Confirm New Password</label>
        <input type="password" class="form-control"
            v-model="passwordForm.confirm_password"
            placeholder="Re-enter new password">
    </div>

    <div v-if="passwordMessage"
        :class="['alert border-0 rounded-4 small',
            passwordMessage.type === 'success' ?
            'alert-success' : 'alert-danger']">
        {{ passwordMessage.text }}
    </div>

    <button class="btn btn-danger fw-bold rounded-3 px-4"
        @click="changePassword"
        :disabled="changingPassword">
        <span v-if="changingPassword">
            <span class="spinner-border spinner-border-sm me-2"></span>
        </span>
        <span v-else>
            <i class="fas fa-lock me-2"></i> Change Password
        </span>
    </button>
    <button class="btn btn-link text-muted small w-100 mt-2"
            @click="showPasswordModal = false">
            Cancel
        </button>
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
      authError: '',

      passwordForm: {
      current_password: '',
      new_password: '',
      confirm_password: ''
},
changingPassword: false,
passwordMessage: null,
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
    },
    async changePassword() {
    if (!this.passwordForm.current_password ||
        !this.passwordForm.new_password) {
        this.passwordMessage = {
            type: 'error',
            text: 'All fields are required.'
        }
        return
    }

    if (this.passwordForm.new_password !==
        this.passwordForm.confirm_password) {
        this.passwordMessage = {
            type: 'error',
            text: 'New passwords do not match.'
        }
        return
    }

    if (this.passwordForm.new_password.length < 8) {
        this.passwordMessage = {
            type: 'error',
            text: 'Password must be at least 8 characters.'
        }
        return
    }

    this.changingPassword = true
    this.passwordMessage = null

    try {
        await api.post('/api/users/change-password/', {
            current_password: this.passwordForm.current_password,
            new_password: this.passwordForm.new_password
        })

        this.passwordMessage = {
            type: 'success',
            text: 'Password changed successfully! '
        }
        this.passwordForm = {
            current_password: '',
            new_password: '',
            confirm_password: ''
        }
        setTimeout(() => {
            this.passwordMessage = null
        }, 3000)

    } catch (err) {
        this.passwordMessage = {
            type: 'error',
            text: err.response?.data?.error || 'Failed. Please try again.'
        }
    } finally {
        this.changingPassword = false
    }
},
logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      this.$router.push('/')
    },
    async saveProfile() {
      this.saving = true;
  try {
    const payload = {
      name: this.user.name,
      phone_number: this.user.phone_number,
      blood_group: this.user.blood_group,
      address: this.user.address
    };

    const res = await api.put('/api/users/update-profile/', payload);

    // Update local state (important)
    this.user = res.data;

    alert("Profile updated successfully!");

  } catch (err) {
    console.error(err);
    alert(err.response?.data?.error || "Failed to update profile.");
  }
}
  }
}
</script>
<style>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: whitesmoke;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}
</style>