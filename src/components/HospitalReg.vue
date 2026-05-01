<template>
  <div>
    <div class="card main-card">
      <div class="row g-0">
        <div class="col-md-5 illustration-side d-none d-md-flex text-center">
          <img src="https://img.freepik.com/free-vector/hospital-building-concept-illustration_114360-8440.jpg" alt="Hospital Care" style="width: 90%;">
          <h5 class="mt-4 fw-bold text-primary">Healthcare Partnership</h5>
          <p class="text-muted small px-4">Register your medical facility to streamline blood and organ donation workflows.</p>
        </div>

        <div class="col-md-7 login-side">
          <div class="brand-logo">
            <i class="fa-solid fa-hospital-user"></i> JeevanDaan+ <span class="badge bg-primary fs-6">PARTNERS</span>
          </div>
          <h2 class="fw-bold">Facility Registration</h2>
          <p class="text-muted small mb-4">Join the network to manage donor requests and emergency supplies.</p>

          <form @submit.prevent="handleRegister">
            <div class="row">
              <div class="col-md-6">
                <div class="input-group-custom">
                  <i class="fa-solid fa-hospital text-muted"></i>
                  <input type="text" v-model="form.hospital_name" placeholder="Hospital Name" required maxlength="100">
                </div>
              </div>
              <div class="col-md-6">
                <div class="input-group-custom">
                  <i class="fa-solid fa-id-card text-muted"></i>
                  <input type="text" v-model="form.license_id" placeholder="Reg/License ID" required maxlength="50">
                </div>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <div class="input-group-custom">
                  <i class="fa-solid fa-phone-volume text-muted"></i>
                  <input type="tel" v-model="form.contact" @input="handlePhone" placeholder="Emergency Contact" required>
                </div>
              </div>
              <div class="col-md-6">
                <div class="input-group-custom">
                  <i class="fa-solid fa-layer-group text-muted"></i>
                  <select v-model="form.partner_type" required class="form-control">
                    <option disabled value="">Facility Type</option>
                    <option value="government">Government</option>
                    <option value="private_multi_specialty">Private Multi-specialty</option>
                    <option value="blood_bank">Blood Bank</option>
                  </select>
                </div>
              </div>
            </div>

            <div class="input-group-custom">
              <i class="fa-solid fa-envelope text-muted"></i>
              <input type="email" v-model="form.email" placeholder="Official Email Address" required>
            </div>
            <div class="input-group-custom">
    <i class="fa-solid fa-map-marker-alt text-muted"></i>
    <input type="text" v-model="form.address" placeholder="Full Address" required maxlength="200">
</div>

<div class="row">
    <div class="col-md-6">
        <div class="input-group-custom">
            <i class="fa-solid fa-city text-muted"></i>
            <input type="text" v-model="form.city" placeholder="City" @input="handleCity('city')" required>
        </div>
    </div>
    <div class="col-md-6">
        <div class="input-group-custom">
            <i class="fa-solid fa-map text-muted"></i>
            <select v-model="form.state" required class="form-control">
  <option disabled value="">Select State</option>
  <option>Uttar Pradesh</option>
  <option>Maharashtra</option>
  <option>Bihar</option>
  <option>West Bengal</option>
  <option>Madhya Pradesh</option>
  <option>Tamil Nadu</option>
  <option>Rajasthan</option>
  <option>Karnataka</option>
  <option>Gujarat</option>
  <option>Andhra Pradesh</option>
  <option>Odisha</option>
  <option>Telangana</option>
  <option>Kerala</option>
  <option>Jharkhand</option>
  <option>Assam</option>
  <option>Punjab</option>
  <option>Chhattisgarh</option>
  <option>Haryana</option>
  <option>Uttarakhand</option>
  <option>Himachal Pradesh</option>
  <option>Tripura</option>
  <option>Meghalaya</option>
  <option>Manipur</option>
  <option>Nagaland</option>
  <option>Goa</option>
  <option>Arunachal Pradesh</option>
  <option>Mizoram</option>
  <option>Sikkim</option>
</select>
        </div>
    </div>
</div>

<div class="input-group-custom">
    <i class="fa-solid fa-notes-medical text-muted"></i>
    <input type="text" v-model="form.facility" placeholder="Facility Description (e.g. 24/7 Blood Bank)" required>
</div>

<div class="input-group-custom">
    <i class="fa-solid fa-indian-rupee-sign text-muted"></i>
    <input type="number" v-model="form.convenience_fee" placeholder="Convenience Fee (₹)" min="0" required>
