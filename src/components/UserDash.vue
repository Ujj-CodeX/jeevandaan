<template>
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JeevanDaan+ Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
</head>



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
        <img src="https://placehold.co/40x40/e53935/ffffff?text=U" alt="User" class="user-profile-img">
    </div>
</nav>

<!-- Main Navbar for Mobile (with sidebar trigger) -->
<nav class="top-navbar d-flex d-lg-none justify-content-between align-items-center sticky-top">
    <a class="navbar-brand fw-bold" href="#">JeevanDaan+</a>
    <button class="btn btn-link p-0" onclick="toggleSidebar()">
        <i class="fas fa-bars fa-2x text-muted"></i>
    </button>
</nav>

<!-- Sidebar -->
<div class="sidebar" id="sidebar">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h5 class="fw-bold text-dark mb-0">Menu</h5>
        <button class="btn btn-link p-0" onclick="toggleSidebar()">
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

<div class="overlay" id="overlay" onclick="toggleSidebar()"></div>

<!-- Main Dashboard Content -->
<div class="main-content container">
    <!-- User Profile Header Section -->
    <div class="user-header">
        <div class="d-flex align-items-center">
            <img src="https://placehold.co/60x60/e53935/ffffff?text=U" alt="User Profile" class="rounded-circle me-3">
            <div>
                <h4 class="fw-bold mb-0">Welcome Back, [User Name]!</h4>
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

    <!-- Buttons in Red Cards -->
    <div class="row g-4 mb-4">
        <div class="col-md-6">
            <div class="dashboard-card bg-danger text-white text-center p-4">
                <h5 class="card-title fw-bold mb-3">Need Help?</h5>
                <p class="card-text">Raise a request for blood, plasma, or organs.</p>
                <button class="btn btn-light mt-3 rounded-pill fw-bold">
                    <i class="fa-solid fa-plus me-2"></i> Request for Help
                </button>
            </div>
        </div>
        <div class="col-md-6">
            <div class="dashboard-card bg-danger text-white text-center p-4">
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
            <h5 class="card-title mb-0">Available Requests near you</h5>
            <a href="#" class="btn btn-sm btn-outline-danger rounded-pill px-4">View Requests</a>
        </div>
        <p class="card-text text-muted mb-0">No active requests at the moment. Check back later!</p>
    </div>

    <!-- Donation Cards -->
    <div class="row g-4">
        <!-- Blood Donations Card -->
        <div class="col-md-6 col-lg-3">
            <div class="dashboard-card text-center">
                <i class="fa-solid fa-droplet card-icon"></i>
                <h5 class="card-title">Blood Donations</h5>
                <p class="card-text">Manage your donation history and find blood camps.</p>
                <a href="#" class="btn btn-action mt-3">View Details</a>
            </div>
        </div>

        <!-- Plasma Donations Card -->
        <div class="col-md-6 col-lg-3">
            <div class="dashboard-card text-center">
                <i class="fa-solid fa-syringe card-icon"></i>
                <h5 class="card-title">Plasma Donations</h5>
                <p class="card-text">Find info on plasma donation requirements and schedules.</p>
                <a href="#" class="btn btn-action mt-3">View Details</a>
            </div>
        </div>

        <!-- Organ Donations Card -->
        <div class="col-md-6 col-lg-3">
            <div class="dashboard-card text-center">
                <i class="fa-solid fa-heart-pulse card-icon"></i>
                <h5 class="card-title">Organ Donations</h5>
                <p class="card-text">Learn about organ donation and register your intent to donate.</p>
                <a href="#" class="btn btn-action mt-3">View Details</a>
            </div>
        </div>

        <!-- My Donations Card -->
        <div class="col-md-6 col-lg-3">
            <div class="dashboard-card text-center">
                <i class="fa-solid fa-hand-holding-medical card-icon"></i>
                <h5 class="card-title">My Donations</h5>
                <p class="card-text">Track the donation requests you have fulfilled or responded to.</p>
                <a href="#" class="btn btn-action mt-3">View Contributions</a>
            </div>
        </div>
    </div>
</div>




</template>

<script>
    
</script>
<style>
        :root {
            --primary-color: #e53935;
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
            color: var(--primary-color) !important;
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
            background-color: #e53935;
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

        /* Footer */
        

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