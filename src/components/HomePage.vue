<template>
<nav class="navbar navbar-expand-lg bg-white shadow-sm sticky-top">
    <div class="container-fluid">
        <a class="navbar-brand" href="#" style="color:#e53935; font-weight: bold;">
            JeevanDaan+
        </a>
        <button class="btn btn-link d-lg-none p-0" type="button" onclick="toggleSidebar()">
            <i class="fas fa-bars fa-2x text-muted"></i>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="#">Home</a>
                </li>
            
                <li class="nav-item">
                    <router-link class="nav-link" to="/hospital_login">Hospital Login</router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/register">Register Now</router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/login">Login</router-link>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Learn More</a>
                </li>
            </ul>
            <div class="d-flex align-items-center">
                <button class="btn btn-outline-danger me-2">Search hospitals</button>
                <i class="fas fa-search fa-lg me-2 text-muted"></i>
                <i class="fas fa-arrow-right-long fa-lg text-muted"></i>
            </div>
        </div>
    </div>
</nav>

<!-- Sidebar -->
<div class="sidebar" id="sidebar">
    <div class="sidebar-header d-flex justify-content-between align-items-center">
        <a class="navbar-brand" href="#" style="color: #e53935; font-weight: bold;">
            JeevanDaan+
        </a>
        <button class="btn btn-link p-0" onclick="toggleSidebar()">
            <i class="fas fa-times fa-2x text-muted"></i>
        </button>
    </div>
    <div class="sidebar-body mt-4">
        <ul class="nav flex-column">
            <li class="nav-item">
                <a class="nav-link" href="#">
                    <button class="btn btn-outline-danger">Search hospitals</button>
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link active" href="#">Home</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Make a Request</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Become a Donor</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Register Now</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">View Donor Dashboard</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Learn More</a>
            </li>
        </ul>
    </div>
</div>

<div class="overlay" id="overlay" onclick="toggleSidebar()"></div>

<!-- Header Section -->
<div class="header-content pt-5 pb-5 ">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12 text-center">
                <div class="p-3">
                    <h1 class="display-4 fw-bold">JeevanDaan+</h1>
                    <p class="lead">A life-saving act. A seamless connection. Your single action can save multiple patients. Donate blood, plasma, or organs today!</p>
                    <div class="d-grid gap-2 d-sm-flex justify-content-sm-center justify-content-lg-center">
                        <button type="button" class="btn btn-light rounded-pill px-4 py-2 me-sm-2 mb-2 mb-sm-0"  >Become a Donor</button>
                        <button type="button" class="btn btn-outline-light rounded-pill px-4 py-2">Request Help</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Why Join Section -->
<section class="section-why py-5">
    <div class="container">
        <div class="text-center">
            <h2 class="display-6 mb-3">Why Join Jeevandaan+?</h2>
            <p class="text-muted mb-5">We help you find a perfect match and make a difference. Our platform is a life-changing mission, saving lives since 2012.</p>
        </div>
        <div class="row text-center g-4">
            <!-- Donors Card -->
            <div class="col-md-4">
                <div class="feature-card bg-white p-4 h-100 d-flex flex-column justify-content-between">
                    <div class="flex-grow-1">
                        <i class="fas fa-heartbeat feature-icon mb-3"></i>
                        <h3 class="h5 fw-bold text-dark">Donors</h3>
                        <p class="text-muted">Seamlessly apply or donate blood, plasma, or organs. It is an act of empathy and compassion that will make a difference.</p>
                    </div>
                    <div>
                        <a href="#" class="btn btn-sm btn-outline-danger rounded-pill mt-3">Learn More</a>
                    </div>
                </div>
            </div>
            <!-- Hospitals Card -->
            <div class="col-md-4">
                <div class="feature-card bg-white p-4 h-100 d-flex flex-column justify-content-between">
                    <div class="flex-grow-1">
                        <i class="fas fa-hospital-user feature-icon mb-3"></i>
                        <h3 class="h5 fw-bold text-dark">Hospitals</h3>
                        <p class="text-muted">Streamline patient-donor matching and improve efficiency with our easy-to-use intuitive platform.</p>
                    </div>
                    <div>
                        <a href="#" class="btn btn-sm btn-outline-danger rounded-pill mt-3">Learn More</a>
                    </div>
                </div>
            </div>
            <!-- Recipients Card -->
            <div class="col-md-4">
                <div class="feature-card bg-white p-4 h-100 d-flex flex-column justify-content-between">
                    <div class="flex-grow-1">
                        <i class="fas fa-users-line feature-icon mb-3"></i>
                        <h3 class="h5 fw-bold text-dark">Recipients</h3>
                        <p class="text-muted">Quickly find donors with a perfect match for blood, plasma, or organ needs. Our dedicated team is here to support you.</p>
                    </div>
                    <div>
                        <a href="#" class="btn btn-sm btn-outline-danger rounded-pill mt-3">Learn More</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- How it Works Section -->
