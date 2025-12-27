<template>
<nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top shadow-sm">
    <div class="container">
        <a class="navbar-brand fw-bold text-danger" href="#">JeevanDaan<span class="text-dark">+</span></a>
        <button class="navbar-toggler shadow-none border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav mx-auto">
                <li class="nav-item">
                    <router-link class="nav-link" to="#">Home</router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="#">Learn More</router-link></li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/register">Join US</router-link></li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/partnersreg">Join as Partner</router-link></li>
            </ul>
            <div class="d-flex flex-column flex-lg-row gap-2">
                <router-link to="/login" class="btn btn-outline-danger btn-sm rounded-pill px-3">Login</router-link>
                <router-link to="/partners_login" class="btn btn-danger btn-sm rounded-pill px-3 text-white">Partner Login</router-link>
            </div>
        </div>
    </div>
</nav>

<section class="hero-section">
    <div class="container">
        <h1 class="display-3 fw-bold mb-4">Donate Blood. Save Lives.</h1>
        <p class="lead mb-5 px-md-5">Join a verified network of government & private blood banks for safe, real-time blood donation and emergency requests.</p>
        <div class="d-flex flex-column flex-md-row justify-content-center gap-3">
            <a href="#" class="btn btn-red shadow-lg">Register as Donor</a>
            <a href="#" class="btn btn-outline-white">Find Blood Banks</a>
        </div>
    </div>
</section>

<section class="py-5 bg-white">
    <div class="container py-5">
        <h2 class="text-center fw-bold mb-5">How JeevanDaan+ Works</h2>
        
        <div class="row align-items-center mb-5">
            <div class="col-md-6 text-center"><img src="https://cdni.iconscout.com/illustration/premium/thumb/blood-donation-center-4437142-3712217.png" class="work-sticker"></div>
            <div class="col-md-6 text-center text-md-start">
                <h4 class="fw-bold text-danger">Verified Partner Network</h4>
                <p class="text-muted">Govt & private licensed blood banks with transparent charges and safe issue processes.</p>
            </div>
        </div>

        <div class="row align-items-center mb-5 flex-column-reverse flex-md-row">
            <div class="col-md-6 text-center text-md-end">
                <h4 class="fw-bold text-danger">Smart Emergency Requests</h4>
                <p class="text-muted">Upload documents for instant verification. No middleman, just direct life-saving support.</p>
            </div>
            <div class="col-md-6 text-center"><img src="https://cdni.iconscout.com/illustration/premium/thumb/blood-test-4437139-3712214.png" class="work-sticker"></div>
        </div>

        <div class="row align-items-center mb-5">
            <div class="col-md-6 text-center"><img src="https://cdni.iconscout.com/illustration/premium/thumb/patient-safety-illustration-download-in-svg-png-gif-formats--security-medical-care-shield-hospital-pack-healthcare-illustrations-4715424.png" class="work-sticker"></div>
            <div class="col-md-6 text-center text-md-start">
                <h4 class="fw-bold text-danger">Donor Safety Model</h4>
                <p class="text-muted">Privacy-first design. No direct contact with patients; manage everything via status buttons.</p>
            </div>
        </div>

        <div class="row align-items-center mb-5 flex-column-reverse flex-md-row">
            <div class="col-md-6 text-center text-md-end">
                <h4 class="fw-bold text-danger">Real-Time Matching</h4>
                <p class="text-muted">Location-based matching with reliability scoring for the fastest emergency response.</p>
            </div>
            <div class="col-md-6 text-center"><img src="https://cdni.iconscout.com/illustration/premium/thumb/location-matching-illustration-download-in-svg-png-gif-formats--search-find-gps-navigation-pack-maps-illustrations-5343467.png" class="work-sticker"></div>
        </div>

        <div class="row align-items-center mb-5">
            <div class="col-md-6 text-center"><img src="https://cdni.iconscout.com/illustration/premium/thumb/blood-donation-camp-illustration-download-in-svg-png-gif-formats--donor-volunteer-help-community-pack-healthcare-illustrations-4715423.png" class="work-sticker"></div>
            <div class="col-md-6 text-center text-md-start">
                <h4 class="fw-bold text-danger">Donation Camps</h4>
                <p class="text-muted">Multi-partner events and mass volunteer matching for scheduled community drives.</p>
            </div>
        </div>

        <div class="row align-items-center mb-5 flex-column-reverse flex-md-row">
            <div class="col-md-6 text-center text-md-end">
                <h4 class="fw-bold text-danger">Transparent Stock</h4>
                <p class="text-muted">Partner-managed daily updates ensure you never visit a bank with zero stock.</p>
            </div>
            <div class="col-md-6 text-center"><img src="https://cdni.iconscout.com/illustration/premium/thumb/inventory-management-illustration-download-in-svg-png-gif-formats--warehouse-stock-logistics-pack-business-illustrations-6419736.png" class="work-sticker"></div>
        </div>
    </div>
