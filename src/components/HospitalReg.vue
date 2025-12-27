<template>
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

            <form>
                <div class="row">
                    <div class="col-md-6">
                        <div class="input-group-custom">
                            <i class="fa-solid fa-hospital text-muted"></i>
                            <input type="text" placeholder="Hospital Name" required>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="input-group-custom">
                            <i class="fa-solid fa-id-card text-muted"></i>
                            <input type="text" placeholder="Reg/License ID" required>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6">
                        <div class="input-group-custom">
                            <i class="fa-solid fa-phone-volume text-muted"></i>
                            <input type="tel" placeholder="Emergency Contact" required>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="input-group-custom">
                            <i class="fa-solid fa-layer-group text-muted"></i>
                            <select required>
                                <option selected disabled>Facility Type</option>
                                <option>Government</option>
                                <option>Private Multi-specialty</option>
                                <option>Blood Bank</option>
                                
                            </select>
                        </div>
                    </div>
                </div>

                <div class="input-group-custom">
                    <i class="fa-solid fa-envelope text-muted"></i>
                    <input type="email" placeholder="Official Email Address" required>
                </div>

                <div class="input-group-custom mb-2">
                    <i class="fa-solid fa-lock text-muted"></i>
                    <input type="password" id="hosp-pw" placeholder="Create Admin Password" required>
                </div>

                <div class="restriction-text">
                    <span id="hChar" class="req"><i class="fa-solid fa-circle-check"></i> 8+ Characters</span>
                    <span id="hAlpha" class="req"><i class="fa-solid fa-circle-check"></i> Alpha-numeric</span>
                </div>

                <div class="form-check mb-4">
                    <input class="form-check-input" type="checkbox" id="hTerms" required>
                    <label class="form-check-label text-muted small" for="hTerms">
                        We agree to the <a href="#" data-bs-toggle="modal" data-bs-target="#hospModal" class="text-primary fw-bold text-decoration-none">Partner Terms</a>
                    </label>
                </div>

                <button type="submit" class="btn-hospital">Register Facility</button>
                <p class="text-center mt-3 text-muted small">Already registered? <a href="#" class="text-primary fw-bold text-decoration-none">Partner Login</a></p>
            </form>
        </div>
    </div>
</div>

<div class="modal fade" id="hospModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow" style="border-radius: 20px;">
            <div class="modal-header border-0 pb-0">
                <h5 class="modal-title fw-bold">Partners Terms of Use</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body text-muted small">
                <p>1. Facilities must maintain real-time inventory updates for blood stocks.</p>
                <p>2. Emergency organ requests must follow national clinical protocols.</p>
                <p>3. Patient data shared via JeevanDaan+ must be handled under HIPAA/Digital Health standards.</p>
            </div>
        </div>
    </div>
</div>

</template>
<style>
    body.Hospital-reg {
            /* Blue Gradient with White mix as requested */
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
        }

        .input-group-custom:focus-within {
            background: #fff;
            border-color: #b6d4fe;
        }

        .input-group-custom input, .input-group-custom select {
            border: none;
            background: transparent;
            width: 100%;
            margin-left: 12px;
            outline: none;
            color: #495057;
        }

        .restriction-text {
            font-size: 0.75rem;
            margin-top: -10px;
            margin-bottom: 15px;
            display: flex;
            gap: 15px;
        }
        
        .req { color: #999; }
        .req.active { color: var(--success-green); font-weight: bold; }

        .btn-hospital {
            background-color: var(--hosp-blue);
            border: none;
            border-radius: 50px;
            padding: 12px;
            font-weight: 600;
            color: white;
            width: 100%;
        }

        @media (max-width: 768px) {
            .illustration-side { display: none; }
            .login-side { padding: 30px 20px; }
        }
    </style>
<script>
    export default {
        name : 'hospitalreg',
    mounted(){
        document.body.classList.add('Hospital-reg');
    const hPw = document.getElementById('hosp-pw');
    const hChar = document.getElementById('hChar');
    const hAlpha = document.getElementById('hAlpha');

    hPw.addEventListener('input', () => {
        const v = hPw.value;
        v.length >= 8 ? hChar.classList.add('active') : hChar.classList.remove('active');
        (/[a-zA-Z]/.test(v) && /[0-9]/.test(v)) ? hAlpha.classList.add('active') : hAlpha.classList.remove('active');
    })},
     unmounted() {
    document.body.classList.remove('Hospital-reg');
    }


    }
</script>