<template>
    <nav class="top-navbar d-none d-lg-flex justify-content-between align-items-center sticky-top">
    <a class="navbar-brand fw-bold" href="#">JeevanDaan+</a>
    <ul class="nav">
        <li class="nav-item">
            <a class="nav-link text-dark" href="#">Home</a>
        </li>
        <li class="nav-item">
            <a class="nav-link text-dark" href="#">Raise a Request</a>
        </li>
        <li class="nav-item">
            <a class="nav-link text-dark" href="#">Log out</a>
        </li>
        <li class="nav-item">
            <a class="nav-link text-dark" href="#">Learn More</a>
        </li>
    </ul>
    <div class="d-flex align-items-center">
        <i class="fas fa-search me-3"></i>
        <i class="fa-solid fa-bell me-3"></i>
        <img src="https://placehold.co/40x40/2196F3/ffffff?text=H" alt="Hospital" class="user-profile-img">
    </div>
</nav>

<!-- Main Navbar for Mobile (with sidebar trigger) -->
<nav class="top-navbar d-flex d-lg-none justify-content-between align-items-center sticky-top">
    <a class="navbar-brand fw-bold" href="#">JeevanDaan+</a>
    <button class="btn btn-link p-0" @click="toggleSidebar()">
        <i class="fas fa-bars fa-2x text-muted"></i>
    </button>
</nav>

<!-- Sidebar -->
<div class="sidebar" id="sidebar">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h5 class="fw-bold text-dark mb-0">Menu</h5>
        <button class="btn btn-link p-0" @click="toggleSidebar()">
            <i class="fas fa-times fa-2x text-muted"></i>
        </button>
    </div>
    <ul class="nav flex-column">
        <li class="nav-item">
            <a class="nav-link active" href="#">
                <i class="fas fa-home me-2"></i> Dashboard
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="#">
                <i class="fas fa-hand-holding-medical me-2"></i> Raise a Request
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="#">
                <i class="fas fa-cog me-2"></i> Account Settings
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="#">
                <i class="fas fa-sign-out-alt me-2"></i> Log Out
            </a>
        </li>
    </ul>
</div>

<div class="overlay" id="overlay" @click="toggleSidebar()"></div>

