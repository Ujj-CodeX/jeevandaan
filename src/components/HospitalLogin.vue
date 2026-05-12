<template>
    <div class="card main-card">
        <div class="row g-0">
            <div class="col-md-5 illustration-side d-none d-md-flex">
                <img src="https://img.freepik.com/free-vector/hospital-building-concept-illustration_114360-8440.jpg" alt="Login" style="width: 100%;">
            </div>
            <div class="col-md-7 login-side">
                <h3 class="fw-bold text-primary mb-1">Partners Portal</h3>
                <p class="text-muted small mb-4">Secure access for medical administrators.</p>

                <form @submit.prevent="handleLogin">
                    <div class="input-group-custom">
                        <i class="fa-solid fa-hashtag text-muted"></i>
                        <input
                            type="text"
                            v-model="form.license_id"
                            placeholder="Hospital License ID"
                            required
                        >
                    </div>

                    <div class="input-group-custom" style="position: relative;">
                        <i class="fa-solid fa-lock text-muted"></i>
                        <input
                            type="password"
                            v-model="form.password"
                            id="partner-pw"
                            placeholder="Admin Password"
                            required
                        >
                        <i class="fa-solid fa-eye toggle-eye"
                           @click="togglePassword('partner-pw', $event.target)">
                        </i>
                    </div>

                    <!-- Error -->
                    <div v-if="error" class="alert-custom error mt-2">
                        <i class="fa-solid fa-circle-exclamation"></i> {{ error }}
                    </div>

                    <!-- Success -->
                    <div v-if="success" class="alert-custom success mt-2">
                        <i class="fa-solid fa-circle-check"></i> {{ success }}
                    </div>

                    <button type="submit" class="btn-hospital mt-3" :disabled="loading">
                        <span v-if="loading">Logging in...</span>
                        <span v-else>Portal Login</span>
                    </button>

                    <p class="text-center mt-3 text-muted small">
                        Facility not on-boarded?
                        <router-link to="/partnersreg" class="text-primary fw-bold text-decoration-none">
                            Apply Now
                        </router-link>
                    </p>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import api from '@/api/index.js'

export default {
    name: 'hospital_login',

    data() {
        return {
            form: {
                license_id: '',
                password: ''
            },
            loading: false,
            error: null,
            success: null
        }
    },

    methods: {
        async handleLogin() {
            this.loading = true
            this.error = null

            try {
                const response = await api.post('https://api.jeevandaan.online/api/partners/login/', this.form)

                // Store tokens
                localStorage.setItem('access_token', response.data.tokens.access)
                localStorage.setItem('refresh_token', response.data.tokens.refresh)
                localStorage.setItem('user_type', 'partner')

                // Store partner info
                localStorage.setItem('partner', JSON.stringify(response.data.partner))

                this.success = 'Login successful! Redirecting...'

                setTimeout(() => {
                    this.$router.push('/partnersdash')
                }, 1000)

            } catch (error) {
                if (error.response && error.response.data) {
                    this.error = error.response.data.error || 'Login failed.'
                } else {
                    this.error = 'Something went wrong. Please try again.'
                }
            } finally {
                this.loading = false
            }
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
        document.body.classList.add('Hospital-login')
    },

    unmounted() {
        document.body.classList.remove('Hospital-login')
    }
}
</script>

<style>
body.Hospital-login {
    background: linear-gradient(135deg, #ffffff 0%, #eef6ff 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Segoe UI', sans-serif;
}
</style>

<style scoped>
.main-card {
    background: white;
    border-radius: 30px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.1);
    overflow: hidden;
    max-width: 900px;
    width: 95%;
    border: none;
}

.illustration-side {
    background: #f0f7ff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
}

.login-side { padding: 50px; }

.input-group-custom {
    background: #f1f3f5;
    border-radius: 12px;
    padding: 12px 18px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    position: relative;
}

.input-group-custom input {
    border: none;
    background: transparent;
    width: 100%;
    margin-left: 12px;
    outline: none;
}

.toggle-eye {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    color: #6c757d;
}

.toggle-eye:hover { color: #333; }

.btn-hospital {
    background: #0d6efd;
    color: white;
    border: none;
    border-radius: 50px;
    padding: 12px;
    width: 100%;
    font-weight: 600;
    transition: 0.3s;
}

.btn-hospital:hover { opacity: 0.9; transform: translateY(-2px); }

.btn-hospital:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

.alert-custom {
    padding: 10px 15px;
    border-radius: 10px;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
}

.alert-custom.error {
    background: #fff2f2;
    color: #e74c3c;
    border: 1px solid #ffcccc;
}

.alert-custom.success {
    background: #f0fff4;
    color: #198754;
    border: 1px solid #b7f5c8;
}

@media (max-width: 768px) {
    .illustration-side { display: none; }
    .login-side { padding: 30px 20px; }
}
</style>