</div>

            <div class="input-group-custom mb-2" style="position: relative;">
              <i class="fa-solid fa-lock text-muted"></i>
              <input type="password" id="hosp-pw" v-model="form.password" placeholder="Create Admin Password" required>
              <i class="fa-solid fa-eye toggle-eye" @click="togglePassword('hosp-pw', $event.target)"></i>
            </div>

            <div class="restriction-text">
              <span id="hChar" class="req"><i class="fa-solid fa-circle-check"></i> 8+ Characters</span>
              <span id="hAlpha" class="req"><i class="fa-solid fa-circle-check"></i> Alpha-numeric</span>
            </div>

            <div class="form-check mb-4">
              <input class="form-check-input" type="checkbox" id="hTerms"
                v-model="termsAccepted" required>
              <label class="form-check-label text-muted small" for="hTerms">
                We agree to the
                <a href="#" @click.prevent="openTermsModal" class="text-primary fw-bold text-decoration-none">
                  Partner Terms
                </a>
              </label>
            </div>

            
<div v-if="error" class="alert-custom error mb-3">
    <i class="fa-solid fa-circle-exclamation"></i> {{ error }}
</div>


<div v-if="success" class="alert-custom success mb-3">
    <i class="fa-solid fa-circle-check"></i> {{ success }}
</div>

<button type="submit" class="btn-hospital" :disabled="!termsAccepted || loading">
    <span v-if="loading">Registering...</span>
    <span v-else>Register Facility</span>
</button>
            <p class="text-center mt-3 text-muted small">Already registered?
              <RouterLink to="/partners_login" class="text-primary fw-bold text-decoration-none">Partner Login</RouterLink>
            </p>
          </form>
        </div>
      </div>
    </div>

    <!--   Vue Modal -->
    <div v-if="showTermsModal" class="modal-overlay" @click.self="closeTermsModal">
      <div class="modal-box">
        <div class="modal-box-header">
          <h5 class="fw-bold mb-0">Partners Terms of Use</h5>
          <button class="btn-close" @click="closeTermsModal"></button>
        </div>
        <div class="modal-box-body text-muted small">
  <p>1. Facilities must maintain accurate, real-time updates of blood stock availability.</p>
  <p>2. Request handling must be timely and precise to ensure rapid response in emergency situations.</p>
  <p>3. Facilities must not require or request replacement donors in exchange for providing blood.</p>
  <p>4. Blood stock must be updated immediately after fulfillment of any request or donation.</p>
  <p>5. Stock updates after blood donation camps must be recorded promptly and accurately.</p>
  <p>6. All activities must comply with JeevanDaan+ policies and applicable health regulations.</p>
  <p>7. Any misuse, false reporting, or policy violation may result in administrative action or legal consequences.</p>
</div>
        <div class="modal-box-footer">
          <button class="btn btn-primary w-100 rounded-pill" @click="acceptTerms">
            I Understand
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import api from '@/api/index.js'

