<template>
    <nav class="top-navbar d-none d-lg-flex justify-content-between align-items-center sticky-top">
    <a class="navbar-brand fw-bold text-danger"  href="#">JeevanDaan+</a>
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
        <li class="nav-item">
            <a class="nav-link text-dark" href="#">Raise Query</a>
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
                <i class="fas fa-cog me-2"></i> Raise a Query
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
<div class="main-content container mt-4">
    
    <div class="hero-section text-center mb-5 p-5 rounded-5 shadow-sm">
      <h1 class="display-5 fw-bold text-primary">Welcome, [Hospital Name]</h1>
      <p class="lead text-muted">"Be the reason someone lives today. Give hope. Give life."</p>
      <div class="mt-4">
        <span class="badge rounded-pill bg-success p-2 px-3">
          <i class="fas fa-check-circle me-1"></i> Verified Partner
        </span>
      </div>
    </div>

    <div class="row g-4 mb-5">
      <div class="col-md-4">
        <div class="dashboard-card action-card text-center p-4">
          <div class="icon-circle bg-danger-soft mb-3">
            <i class="fa-solid fa-truck-medical text-danger"></i>
          </div>
          <h5 class="fw-bold">Urgent Request</h5>
          <p class="small text-muted">Raise a priority donor request for emergencies.</p>
          <button class="btn btn-outline-danger w-100 rounded-pill">Raise Now</button>
        </div>
      </div>
      <div class="col-md-4">
        <div class="dashboard-card action-card text-center p-4">
          <div class="icon-circle bg-primary-soft mb-3">
            <i class="fa-solid fa-tent text-primary"></i>
          </div>
          <h5 class="fw-bold">Organize Camp</h5>
          <p class="small text-muted">Schedule and manage a blood donation drive.</p>
          <button class="btn btn-outline-primary w-100 rounded-pill">Create Camp</button>
        </div>
      </div>
      <div class="col-md-4">
        <div class="dashboard-card action-card text-center p-4">
          <div class="icon-circle bg-success-soft mb-3">
            <i class="fa-solid fa- boxes-stacked text-success"></i>
          </div>
          <h5 class="fw-bold">Stock Update</h5>
          <p class="small text-muted">Manually update your current blood inventory.</p>
          <button class="btn btn-outline-success w-100 rounded-pill">Update Stock</button>
        </div>
      </div>
    </div>

    <div class="dashboard-card mb-5 p-4 border-primary border-start border-4">
      <h5 class="fw-bold mb-3"><i class="fa-solid fa-magnifying-glass me-2"></i>Verify Attender Request</h5>
      <div class="input-group mb-3">
        <input type="text" v-model="refNumber" class="form-control form-control-lg" placeholder="Enter Reference Number (e.g., JD-10293)">
        <button class="btn btn-primary px-4" @click="searchRequest">Search Details</button>
      </div>
    </div>

    <div class="dashboard-card p-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h5 class="fw-bold mb-0">Live Blood Inventory</h5>
        <span class="text-muted small text-uppercase fw-bold">Last updated: Just now</span>
      </div>
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>Blood Group</th>
              <th>Status</th>
              <th>Quantity (Units)</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="stock in inventory" :key="stock.group">
              <td class="fw-bold text-danger">{{ stock.group }}</td>
              <td>
                <span :class="stock.qty < 5 ? 'text-danger' : 'text-success'">
                  <i class="fas fa-circle font-xs me-1"></i> {{ stock.qty < 5 ? 'Low Stock' : 'Available' }}
                </span>
              </td>
              <td>{{ stock.qty }}</td>
              <td><button class="btn btn-sm btn-light border">Edit</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showResultModal" class="custom-modal-overlay d-flex align-items-center justify-content-center">
      <div class="request-details-card p-5 shadow-lg">
        <button class="btn-close float-end" @click="showResultModal = false"></button>
        <h3 class="fw-bold mb-4">Request Details</h3>
        <div class="row text-start mb-4">
          <div class="col-6">
            <label class="text-muted small">Patient Name</label>
            <p class="fw-bold">Rahul Sharma</p>
          </div>
          <div class="col-6">
            <label class="text-muted small">Blood Required</label>
            <p class="fw-bold text-danger">O+ Positive</p>
          </div>
        </div>

        <div v-if="!showRejectionInput" class="d-flex gap-3">
          <button class="btn btn-success flex-grow-1 py-3 rounded-3 shadow" @click="verifyRequest">
            <i class="fa-solid fa-check me-2"></i> Verify Request
          </button>
          <button class="btn btn-outline-danger flex-grow-1 py-3 rounded-3" @click="showRejectionInput = true">
            <i class="fa-solid fa-xmark me-2"></i> Decline
          </button>
        </div>

        <div v-else class="mt-3 text-start">
          <label class="fw-bold mb-2">Reason for Rejection</label>
          <select class="form-select mb-3">
            <option>Stock Unavailable</option>
            <option>Invalid Documentation</option>
            <option>Ineligible Patient Condition</option>
            <option>Other</option>
          </select>
          <textarea class="form-control mb-3" placeholder="Additional notes..."></textarea>
          <button class="btn btn-danger w-100" @click="submitDecline">Submit Rejection</button>
        </div>
      </div>
    </div>
</div>

</template>
<style scoped>
        :root {
            --primary-color: #2196F3; /* Hospital blue */
            
            --secondary-color: #f7f9fc;
            --card-bg-color: #ffffff;
            --text-dark: #212529;
            --text-muted: #6c757d;
            --brand-red: #E63946;
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

       /* Glassmorphism Rejection Modal */
.custom-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(12px); /* This creates the blur effect */
    -webkit-backdrop-filter: blur(12px);
    z-index: 2000;
    animation: fadeIn 0.3s ease;
}

.request-details-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 2rem;
    width: 90%;
    max-width: 500px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.hero-section {
    background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
    border: 1px solid rgba(33, 150, 243, 0.1);
}

/* Icon circles for action cards */
.icon-circle {
    width: 60px;
    height: 60px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin: 0 auto;
}

.bg-danger-soft { background: #ffebee; }
.bg-primary-soft { background: #e3f2fd; }
.bg-success-soft { background: #e8f5e9; }

.action-card {
    border: 1px solid transparent;
}

.action-card:hover {
    border-color: var(--primary-color);
}

.font-xs { font-size: 0.6rem; }
        

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
  name: 'hospitaldash',
  data() {
    return {
      refNumber: '',
      showResultModal: false,
      showRejectionInput: false,
      inventory: [
        { group: 'A+', qty: 12 },
        { group: 'B+', qty: 3 },
        { group: 'O-', qty: 8 },
        { group: 'AB+', qty: 15 }
      ]
    }
  },
  methods: {
    toggleSidebar() {
      const sidebar = document.getElementById('sidebar');
      const overlay = document.getElementById('overlay');
      sidebar.classList.toggle('show');
      overlay.classList.toggle('show');
    },
    searchRequest() {
      if(this.refNumber.length > 0) {
        this.showResultModal = true;
        this.showRejectionInput = false;
      } else {
        alert("Please enter a reference number");
      }
    },
    verifyRequest() {
      alert("Request Verified Successfully!");
      this.showResultModal = false;
    },
    submitDecline() {
      alert("Request Declined.");
      this.showResultModal = false;
    }
  }
}
</script>