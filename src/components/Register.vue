<template>
  <div>
    <div class="card main-card">
      <div class="row g-0">
        <div class="col-md-5 illustration-side d-none d-md-flex text-center">
          <img src="https://img.freepik.com/free-vector/blood-donation-concept-illustration_114360-5029.jpg" alt="Tracking" style="width: 85%;">
          <h5 class="mt-4 fw-bold">Live Health Tracking</h5>
          <p class="text-muted small px-4">Register to connect with nearby blood donors and emergency organ requests instantly.</p>
        </div>

        <div class="col-md-7 login-side">
          <div class="brand-logo">
            <img 
    src="@/assets/L1.png" 
    alt="JeevanDaan Logo" 
    width="32" 
    height="32" 
    class="me-2 d-inline-block align-top logo-icon"
  > JeevanDaan+
          </div>
          <h2 class="fw-bold">Create Account</h2>
          <p class="text-muted small mb-4">Be a part of India's fastest growing digital life-saving network.</p>

          <form id="regForm" @submit.prevent="handleRegister">
            <div class="row">
    <div class="col-md-6">
        <div class="input-group-custom">
            <i class="fa-regular fa-user text-muted"></i>
            <input type="text" v-model="form.name" placeholder="Full Name" required>
        </div>
    </div>
    <div class="col-md-6">
        <div class="input-group-custom">
            <i class="fa-solid fa-at text-muted"></i>
            <input type="text" v-model="form.username" placeholder="Username" required>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6">
        <div class="input-group-custom">
            <i class="fa-solid fa-phone text-muted"></i>
            <input type="tel" v-model="form.phone_number" placeholder="Mobile Number" required>
        </div>
    </div>
    <div class="col-md-6">
        <div class="input-group-custom">
            <i class="fa-solid fa-droplet text-danger"></i>
            <select v-model="form.blood_group" required>
                <option selected disabled value="">Blood Group</option>
                <option>A+</option><option>A-</option>
                <option>B+</option><option>B-</option>
                <option>O+</option><option>O-</option>
                <option>AB+</option><option>AB-</option>
            </select>
        </div>
    </div>
</div>

<div class="input-group-custom">
    <i class="fa-regular fa-envelope text-muted"></i>
    <input type="email" v-model="form.email" placeholder="Email Address" required>
</div>

<div class="input-group-custom">
    <i class="fa-solid fa-location-dot text-muted"></i>
    <input type="text" v-model="form.address" placeholder="City / Address" required>
</div>

<div class="input-group-custom mb-2" style="position: relative;">
    <i class="fa-solid fa-lock text-muted"></i>
    <input type="password" v-model="form.password" id="pw" placeholder="Create Password" required>
    <i class="fa-solid fa-eye toggle-eye" @click="togglePassword('pw', $event.target)"></i>
</div>

            <div class="restriction-text">
              <span id="charCount" class="req"><i class="fa-solid fa-circle-check"></i> 8+ Characters</span>
              <span id="alphaNum" class="req"><i class="fa-solid fa-circle-check"></i> Alpha-numeric</span>
            </div>

            <div class="form-check mb-4">
              <input class="form-check-input" type="checkbox" id="termsCheck"
                :disabled="!termsRead"
                v-model="termsAccepted">
              <label class="form-check-label text-muted small" for="termsCheck">
                I agree to the
                <a href="#" @click.prevent="openTermsModal" class="text-danger fw-bold text-decoration-none">
                  Terms & Conditions
                </a>
              </label>
            </div>

            <div v-if="error" class="alert-custom error">
    <i class="fa-solid fa-circle-exclamation"></i> {{ error }}
</div>

<!-- Success message -->
<div v-if="success" class="alert-custom success">
    <i class="fa-solid fa-circle-check"></i> {{ success }}