export default {
    name: 'hospitalreg',

    data() {
        return {
            termsRead: false,
            termsAccepted: false,
            showTermsModal: false,
            loading: false,
            error: null,
            success: null,

            form: {
                hospital_name: '',
                license_id: '',
                contact: '',
                partner_type: '',
                email: '',
                address: '',
                city: '',
                state: '',
                facility: '',
                convenience_fee: 0,
                fee_description: '',
                password: ''
            }
        }
    },

    methods: {
      handlePhone() {
  let val = this.form.contact.replace(/\D/g, '')
  this.form.contact = val.slice(0, 10)
},

             handleCity(field) {
  this.form[field] = this.form[field]
    .replace(/[^A-Za-z\s]/g, '')
    .replace(/\s{2,}/g, ' ')
    .slice(0, 50)
},
        async handleRegister() {
            if (!this.termsAccepted) {
                this.error = 'Please accept Partner Terms first.'
                return
            }
            if (!/^[6-9]\d{9}$/.test(this.form.contact)) {
            this.error = "Invalid contact number"
             return
             }

             //email
             const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
          if (!emailRegex.test(this.form.email)) {
            this.error = "Invalid email address"
            return
            }
            // facility type
            if (!this.form.partner_type) {
  this.error = "Please select facility type"
  return
}

            const pw = this.form.password
            if (pw.length < 8) {
                this.error = 'Password must be at least 8 characters.'
                return
            }
            if (!/[a-zA-Z]/.test(pw) || !/[0-9]/.test(pw)) {
                this.error = 'Password must be alpha-numeric.'
                return
            }

            this.loading = true
            this.error = null

            try {
                 await api.post('https://jeevandaan-yaal.onrender.com/api/partners/register/', this.form)

                

                this.success = 'Facility registered! Waiting for admin verification...'

                

            } catch (error) {
                if (error.response && error.response.data) {
                    const errors = error.response.data
                    const firstError = Object.values(errors)[0]
                    this.error = Array.isArray(firstError) ? firstError[0] : firstError
                } else {
                    this.error = 'Something went wrong. Please try again.'
                }
            } finally {
                this.loading = false
            }
        },

        openTermsModal() {
            this.showTermsModal = true
        },

        closeTermsModal() {
            this.showTermsModal = false
        },

        acceptTerms() {
            this.termsRead = true
            this.termsAccepted = true
            this.showTermsModal = false
        },

        togglePassword(inputId, iconEl) {
            const input = document.getElementById(inputId)
            if (input.type === 'password') {
                input.type = 'text'
                iconEl.classList.replace('fa-eye', 'fa-eye-slash')
            } else {
                input.type = 'password'
                iconEl.classList.replace('fa-eye-slash', 'fa-eye')
            }
        }
    },

    mounted() {
        document.body.classList.add('Hospital-reg')

        const hPw = document.getElementById('hosp-pw')
        const hChar = document.getElementById('hChar')
        const hAlpha = document.getElementById('hAlpha')

        hPw.addEventListener('input', () => {
            const v = hPw.value
            v.length >= 8 ? hChar.classList.add('active') : hChar.classList.remove('active')
            ;(/[a-zA-Z]/.test(v) && /[0-9]/.test(v)) ? hAlpha.classList.add('active') : hAlpha.classList.remove('active')
        })
    },

    unmounted() {
        document.body.classList.remove('Hospital-reg')
    }
}
</script>

<style>
  body.Hospital-reg {
    background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 50%, #d1e7ff 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 30px 0;
    font-family: 'Segoe UI', sans-serif;
  }
</style>

<style scoped>
  :root {
    --hosp-blue: #0d6efd;
    --light-blue: #e7f1ff;
    --success-green: #198754;
  }

  .main-card {
    background: white;
    border-radius: 30px;
    box-shadow: 0 20px 60px rgba(13, 110, 253, 0.15);
    overflow: hidden;
    max-width: 1150px;
    width: 95%;
    border: none;
  }

  .illustration-side {
    background-color: #f8fbff;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
  }

  .login-side { padding: 40px 60px; }

  .brand-logo {
    color: var(--hosp-blue);
    font-weight: 800;
    font-size: 1.5rem;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .input-group-custom {
    background: #f1f3f5;
    border-radius: 12px;
    padding: 10px 18px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    border: 1px solid transparent;
    position: relative;
  }

  .input-group-custom:focus-within {
    background: #fff;
    border-color: #b6d4fe;
  }

  .input-group-custom input,
  .input-group-custom select {
    border: none;
    background: transparent;
    width: 100%;
    margin-left: 12px;
    outline: none;
    color: #495057;
  }

  .toggle-eye {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    color: #6c757d;
    transition: color 0.2s;
  }

  .toggle-eye:hover { color: #333; }

  .restriction-text {
    font-size: 0.75rem;
    margin-top: -10px;
    margin-bottom: 15px;
    display: flex;
    gap: 15px;
  }

  .req { color: #999; }
  .req.active { color: #198754; font-weight: bold; }

  .btn-hospital {
    background-color: #0d6efd;
    border: none;
    border-radius: 50px;
    padding: 12px;
    font-weight: 600;
    color: white;
    width: 100%;
    transition: 0.3s;
  }

  .btn-hospital:hover { opacity: 0.9; transform: translateY(-2px); }

  .btn-hospital:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  /* Vue Modal */
  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
  }

  .modal-box {
    background: white;
    border-radius: 20px;
    width: 90%;
    max-width: 450px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  }

  .modal-box-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px 10px;
  }

  .modal-box-body { padding: 10px 24px; }
  .modal-box-footer { padding: 10px 24px 20px; }

  @media (max-width: 768px) {
    .illustration-side { display: none; }
    .login-side { padding: 30px 20px; }
  }
</style>