</section>

<section class="py-5 bg-light overflow-hidden">
    <div class="container text-center">
        <h2 class="fw-bold mb-5">How Donation Works</h2>
        <div class="row g-0 flow-container">
            <div class="col-12 col-lg-2 flow-step">
                <i class="fa-solid fa-bell"></i>
                <h6 class="fw-bold">Donor Notified</h6>
                <div class="flow-line"></div>
            </div>
            <div class="col-12 col-lg-2 flow-step">
                <i class="fa-solid fa-thumbs-up"></i>
                <h6 class="fw-bold">Accepts Request</h6>
                <div class="flow-line"></div>
            </div>
            <div class="col-12 col-lg-2 flow-step">
                <i class="fa-solid fa-hospital-user"></i>
                <h6 class="fw-bold">Visits Partner</h6>
                <div class="flow-line"></div>
            </div>
            <div class="col-12 col-lg-2 flow-step">
                <i class="fa-solid fa-hand-holding-medical"></i>
                <h6 class="fw-bold">Donates Safely</h6>
                <div class="flow-line"></div>
            </div>
            <div class="col-12 col-lg-2 flow-step">
                <i class="fa-solid fa-database"></i>
                <h6 class="fw-bold">Stock Updated</h6>
                <div class="flow-line"></div>
            </div>
            <div class="col-12 col-lg-2 flow-step">
                <i class="fa-solid fa-medal"></i>
                <h6 class="fw-bold">Recognition</h6>
            </div>
        </div>
        
        <div class="mt-5 p-4 border border-danger rounded-4 d-inline-block bg-white shadow-sm">
            <h5 class="fw-bold text-danger mb-2"><i class="fa-solid fa-stethoscope me-2"></i>Quick Compatibility Check</h5>
            <p class="mb-0 text-muted px-md-5">All donors must undergo a mandatory physical check for eligibility at the partner bank.</p>
        </div>
    </div>
</section>

<section class="impact-section text-center">
    <div class="container">
        <div class="row g-4">
            <div class="col-md-4"><span class="stat-number">25k+</span><p class="mt-2 fw-bold">Donors Registered</p></div>
            <div class="col-md-4"><span class="stat-number">10k+</span><p class="mt-2 fw-bold">Lives Helped</p></div>
            <div class="col-md-4"><span class="stat-number">450+</span><p class="mt-2 fw-bold">Partner Blood Banks</p></div>
        </div>
    </div>
</section>

<section class="py-5 bg-white">
    <div class="container text-center py-5">
        <h2 class="fw-bold mb-5 border-bottom pb-3 d-inline-block">Trust & Safety</h2>
        <div class="row g-4 mt-3">
            <div class="col-6 col-md-3"><i class="fa-solid fa-shield-halved trust-icon"></i><p class="small fw-bold">WHO & NACO Guidelines</p></div>
            <div class="col-6 col-md-3"><i class="fa-solid fa-file-shield trust-icon"></i><p class="small fw-bold">Anti-Fraud Protection</p></div>
            <div class="col-6 col-md-3"><i class="fa-solid fa-certificate trust-icon"></i><p class="small fw-bold">Licensed Partners Only</p></div>
            <div class="col-6 col-md-3"><i class="fa-solid fa-lock trust-icon"></i><p class="small fw-bold">Secure Data Design</p></div>
        </div>
    </div>
</section>

<section class="camp-carousel-container">
    <div class="container">
        <h3 class="text-center mb-4 fw-bold">Recent Blood Donation Camps</h3>
        <div id="campCarousel" class="carousel slide carousel-fade shadow-lg rounded-4 overflow-hidden" data-bs-ride="carousel">
            <div class="carousel-inner">
                <div class="carousel-item active"><img src="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&q=80&w=2000" class="d-block w-100"></div>
                <div class="carousel-item"><img src="https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?auto=format&fit=crop&q=80&w=2000" class="d-block w-100"></div>
            </div>
        </div>
    </div>
</section>