<section class="section-works py-5">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-6 mb-3">How it Works</h2>
        </div>
        <div class="row justify-content-center g-4">
            <!-- Real time matching Card -->
            <div class="col-md-8">
                <div class="card p-4">
                    <div class="d-flex align-items-center mb-3">
                        <i class="fas fa-clock fa-2x text-danger me-3"></i>
                        <h3 class="h5 mb-0 fw-bold">Real time matching</h3>
                    </div>
                    <p class="text-muted">Connect with donors and hospitals in real-time. Our matching algorithm connects you based on location, blood group, and other key data.</p>
                </div>
            </div>
            <!-- Location Based Search Card -->
            <div class="col-md-8">
                <div class="card p-4">
                    <div class="d-flex align-items-center mb-3">
                        <i class="fas fa-map-marker-alt fa-2x text-danger me-3"></i>
                        <h3 class="h5 mb-0 fw-bold">Location Based Search</h3>
                    </div>
                    <p class="text-muted">Find nearby donors and hospitals with our location-based matching API. Get a clearer picture of who is available to help you.</p>
                </div>
            </div>
            <!-- Actionable Analytics Card -->
            <div class="col-md-8">
                <div class="card p-4">
                    <div class="d-flex align-items-center mb-3">
                        <i class="fas fa-chart-line fa-2x text-danger me-3"></i>
                        <h3 class="h5 mb-0 fw-bold">Actionable Analytics</h3>
                    </div>
                    <p class="text-muted">Leverage real-time data to make informed decisions. Our dashboard provides detailed insights into donor-recipient availability, and regional needs.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Our Impact Section -->
<section class="section-impact py-5">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-6 mb-3">Our Impact by numbers</h2>
            <p class="text-muted">Every day, we're changing lives. Our numbers tell our story of hope and compassion.</p>
        </div>
        <div class="row text-center g-4 justify-content-center">
            <div class="col-sm-6 col-lg-3">
                <div class="stats-card p-4">
                    <h3 class="display-5 fw-bold text-danger">3,450+</h3>
                    <p class="text-muted">Successful Requests</p>
                </div>
            </div>
            <div class="col-sm-6 col-lg-3">
                <div class="stats-card p-4">
                    <h3 class="display-5 fw-bold text-primary">1,200+</h3>
                    <p class="text-muted">Successful Donors</p>
                </div>
            </div>
            <div class="col-sm-6 col-lg-3">
                <div class="stats-card p-4">
                    <h3 class="display-5 fw-bold text-success">50+</h3>
                    <p class="text-muted">Partner Hospitals</p>
                </div>
            </div>
            <div class="col-sm-6 col-lg-3">
                <div class="stats-card p-4">
                    <h3 class="display-5 fw-bold text-warning">95%</h3>
                    <p class="text-muted">Request Success Rate</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- What Our Community Says Section -->
