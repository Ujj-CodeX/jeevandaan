<template>
    <div class="card main-card">
    <div class="row g-0">
        <div class="col-md-5 illustration-side d-none d-md-flex">
            <img src="https://img.freepik.com/free-vector/hospital-building-concept-illustration_114360-8440.jpg" alt="Login" style="width: 100%;">
        </div>
        <div class="col-md-7 login-side">
            <h3 class="fw-bold text-primary mb-1">Hospital Portal</h3>
            <p class="text-muted small mb-4">Secure access for medical administrators.</p>
            <form>
                <div class="input-group-custom">
                    <i class="fa-solid fa-hashtag text-muted"></i>
                    <input type="text" placeholder="Hospital License ID" required>
                </div>
                <div class="input-group-custom">
                    <i class="fa-solid fa-lock text-muted"></i>
                    <input type="password" placeholder="Admin Password" required>
                </div>
                <button type="submit" class="btn-hospital mt-3">Portal Login</button>
                <p class="text-center mt-3 text-muted small">Facility not on-boarded? <a href="#" class="text-primary fw-bold text-decoration-none">Apply Now</a></p>
            </form>
        </div>
    </div>
</div>
    
</template>
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
        .illustration-side { background: #f0f7ff; display: flex; align-items: center; justify-content: center; padding: 40px; }
        .login-side { padding: 50px; }
        .input-group-custom {
            background: #f1f3f5;
            border-radius: 12px;
            padding: 12px 18px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .input-group-custom input { border: none; background: transparent; width: 100%; margin-left: 12px; outline: none; }
        .btn-hospital { background: #0d6efd; color: white; border: none; border-radius: 50px; padding: 12px; width: 100%; font-weight: 600; }
    </style>
    <script>
        export default {
        name : 'hospital_login',
    mounted(){ 
        document.body.classList.add('Hospital-login');

    },
    unmounted(){
        document.body.classList.remove('Hospital-login');
    }
}
    </script>