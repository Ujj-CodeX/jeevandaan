```vue
<template>
  <div class="card main-card">
    <div class="brand-logo">
      <img 
    src="@/assets/L1.png" 
    alt="JeevanDaan Logo" 
    width="32" 
    height="32" 
    class="me-2 d-inline-block align-top logo-icon"
  > JeevanDaan+
    </div>

    <div class="row g-0">
      <!-- Illustration -->
      <div class="col-lg-6 col-md-6 illustration-side d-none d-md-flex">
        <img
          src="https://img.freepik.com/free-vector/blood-donation-concept-illustration_114360-5029.jpg"
          alt="Health Donation Illustration"
          style="width: 80%;"
        />
      </div>

      <!-- Login -->
      <div class="col-lg-6 col-md-5 login-side">
        <h2 class="welcome-text">Welcome Back :)</h2>
        <p class="sub-text">
          Join the life-saving mission. Please login with your username and password.
        </p>

        <form @submit.prevent="handleLogin">
          <!-- Username -->
          <div class="input-box">
            <i class="fa-regular fa-user text-muted"></i>
            <input
              type="text"
              v-model="username"
              placeholder="Enter username"
              required
            />
          </div>

          <!-- Password -->
          <div class="input-box">
            <i class="fa-solid fa-lock text-muted"></i>
            <input
              type="password"
              v-model="password"
              placeholder="Enter password"
              required
            />
          </div>

          <!-- Error Message -->
          <p v-if="error" style="color:red; font-size: 14px;">
            {{ error }}
          </p>

          <!-- Options -->
          <!-- Add below password input -->
<div class="d-flex justify-content-between align-items-center mb-4 mt-2">
    <div class="form-check">
        <input class="form-check-input" type="checkbox"
            id="rem" v-model="rememberMe">
        <label class="form-check-label text-muted small" for="rem">
            Remember Me
        </label>
    </div>
    <a href="#" class="text-muted small text-decoration-none"
        @click.prevent="showForgotModal = true">
        Forgot Password?
    </a>
</div>

<!-- Forgot Password Modal -->
<div v-if="showForgotModal" class="modal-overlay"
    @click.self="showForgotModal = false">
    <div class="bg-white rounded-4 shadow-lg p-4"
        style="max-width:420px;width:95%">

        <h5 class="fw-bold mb-1">Reset Password</h5>
        <p class="text-muted small mb-4">
            Enter your email — we'll send an OTP to your registered phone.
        </p>

        <!-- Step 1 — Email -->
        <div v-if="forgotStep === 1">
            <div class="input-box mb-3">
                <i class="fa-regular fa-envelope text-muted"></i>
                <input type="email" v-model="forgotEmail"
                    placeholder="Registered email address">
            </div>

            <div v-if="forgotError"
                class="alert alert-danger border-0 rounded-4 small mb-3">
                {{ forgotError }}
            </div>

            <button class="btn btn-danger w-100 py-3 fw-bold rounded-4"
                @click="sendForgotOTP"
                :disabled="forgotLoading">
                <span v-if="forgotLoading">
                    <span class="spinner-border spinner-border-sm me-2"></span>
                </span>
                <span v-else>Send OTP</span>
            </button>
        </div>

        <!-- Step 2 — OTP + New Password -->
        <div v-if="forgotStep === 2">
            <div class="input-box mb-3">
                <i class="fas fa-key text-muted"></i>
                <input type="text" v-model="forgotOTP"
                    placeholder="Enter OTP from SMS" maxlength="6">
            </div>
            <div class="input-box mb-3">
                <i class="fas fa-lock text-muted"></i>
                <input type="password" v-model="forgotNewPassword"
                    placeholder="New Password">
            </div>

            <div v-if="forgotError"
                class="alert alert-danger border-0 rounded-4 small mb-3">
                {{ forgotError }}
            </div>
            <div v-if="forgotSuccess"
                class="alert alert-success border-0 rounded-4 small mb-3">
                {{ forgotSuccess }}
            </div>

            <button class="btn btn-danger w-100 py-3 fw-bold rounded-4"
                @click="resetPassword"
                :disabled="forgotLoading">
                <span v-if="forgotLoading">
                    <span class="spinner-border spinner-border-sm me-2"></span>
                </span>
                <span v-else>Reset Password</span>
            </button>
        </div>

        <button class="btn btn-link text-muted small w-100 mt-2"
            @click="showForgotModal = false">
            Cancel
        </button>
    </div>
</div>

          <!-- Buttons -->
          <div class="d-flex gap-3 align-items-center mb-4">
            <button type="submit" class="btn btn-primary btn-login" :disabled="loading">
              {{ loading ? 'Logging in...' : 'Login Now' }}
            </button>
            <router-link to="/register" class="btn-create">
              Create Account
            </router-link>
          </div>

          
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api/index.js';


export default {
  name: "Login",

  data() {
    return {
      username: "",
      password: "",
      loading: false,
      error: "",
      showForgotModal: false,
      forgotStep: 1,
      forgotEmail: '',
      forgotOTP: '',
      forgotNewPassword: '',
      forgotLoading: false,
      forgotError: null,
      forgotSuccess: null,
    };
  },

  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = "";

      try {
        const response = await api.post(
          "http://127.0.0.1:8000/api/users/login/",
          {
            username: this.username,
            password: this.password,
          }
        );

        
        localStorage.setItem("access_token", response.data.tokens.access);
        localStorage.setItem("refresh_token", response.data.tokens.refresh);

    
        localStorage.setItem("donor", JSON.stringify(response.data.donor));

        
        this.$router.push("/user");
      } catch (err) {
        this.error =
          err.response?.data?.error ||
          err.response?.data?.message ||
          "Login failed. Try again.";
      } finally {
        this.loading = false;
      }
    },
    async sendForgotOTP() {
    if (!this.forgotEmail) {
        this.forgotError = 'Email is required.'
        return
    }
    this.forgotLoading = true
    this.forgotError = null

    try {
        await api.post('http://127.0.0.1:8000/api/users/forgot-password/', {
            email: this.forgotEmail
        })
        this.forgotStep = 2
    } catch (err) {
        this.forgotError = err.response?.data?.error ||
            'Failed. Please try again.'
    } finally {
        this.forgotLoading = false
    }
},

async resetPassword() {
    if (!this.forgotOTP || !this.forgotNewPassword) {
        this.forgotError = 'OTP and new password are required.'
        return
    }

    this.forgotLoading = true
    this.forgotError = null

    try {
        await api.post('http://127.0.0.1:8000/api/users/reset-password/', {
            email: this.forgotEmail,
            otp: this.forgotOTP,
            new_password: this.forgotNewPassword
        })
        this.forgotSuccess = 'Password reset! Please login.  '
        setTimeout(() => {
            this.showForgotModal = false
            this.forgotStep = 1
        }, 2000)
    } catch (err) {
        this.forgotError = err.response?.data?.error ||
            'Reset failed. Please try again.'
    } finally {
        this.forgotLoading = false
    }
},

    
  },

  mounted() {
    document.body.classList.add("login-page");
  },

  unmounted() {
    document.body.classList.remove("login-page");
  },
};
</script>

<style>
.modal-overlay {
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
:root {
  --primary-red: #d32f2f;
}

body.login-page {
  background: linear-gradient(135deg, #ffffff 0%, #fff1f1 50%, #ffcdd2 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-card {
  background: white;
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  max-width: 1000px;
  width: 90%;
}

.brand-logo {
  color: var(--primary-red);
  font-weight: 800;
  font-size: 1.4rem;
  padding: 35px 0 0 45px;
}

.login-side {
  padding: 45px 60px;
}

.input-box {
  background: #f1f3f5;
  border-radius: 12px;
  padding: 12px 18px;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.input-box input {
  border: none;
  background: transparent;
  width: 100%;
  margin-left: 12px;
  outline: none;
}

.btn-login {
  background-color: #3897f0;
  border-radius: 30px;
  padding: 10px 35px;
  font-weight: 600;
}

.btn-create {
  border: 1px solid #e9ecef;
  border-radius: 30px;
  padding: 10px 30px;
  color: #6c757d;
  text-decoration: none;
}

.social-container {
  display: flex;
  gap: 20px;
  margin-top: 15px;
}

.social-icon-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}
</style>