<section class="section-people py-5">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-6 mb-3">What Our Community Says</h2>
            <p class="text-muted">Read stories of hope and courage from people who have been helped by JeevanDaan+</p>
        </div>
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card p-4 shadow-sm border-0">
                    <div class="d-flex align-items-center mb-3">
                        <img src="https://placehold.co/60x60/e53935/ffffff?text=SJ" class="rounded-circle me-3" alt="Sanjay A.">
                        <div>
                            <h4 class="h6 mb-0 fw-bold">Sanjay A.</h4>
                            <p class="text-muted small mb-0">Patient's relative</p>
                        </div>
                    </div>
                    <p class="text-muted fst-italic">"I was in a desperate situation. Thanks to JeevanDaan+ I found a donor in a few hours and my patient is a lot better."</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA Section -->
<section class="section-cta py-5">
    <div class="container text-center">
        <h2 class="display-6 fw-bold mb-3">Your Act of Kindness Can Change the World!</h2>
        <p class="lead mb-4">Join the community of donors. Be a bridge of hope, one donation at a time.</p>
        <button class="btn btn-light rounded-pill px-5 py-3 fw-bold">Become a Donor Now</button>
    </div>
</section>


</template>

<script >
  export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}

    
</script>


<style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f7f9fc;
            overflow-x: hidden;
        }

        .navbar-brand img {
            height: 40px;
        }

        /* Sidebar Styling */
        .sidebar {
            position: fixed;
            top: 0;
            left: -300px;
            width: 250px;
            height: 100%;
            background-color: #fff;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            transition: left 0.3s ease;
            z-index: 1050;
        }

        .sidebar.show {
            left: 0;
        }

        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease;
            z-index: 1040;
        }

        .overlay.show {
            opacity: 1;
            visibility: visible;
        }

        .sidebar-header {
            background-color: #fff;
            padding: 20px;
            border-bottom: 1px solid #eee;
        }

        .sidebar .nav-link {
            padding: 1rem 1.5rem;
            color: #333;
            font-weight: 500;
        }

        .sidebar .nav-link.active,
        .sidebar .nav-link:hover {
            color: #e53935;
            background-color: #fcebeb;
        }

        /* Header Content */
        .header-content {
            background-color: #e53935;
            color: white;
        }

        .header-content .btn {
            background-color: white;
            color: #e53935;
            font-weight: 600;
        }
        
        .header-content h1 {
            font-weight: 700;
        }
        
        /* Sections */
        .section-why {
            background-color: white;
        }

        .section-why h2, .section-works h2, .section-impact h2, .section-people h2 {
            color: #e53935;
            font-weight: 700;
        }

        .feature-card {
            border-radius: 1rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }

        .feature-icon {
            font-size: 2.5rem;
            color: #e53935;
        }
        
        .section-works .card {
            border: none;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            border-radius: 1rem;
        }
        
        .section-impact .stats-card {
            border-left: 5px solid #e53935;
            background-color: #fff;
            border-radius: 0.5rem;
        }
        
        .section-impact .stats-card:nth-child(2) { border-color: #007bff; }
        .section-impact .stats-card:nth-child(3) { border-color: #28a745; }
        .section-impact .stats-card:nth-child(4) { border-color: #ffc107; }

        .section-cta {
            background-color: #e53935;
            color: white;
        }
        
        /* Animation CSS */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Applying animations to sections */
        .navbar {
            animation: fadeInDown 0.8s ease-out forwards;
        }

        .header-content {
            animation: fadeInUp 0.8s ease-out forwards;
            animation-delay: 0.2s;
            opacity: 0; /* Initial state */
        }

        .section-why, .section-works, .section-impact, .section-people, .section-cta {
            animation: fadeInUp 1s ease-out forwards;
            opacity: 0;
        }
        
        .section-why { animation-delay: 0.4s; }
        .section-works { animation-delay: 0.6s; }
        .section-impact { animation-delay: 0.8s; }
        .section-people { animation-delay: 1s; }
        .section-cta { animation-delay: 1.2s; }
    </style>