</div>

            <button type="submit" class="btn-register" :disabled="!termsAccepted">Register Now</button>
            <p class="text-center mt-3 text-muted small">Already a member?
              <a href="#" class="text-primary fw-bold text-decoration-none">Login</a>
            </p>
          </form>
        </div>
      </div>
    </div>

    
    <div v-if="showTermsModal" class="modal-overlay" @click.self="closeTermsModal">
      <div class="modal-box">
        <div class="modal-box-header">
          <h5 class="fw-bold mb-0">Terms & Conditions</h5>
          <button class="btn-close" @click="closeTermsModal"></button>
        </div>
        <div class="modal-box-body text-muted small">
          <p>Welcome to <b>JeevanDaan+</b>. By checking the box, you agree to:</p>
          <ul>
            <li>Provide accurate health and blood group details.</li>
            <li>Allow the app to access your location for emergency donation requests.</li>
            <li>Not use the platform for commercial selling of blood or organs.</li>
            <li>Your data will be encrypted and used only for health connectivity.</li>
          </ul>
        </div>
        <div class="modal-box-footer">
          <button class="btn btn-danger w-100 rounded-pill" @click="acceptTerms">
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
    name: 'register',

    data() {
        return {
            termsRead: false,
            termsAccepted: false,
            showTermsModal: false,
            loading: false,
            error: null,
            success: null,

            form: {
                name: '',
                username: '',
                phone_number: '',
                blood_group: '',
                email: '',
                address: '',
                password: '',
            }
        }
    },

    methods: {
        async handleRegister() {
            // Validate terms
            if (!this.termsAccepted) {
                this.error = 'Please accept Terms & Conditions first.'
                return
            }

            // Validate password
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
                const response = await api.post('/api/users/register/', this.form)

                // Store tokens
                localStorage.setItem('access_token', response.data.tokens.access)
                localStorage.setItem('refresh_token', response.data.tokens.refresh)
                localStorage.setItem('user_type', 'donor')

                this.success = 'Account created successfully! Redirecting...'

                // Redirect to dashboard after 1.5 seconds
                setTimeout(() => {
                    this.$router.push('/dashboard')
                }, 1500)

            } catch (error) {
                if (error.response && error.response.data) {
                    // Show backend validation errors
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
        document.body.classList.add('register-page')

        const pwInput = document.getElementById('pw')
        const charCount = document.getElementById('charCount')
        const alphaNum = document.getElementById('alphaNum')

        pwInput.addEventListener('input', () => {
            const val = pwInput.value
            if (val.length >= 8) charCount.classList.add('active')
            else charCount.classList.remove('active')
            if (/[a-zA-Z]/.test(val) && /[0-9]/.test(val)) alphaNum.classList.add('active')
            else alphaNum.classList.remove('active')
        })
    },

    unmounted() {
        document.body.classList.remove('register-page')
    }
}
</script>

<style>
  :root {
    --primary-red: #ff5252;
    --btn-blue: #3897f0;
    --valid-green: #2ecc71;
  }

  .alert-custom {
    padding: 10px 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.alert-custom.error {
    background: #fff2f2;
    color: #e74c3c;
    border: 1px solid #ffcccc;
}

.alert-custom.success {
    background: #f0fff4;
    color: #2ecc71;
    border: 1px solid #b7f5c8;
}


  body.register-page {
    background: linear-gradient(135deg, #ffffff 0%, #fff2f2 50%, #ffdce0 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px 0;
    font-family: 'Segoe UI', sans-serif;
  }

  .main-card {
    background: white;
    border-radius: 30px;
    box-shadow: 0 20px 60px rgba(255, 82, 82, 0.15);
    overflow: hidden;
    max-width: 1100px;
    width: 95%;
    border: none;
  }

  .illustration-side {
    background-color: #fafbfc;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
  }

  .login-side { padding: 40px 50px; }

  .brand-logo {
    color: var(--primary-red);
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
    border-color: #ffcccc;
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
    padding-left: 5px;
  }

  .req { color: #999; transition: 0.3s; }
  .req.active { color: var(--valid-green); font-weight: bold; }

  .btn-register {
    background-color: var(--btn-blue);
    border: none;
    border-radius: 50px;
    padding: 12px;
    font-weight: 600;
    color: white;
    width: 100%;
    transition: 0.3s;
  }

  .btn-register:hover { opacity: 0.9; transform: translateY(-2px); }

  .btn-register:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  /* ✅ Vue Modal Styles */
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