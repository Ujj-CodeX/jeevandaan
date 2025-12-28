
    <style>
        :root {
            --jd-red: #E63946;
            --jd-dark-red: #C1121F;
            --jd-soft-red: #fff5f5;
            --jd-gray: #f8f9fa;
            --jd-border-radius: 20px;
        }

        body {
            background-color: #fcfcfc;
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #2d3436;
        }

        /* NAVBAR */
        .navbar { background: white; border-bottom: 1px solid #eee; padding: 15px 0; }
        .nav-link { font-weight: 500; color: #636e72 !important; margin: 0 10px; }
        .nav-link:hover, .nav-link.active { color: var(--jd-red) !important; }
        .nav-icon { font-size: 1.2rem; color: #636e72; position: relative; }
        .notification-dot {
            position: absolute; top: 0; right: 0; width: 8px; height: 8px;
            background: var(--jd-red); border-radius: 50%; border: 2px solid white;
        }

        /* CARDS */
        .jd-card {
            background: white; border: none; border-radius: var(--jd-border-radius);
            box-shadow: 0 10px 30px rgba(0,0,0,0.03); transition: transform 0.3s ease;
            margin-bottom: 24px;
        }
        .jd-card:hover { transform: translateY(-5px); }

        /* HEADER & BADGES */
        .donor-badge {
            background: linear-gradient(135deg, #ffd700, #ffae00);
            color: white; padding: 5px 15px; border-radius: 50px; font-weight: 600; font-size: 0.8rem;
        }

        /* STAT CARDS */
        .stat-card { padding: 25px; text-align: center; }
        .stat-icon { 
            width: 50px; height: 50px; background: var(--jd-soft-red); 
            color: var(--jd-red); border-radius: 15px; display: flex;
            align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 1.5rem;
        }

        /* CALENDAR UI */
        .calendar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .pill-toggle { background: var(--jd-gray); border-radius: 50px; padding: 5px; display: inline-flex; }
        .pill-btn { border: none; background: none; padding: 6px 18px; border-radius: 50px; font-size: 0.85rem; transition: 0.3s; }
        .pill-btn.active { background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.05); color: var(--jd-red); font-weight: 600; }

        .calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; }
        .day-cell { height: 60px; display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: 12px; font-size: 0.9rem; position: relative; }
        .day-cell.active-camp::after {
            content: ''; width: 6px; height: 6px; background: var(--jd-red); 
            border-radius: 50%; position: absolute; bottom: 10px;
        }
        .day-cell:hover { background: var(--jd-soft-red); cursor: pointer; }

        /* SLIDER (NETFLIX STYLE) */
        .camp-slider { display: flex; overflow-x: auto; gap: 20px; padding-bottom: 15px; scrollbar-width: none; }
        .camp-slider::-webkit-scrollbar { display: none; }
        .camp-card { min-width: 280px; background: white; border-radius: 18px; overflow: hidden; border: 1px solid #f0f0f0; }
        .camp-img { height: 140px; background-size: cover; background-position: center; }

        /* EMERGENCY REQUEST */
        .emergency-banner {
            background: linear-gradient(135deg, var(--jd-red), var(--jd-dark-red));
            color: white; border-radius: var(--jd-border-radius); padding: 30px;
        }

        /* ELIGIBILITY CIRCLE */
        .eligibility-check {
            border: 4px solid #00b894; width: 100px; height: 100px; 
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-size: 2rem; color: #00b894; margin: 0 auto 15px;
        }
    </style>



<template>

<nav class="navbar navbar-expand-lg sticky-top">
    <div class="container">
        <a class="navbar-brand fw-bold text-danger" href="#">JeevanDaan<span class="text-dark">+</span></a>
        <button class="navbar-toggler border-0 shadow-none" type="button" data-bs-toggle="collapse" data-bs-target="#dashboardNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="dashboardNav">
            <ul class="navbar-nav mx-auto">
                <li class="nav-item"><a class="nav-link active" href="#">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Raise a Request</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Learn More</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Logout</a></li>
            </ul>
            <div class="d-flex align-items-center gap-4">
                <a href="#" class="nav-icon"><i class="fa-regular fa-bell"></i><span class="notification-dot"></span></a>
                <a href="#" class="nav-icon"><i class="fa-regular fa-circle-user"></i></a>
            </div>
        </div>
    </div>
</nav>

<div class="container py-4">
    <header class="row align-items-center mb-5">
        <div class="col-md-8">
            <h2 class="fw-bold mb-1">Hi, Rahul Sharma 👋</h2>
            <p class="text-muted">Your Lifesaver Dashboard | <span class="text-danger fw-medium">Every donation saves a life.</span></p>
        </div>
        <div class="col-md-4 text-md-end">
            <span class="donor-badge shadow-sm"><i class="fa-solid fa-crown me-2"></i>Gold Member</span>
        </div>
    </header>

    <div class="row g-4 mb-2">
        <div class="col-6 col-lg-3">
            <div class="jd-card stat-card">
                <div class="stat-icon"><i class="fa-solid fa-calendar-day"></i></div>
                <h6 class="text-muted small mb-1">Next Eligible</h6>
                <p class="fw-bold mb-0">12 Oct 2024</p>
            </div>
        </div>
        <div class="col-6 col-lg-3">
            <div class="jd-card stat-card">
                <div class="stat-icon"><i class="fa-solid fa-droplet"></i></div>
                <h6 class="text-muted small mb-1">Total Donations</h6>
                <p class="fw-bold mb-0">12 Units</p>
            </div>
        </div>
        <div class="col-6 col-lg-3">
            <div class="jd-card stat-card">
                <div class="stat-icon"><i class="fa-solid fa-heart-pulse"></i></div>
                <h6 class="text-muted small mb-1">Lives Impacted</h6>
                <p class="fw-bold mb-0">36 People</p>
            </div>
        </div>
        <div class="col-6 col-lg-3">
            <div class="jd-card stat-card">
                <div class="stat-icon"><i class="fa-solid fa-shield-check"></i></div>
                <h6 class="text-muted small mb-1">Reliability</h6>
                <p class="fw-bold mb-0 text-success">98 Score</p>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-lg-8">
            
            <div class="jd-card p-4">
                <div class="calendar-header">
                    <h5 class="fw-bold mb-0">Donation Camp Calendar</h5>
                    <div class="pill-toggle">
                        <button class="pill-btn active">Month</button>
                        <button class="pill-btn">Week</button>
                        <button class="pill-btn">List</button>
                    </div>
                </div>
                <div class="calendar-grid text-center mb-3">
                    <div class="text-muted small fw-bold">Mon</div><div class="text-muted small fw-bold">Tue</div><div class="text-muted small fw-bold">Wed</div><div class="text-muted small fw-bold">Thu</div><div class="text-muted small fw-bold">Fri</div><div class="text-muted small fw-bold">Sat</div><div class="text-muted small fw-bold">Sun</div>
                    <div class="day-cell text-muted">28</div><div class="day-cell text-muted">29</div><div class="day-cell text-muted">30</div><div class="day-cell">1</div><div class="day-cell active-camp">2</div><div class="day-cell">3</div><div class="day-cell">4</div>
                    <div class="day-cell">5</div><div class="day-cell active-camp">6</div><div class="day-cell">7</div><div class="day-cell">8</div><div class="day-cell">9</div><div class="day-cell active-camp">10</div><div class="day-cell">11</div>
                </div>
                <div class="p-3 bg-light rounded-4 d-flex justify-content-between align-items-center">
                    <div>
                        <span class="badge bg-danger rounded-pill mb-1">Recommended for You</span>
                        <p class="mb-0 fw-bold">Mega Drive - Apollo Hospital</p>
                        <small class="text-muted">10 Oct | 5.2 km away | Whole Blood & Platelets</small>
                    </div>
                    <button class="btn btn-danger btn-sm rounded-pill px-4">Register Slot</button>
                </div>
            </div>

            <h5 class="fw-bold mb-3 mt-4">Discover Nearby Camps</h5>
            <div class="camp-slider mb-4">
                <div class="camp-card shadow-sm">
                    <div class="camp-img" style="background-image: url('https://images.unsplash.com/photo-1615461066841-6116e61058f4?auto=format&fit=crop&q=80&w=600');"></div>
                    <div class="p-3">
                        <span class="text-muted small fw-bold">RED CROSS SOCIETY</span>
                        <h6 class="fw-bold mb-2">Corporate Drive, Sector 62</h6>
                        <button class="btn btn-outline-danger btn-sm w-100 rounded-pill">Enroll Now</button>
                    </div>
                </div>
                <div class="camp-card shadow-sm">
                    <div class="camp-img" style="background-image: url('https://images.unsplash.com/photo-1579152276502-545a248a6a61?auto=format&fit=crop&q=80&w=600');"></div>
                    <div class="p-3">
                        <span class="text-muted small fw-bold">GOVT HOSPITAL</span>
                        <h6 class="fw-bold mb-2">Weekend Rural Outreach</h6>
                        <button class="btn btn-outline-danger btn-sm w-100 rounded-pill">Enroll Now</button>
                    </div>
                </div>
            </div>

            <div class="jd-card p-4">
                <h5 class="fw-bold mb-3">Verified Partner Banks Nearby</h5>
                <div class="d-flex gap-2 mb-3 overflow-auto pb-2">
                    <button class="btn btn-light btn-sm rounded-pill text-nowrap px-3 active">All Banks</button>
                    <button class="btn btn-light btn-sm rounded-pill text-nowrap px-3">Whole Blood</button>
                    <button class="btn btn-light btn-sm rounded-pill text-nowrap px-3">Platelets</button>
                    <button class="btn btn-light btn-sm rounded-pill text-nowrap px-3">Plasma</button>
                </div>
                <div class="list-group list-group-flush">
                    <div class="list-group-item d-flex justify-content-between align-items-center px-0 py-3 bg-transparent">
                        <div>
                            <p class="mb-0 fw-bold">Max Super Speciality</p>
                            <small class="text-muted">Verified Partner • 2.1 km</small>
                        </div>
                        <span class="badge bg-success rounded-pill">Stock: High</span>
                    </div>
                    <div class="list-group-item d-flex justify-content-between align-items-center px-0 py-3 bg-transparent">
                        <div>
                            <p class="mb-0 fw-bold">AIIMS Trauma Centre</p>
                            <small class="text-muted">Govt Partner • 4.5 km</small>
                        </div>
                        <span class="badge bg-warning text-dark rounded-pill">Stock: Medium</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-lg-4">
            <div class="jd-card p-4 border-start border-5 border-danger">
                <div class="d-flex justify-content-between mb-3">
                    <h5 class="fw-bold text-danger mb-0">Emergency Need</h5>
                    <span class="spinner-grow spinner-grow-sm text-danger"></span>
                </div>
                <p class="small">O+ Blood Required urgently at <strong>City Hospital</strong>. 3 units needed by tonight.</p>
                <div class="d-flex gap-2">
                    <button class="btn btn-danger btn-sm flex-grow-1 rounded-pill">Accept</button>
                    <button class="btn btn-light btn-sm flex-grow-1 rounded-pill">Decline</button>
                </div>
            </div>
            <div class="jd-card p-4 text-center">
                <h5 class="fw-bold mb-3">Eligibility Status</h5>
                <div class="eligibility-check shadow-sm"><i class="fa-solid fa-check"></i></div>
                <p class="fw-bold mb-1">Ready to Donate!</p>
                <p class="small text-muted mb-3">You completed your cooldown of 90 days. Health markers (Hb/BP) look optimal.</p>
                <button class="btn btn-danger w-100 rounded-pill py-2">Quick Health Pre-Check</button>
            </div>

            <div class="jd-card p-4">
                <h5 class="fw-bold mb-3">Achievements</h5>
                <div class="d-flex flex-wrap gap-3 justify-content-center">
                    <div class="text-center" style="width: 70px;">
                        <img src="https://cdn-icons-png.flaticon.com/512/3112/3112946.png" class="img-fluid opacity-100 mb-1" alt="badge">
                        <small class="d-block x-small fw-bold">Hero</small>
                    </div>
                    <div class="text-center" style="width: 70px;">
                        <img src="https://cdn-icons-png.flaticon.com/512/3112/3112946.png" class="img-fluid opacity-25 mb-1" alt="badge">
                        <small class="d-block x-small">Reliable</small>
                    </div>
                    <div class="text-center" style="width: 70px;">
                        <img src="https://cdn-icons-png.flaticon.com/512/3112/3112946.png" class="img-fluid opacity-25 mb-1" alt="badge">
                        <small class="d-block x-small">Fast Help</small>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <div class="emergency-banner mb-5 text-center shadow-lg">
        <h3 class="fw-bold">In Need of Blood?</h3>
        <p class="mb-4">Raise a verified emergency request to reach 25,000+ donors instantly.</p>
        <button class="btn btn-light btn-lg rounded-pill px-5 fw-bold text-danger">Start Emergency Request</button>
    </div>

    
</div>


</template>