<section class="py-5 bg-light">
    <div class="container py-5 text-center">
        <h2 class="fw-bold mb-5">Voices of Our Lifesavers</h2>
        <div id="reviewCarousel" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">
                <div class="carousel-item active">
                    <div class="row justify-content-center">
                        <div class="col-md-8">
                            <div class="card border-0 shadow-sm p-4 rounded-4">
                                <i class="fa-solid fa-quote-left text-danger opacity-25 fs-1 mb-3"></i>
                                <p class="lead italic">"JeevanDaan+ made the donation process so transparent. Truly rewarding!"</p>
                                <h6 class="fw-bold mb-0">Arjun Sharma</h6>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="py-5 bg-white text-center">
    <div class="container py-5" style="background: linear-gradient(rgba(230, 57, 70, 0.9), rgba(193, 18, 31, 1)); padding: 60px; border-radius: 20px; color: white;">
        <h2 class="display-5 fw-bold mb-4">Become a Lifesaver Today.</h2>
        <div class="d-flex flex-column flex-md-row justify-content-center gap-3">
            <button class="btn btn-light btn-lg rounded-pill px-5 fw-bold text-danger">Join as Donor</button>
            <button class="btn btn-outline-white btn-lg rounded-pill px-4">Organize a Blood Camp</button>
        </div>
    </div>
</section>



</template>
<style>
        :root {
            --jd-red: #E63946;
            --jd-dark-red: #C1121F;
            --jd-white: #FFFFFF;
            --jd-light-bg: #F8F9FA;
        }

        body { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; overflow-x: hidden; }

        /* NAVBAR STYLING */
        .navbar-brand { font-size: 1.5rem; letter-spacing: -1px; }
        .nav-link { font-weight: 500; color: #333 !important; margin: 0 5px; transition: 0.3s; }
        .nav-link:hover { color: var(--jd-red) !important; }

        /* HERO SECTION */
        .hero-section {
            background: linear-gradient(90deg, rgba(230, 57, 70, 0.9) 0%, rgba(193, 18, 31, 0.7) 100%), 
                url('https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&q=80&w=2000');
            background-size: cover;
            background-position: center;
            padding: 100px 0;
            color: white;
            text-align: center;
        }

        .btn-red { background: var(--jd-red); color: white; font-weight: 600; border-radius: 50px; padding: 12px 30px; border: none; }
        .btn-red:hover { background: var(--jd-dark-red); color: white; }
        .btn-outline-white { background: transparent; color: white; font-weight: 600; border-radius: 50px; padding: 12px 30px; border: 2px solid white; }
        .btn-outline-white:hover { background: white; color: var(--jd-red); }

        /* HOW IT WORKS STICKERS */
        .work-sticker { max-width: 220px; width: 100%; height: auto; }

        /* RESPONSIVE DONOR FLOW SYSTEM */
        .flow-container { position: relative; }
        .flow-step { text-align: center; position: relative; padding: 20px; z-index: 2; }
        .flow-step i { 
            font-size: 2.2rem; 
            color: var(--jd-red); 
            background: white; 
            padding: 15px; 
            border-radius: 50%; 
            box-shadow: 0 5px 15px rgba(230, 57, 70, 0.2);
            margin-bottom: 15px; 
        }

        /* Desktop Arrows (Horizontal) */
        @media (min-width: 992px) {
            .flow-line { 
                position: absolute; 
                top: 40px; 
                right: -25%; 
                width: 50%; 
                border-top: 3px dashed var(--jd-red); 
                opacity: 0.3;
                z-index: 1;
            }
        }

        /* Mobile Arrows (Vertical) */
        @media (max-width: 991px) {
            .flow-step { margin-bottom: 40px; }
            .flow-step:not(:last-child)::after {
                content: '\f063'; /* FontAwesome Down Arrow */
                font-family: "Font Awesome 6 Free";
                font-weight: 900;
                position: absolute;
                bottom: -35px;
                left: 50%;
                transform: translateX(-50%);
                font-size: 1.5rem;
                color: var(--jd-red);
            }
        }

        /* IMPACT SECTION */
        .impact-section { background: var(--jd-red); color: white; padding: 80px 0; }
        .stat-number { font-size: 3.5rem; font-weight: 800; line-height: 1; }

        /* TRUST SECTION */
        .trust-icon { font-size: 40px; color: var(--jd-red); margin-bottom: 15px; }
        
        /* CAMP CAROUSEL */
        .carousel-item img { height: 450px; object-fit: cover; border-radius: 15px; }
    </style>