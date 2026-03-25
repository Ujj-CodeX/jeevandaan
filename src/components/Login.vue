```vue
<template>
  <div class="card main-card">
    <div class="brand-logo">
      <i class="fa-solid fa-droplet"></i> JeevanDaan+
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
          <div class="d-flex justify-content-between align-items-center mb-4 mt-2">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" id="rem" />
              <label class="form-check-label text-muted small" for="rem">
                Remember Me
              </label>
            </div>
            <a href="#" class="text-muted small text-decoration-none">
              Forgot Password?
            </a>
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

          <!-- Social Login -->
          <div class="text-muted small">Or you can join with</div>
          <div class="social-container">
            <div class="social-icon-btn" @click="handleGoogleLogin">
              <i class="fa-brands fa-google"></i>
            </div>
            <div class="social-icon-btn">
              <i class="fa-brands fa-facebook-f" style="color: #1877F2;"></i>
            </div>
            <div class="social-icon-btn">
              <i class="fa-brands fa-twitter" style="color: #1DA1F2;"></i>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",

  data() {
    return {
      username: "",
      password: "",
      loading: false,
      error: "",
    };
  },

  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = "";

      try {
        const response = await axios.post(
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

    // 🔐 Placeholder for Google login
    async handleGoogleLogin() {
      alert("Google login integration pending (connect with backend token)");
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

