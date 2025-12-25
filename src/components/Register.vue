<template>
<div class="card main-card">
    <div class="row g-0">
        <div class="col-md-5 illustration-side d-none d-md-flex text-center">
            <img src="https://img.freepik.com/free-vector/blood-donation-concept-illustration_114360-5029.jpg" alt="Tracking" style="width: 85%;">
            <h5 class="mt-4 fw-bold">Live Health Tracking</h5>
            <p class="text-muted small px-4">Register to connect with nearby blood donors and emergency organ requests instantly.</p>
        </div>

        <div class="col-md-7 login-side">
            <div class="brand-logo">
                <i class="fa-solid fa-heart-pulse"></i> JeevanDaan+
            </div>
            <h2 class="fw-bold">Create Account</h2>
            <p class="text-muted small mb-4">Be a part of India's fastest growing digital life-saving network.</p>

            <form id="regForm">
                <div class="row">
                    <div class="col-md-6">
                        <div class="input-group-custom">
                            <i class="fa-regular fa-user text-muted"></i>
                            <input type="text" placeholder="Full Name" required>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="input-group-custom">
                            <i class="fa-solid fa-at text-muted"></i>
                            <input type="text" placeholder="Username" required>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6">
                        <div class="input-group-custom">
                            <i class="fa-solid fa-phone text-muted"></i>
                            <input type="tel" placeholder="Mobile Number" required>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="input-group-custom">
                            <i class="fa-solid fa-droplet text-danger"></i>
                            <select required>
                                <option selected disabled>Blood Group</option>
                                <option>A+</option><option>A-</option><option>B+</option><option>B-</option>
                                <option>O+</option><option>O-</option><option>AB+</option><option>AB-</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="input-group-custom">
                    <i class="fa-regular fa-envelope text-muted"></i>
                    <input type="email" placeholder="Email Address" required>
                </div>

                <div class="input-group-custom mb-2">
                    <i class="fa-solid fa-lock text-muted"></i>
                    <input type="password" id="pw" placeholder="Create Password" required>
                </div>

                <div class="restriction-text">
                    <span id="charCount" class="req"><i class="fa-solid fa-circle-check"></i> 8+ Characters</span>
                    <span id="alphaNum" class="req"><i class="fa-solid fa-circle-check"></i> Alpha-numeric</span>
                </div>

                <div class="form-check mb-4">
                    <input class="form-check-input" type="checkbox" id="termsCheck" required>
                    <label class="form-check-label text-muted small" for="termsCheck">
                        I agree to the <a href="#" data-bs-toggle="modal" data-bs-target="#termsModal" class="text-danger fw-bold text-decoration-none">Terms & Conditions</a>
                    </label>
                </div>

                <button type="submit" class="btn-register">Register Now</button>
                <p class="text-center mt-3 text-muted small">Already a member? <a href="#" class="text-primary fw-bold text-decoration-none">Login</a></p>
            </form>
        </div>
    </div>
</div>

<div class="modal fade" id="termsModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow" style="border-radius: 20px;">
            <div class="modal-header border-0 pb-0">
                <h5 class="modal-title fw-bold">Terms & Conditions</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body text-muted small">
                <p>Welcome to <b>JeevanDaan+</b>. By checking the box, you agree to:</p>
                <ul>
                    <li>Provide accurate health and blood group details.</li>
                    <li>Allow the app to access your location for emergency donation requests.</li>
                    <li>Not use the platform for commercial selling of blood or organs.</li>
                    <li>Your data will be encrypted and used only for health connectivity.</li>
                </ul>
            </div>
            <div class="modal-footer border-0 pt-0">
                <button type="button" class="btn btn-danger w-100 rounded-pill" data-bs-dismiss="modal">I Understand</button>
            </div>
        </div>
    </div>
</div>

</template>
<script>
    export default {
  name: 'register',

  mounted() {
    
    document.body.classList.add('register-page')
      // Real-time Password Validation
    const pwInput = document.getElementById('pw');
    const charCount = document.getElementById('charCount');
    const alphaNum = document.getElementById('alphaNum');

    pwInput.addEventListener('input', () => {
        const val = pwInput.value;
        
        // Check Length
        if(val.length >= 8) charCount.classList.add('active');
        else charCount.classList.remove('active');

        // Check Alpha-numeric (has letter AND number)
        if(/[a-zA-Z]/.test(val) && /[0-9]/.test(val)) alphaNum.classList.add('active');
        else alphaNum.classList.remove('active');
    });
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
        }

        .input-group-custom:focus-within {
            background: #fff;
            border-color: #ffcccc;
        }

        .input-group-custom input, .input-group-custom select {
            border: none;
            background: transparent;
            width: 100%;
            margin-left: 12px;
            outline: none;
            color: #495057;
        }

        /* Password Restriction Styling */
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

        @media (max-width: 768px) {
            .illustration-side { display: none; }
            .login-side { padding: 30px 20px; }
        }
    </style>