<!-- Main Dashboard Content -->
<div class="main-content container">
    <!-- User Profile Header Section -->
    <div class="user-header">
        <div class="d-flex align-items-center">
            <img src="https://placehold.co/60x60/2196F3/ffffff?text=H" alt="Hospital Profile" class="rounded-circle me-3">
            <div>
                <h4 class="fw-bold mb-0">Welcome Back, [Hospital Name]!</h4>
                <p class="text-muted mb-0">Your profile is up to date.</p>
            </div>
        </div>
        <i class="fa-solid fa-bell fa-2x text-muted"></i>
    </div>
    
    <!-- Be the reason someone lives today section -->
    <div class="welcome-section">
        <h2 class="fw-bold mb-1">Be the reason someone lives today</h2>
        <p class="text-muted mb-0">Give hope. Give life.</p>
    </div>

    <!-- Buttons in Blue Cards -->
    <div class="row g-4 mb-4">
        <div class="col-md-6">
            <div class="dashboard-card bg-primary text-white text-center p-4">
                <h5 class="card-title fw-bold mb-3">Need Help?</h5>
                <p class="card-text">Raise a request for blood, plasma, or organs.</p>
                <button class="btn btn-light mt-3 rounded-pill fw-bold">
                    <i class="fa-solid fa-plus me-2"></i> Raise a Request
                </button>
            </div>
        </div>
        <div class="col-md-6">
            <div class="dashboard-card bg-primary text-white text-center p-4">
                <h5 class="card-title fw-bold mb-3">Manage Your Profile</h5>
                <p class="card-text">Update your details and manage your account.</p>
                <button class="btn btn-light mt-3 rounded-pill fw-bold">
                    <i class="fa-solid fa-gear me-2"></i> Account Settings
                </button>
            </div>
        </div>
    </div>

    <!-- Available Requests Section -->
    <div class="dashboard-card mb-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="card-title mb-0">Available Donors near you</h5>
            <a href="#" class="btn btn-sm btn-outline-primary rounded-pill px-4">View Donors</a>
        </div>
        <p class="card-text text-muted mb-0">No active donors at the moment. Check back later!</p>
    </div>

    <!-- Request Cards -->
    <div class="row g-4">
        <!-- Blood Request Card -->
        <div class="col-md-6 col-lg-3">
            <div class="dashboard-card text-center">
                <i class="fa-solid fa-droplet card-icon"></i>
                <h5 class="card-title">Blood Requests</h5>
                <p class="card-text">Manage your blood requests and find local donors.</p>
                <a href="#" class="btn btn-action mt-3">View Details</a>
            </div>
        </div>

        <!-- Plasma Request Card -->
        <div class="col-md-6 col-lg-3">
            <div class="dashboard-card text-center">
                <i class="fa-solid fa-syringe card-icon"></i>
                <h5 class="card-title">Plasma Requests</h5>
                <p class="card-text">Manage your plasma requests and find local donors.</p>
                <a href="#" class="btn btn-action mt-3">View Details</a>
            </div>
        </div>

        <!-- Organ Request Card -->
        <div class="col-md-6 col-lg-3">
            <div class="dashboard-card text-center">
                <i class="fa-solid fa-heart-pulse card-icon"></i>
                <h5 class="card-title">Organ Requests</h5>
                <p class="card-text">Manage your organ requests and find registered donors.</p>
                <a href="#" class="btn btn-action mt-3">View Details</a>
            </div>
        </div>

        <!-- My Requests Card -->
        <div class="col-md-6 col-lg-3">
            <div class="dashboard-card text-center">
                <i class="fa-solid fa-hand-holding-medical card-icon"></i>
                <h5 class="card-title">My Requests</h5>
                <p class="card-text">Track your hospital's requests and their status.</p>
                <a href="#" class="btn btn-action mt-3">View Contributions</a>
            </div>
        </div>
    </div>
</div>

</template>
<style>
        :root {
            --primary-color: #2196F3; /* Hospital blue */
            --brand-color: #e53935; /* JeevanDaan+ red */
            --secondary-color: #f7f9fc;
            --card-bg-color: #ffffff;
            --text-dark: #212529;
            --text-muted: #6c757d;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--secondary-color);
            min-height: 100vh;
        }

        /* Top Navbar */
        .top-navbar {
            background-color: var(--card-bg-color);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            padding: 1rem 2rem;
        }
        
        .navbar-brand {
            font-weight: 700;
            color: var(--brand-color) !important;
            font-size: 1.5rem;
        }

        .user-profile-img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
        }

        /* Side Navbar for small screens */
        .sidebar {
            position: fixed;
            top: 0;
            left: -300px;
            width: 250px;
            height: 100%;
            background-color: var(--card-bg-color);
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            transition: left 0.3s ease;
            z-index: 1050;
            padding: 1.5rem;
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

        .sidebar .nav-link {
            padding: 0.75rem 1rem;
            color: var(--text-dark);
            font-weight: 500;
            border-radius: 0.75rem;
            transition: background-color 0.2s ease;
        }

        .sidebar .nav-link:hover, .sidebar .nav-link.active {
            background-color: var(--primary-color);
            color: #fff;
        }

        /* Main Dashboard Content */
        .main-content {
            padding: 2rem;
            animation: fadeIn 0.8s ease-out forwards;
        }
        
        .user-header {
            background-color: var(--card-bg-color);
            border-radius: 1.5rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            padding: 2rem;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .welcome-section {
            background-color: var(--card-bg-color);
            border-radius: 1.5rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            padding: 2rem;
            margin-bottom: 2rem;
            text-align: center;
        }

        .dashboard-card {
            background-color: var(--card-bg-color);
            border-radius: 1.5rem;
            padding: 1.5rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
        }

        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }

        .card-icon {
            color: var(--primary-color);
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

       
        

        /* Animations */
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
    </style>
<script>
    export default {
        name : 'hospitaldash',

    
    methods : {
    toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('overlay');
        sidebar.classList.toggle('show');
        overlay.classList.toggle('show');
    }}}
</script>