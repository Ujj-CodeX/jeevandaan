<template>
<div class="card main-card">
    <div class="brand-logo">
        <i class="fa-solid fa-droplet"></i> JeevanDaan+
    </div>
    
    <div class="row g-0">
        <div class="col-lg-6 col-md-6 illustration-side d-none d-md-flex">
            <img src="https://img.freepik.com/free-vector/blood-donation-concept-illustration_114360-5029.jpg" alt="Health Donation Illustration" style="width: 80%;">
        </div>

        <div class="col-lg-6 col-md-5 login-side">
            <h2 class="welcome-text">Welcome Back :)</h2>
            <p class="sub-text">Join the life-saving mission. Please login with your email address and password.</p>

            <form>
                <div class="input-box">
                    <i class="fa-regular fa-envelope text-muted"></i>
                    <input type="email" value="Justin@jeevandaan.io">
                    <i class="fa-solid fa-circle-check text-success"></i>
                </div>

                <div class="input-box">
                    <i class="fa-solid fa-lock text-muted"></i>
                    <input type="password" value="••••••••••••">
                </div>

                <div class="d-flex justify-content-between align-items-center mb-4 mt-2">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="rem" checked>
                        <label class="form-check-label text-muted small" for="rem">Remember Me</label>
                    </div>
                    <a href="#" class="text-muted small text-decoration-none">Forgot Password?</a>
                </div>

                <div class="d-flex gap-3 align-items-center mb-4">
                    <button type="submit" class="btn btn-primary btn-login">Login Now</button>
                    <a href="#" class="btn-create">Create Account</a>
                </div>

                <div class="text-muted small">Or you can join with</div>
                <div class="social-container">
                    <div class="social-icon-btn">
                        <svg class="google-svg" viewBox="0 0 24 24">
                            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
                            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.66l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                        </svg>
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
    export default {
  name: 'Login',

  mounted() {
    document.body.classList.add('login-page')
  },

  unmounted() {
    document.body.classList.remove('login-page')
  }
}

</script>
<style>
        :root {
            --primary-red: #d32f2f;
            --google-blue: #4285F4;
            --fb-blue: #1877F2;
            --twitter-blue: #1DA1F2;
        }
        body.login-page {
            background: linear-gradient(135deg, #ffffff 0%, #fff1f1 50%, #ffcdd2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
        }

        

        .main-card {
            background: white;
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.08);
            overflow: hidden;
            max-width: 1000px;
            width: 90%;
            border: none;
            margin: 0 auto;
        }

        .brand-logo {
            color: var(--primary-red);
            font-weight: 800;
            font-size: 1.4rem;
            padding: 35px 0 0 45px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .illustration-side {
            background-color: #fffafa;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .illustration-img {
            width: 90%;
            max-width: 430px; /* Prevent image from pushing login content */
            height: auto;
            object-fit: contain;
        }

        .login-side {
            padding: 45px 60px;
            min-width: 430px; 
            flex-shrink: 0;
        }

        .welcome-text {
            font-weight: 700;
            font-size: 2rem;
            color: #2d3436;
        }

        .sub-text {
            color: #636e72;
            font-size: 0.9rem;
            margin-bottom: 25px;
        }

        /* Input Styles matching your image */
        .input-box {
            background: #f1f3f5;
            border-radius: 12px;
            padding: 12px 18px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            border: 1px solid transparent;
        }

        .input-box:focus-within {
            border-color: #dee2e6;
            background: #fff;
        }

        .input-box input {
            border: none;
            background: transparent;
            width: 100%;
            margin-left: 12px;
            outline: none;
            color: #495057;
        }

        .btn-login {
            background-color: #3897f0;
            border: none;
            border-radius: 30px;
            padding: 10px 35px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(56, 151, 240, 0.3);
        }

        .btn-create {
            border: 1px solid #e9ecef;
            border-radius: 30px;
            padding: 10px 30px;
            color: #6c757d;
            text-decoration: none;
            font-weight: 500;
        }

        /* Social Icons */
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
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: transform 0.2s;
        }

        .social-icon-btn:hover {
            transform: scale(1.1);
        }

        .google-svg {
            width: 20px;
            height: 20px;
        }
    </style>