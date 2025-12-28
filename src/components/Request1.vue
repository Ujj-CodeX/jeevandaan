
    <style>
        :root {
            --jd-red: #E63946;
            --jd-dark-red: #C1121F;
            --jd-light-bg: #F8F9FA;
            --jd-hindi: #6c757d;
        }

        body {
            background-color: var(--jd-light-bg);
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            color: #2d3436;
        }

        /* Bilingual Typography */
        .hindi-sub {
            display: block;
            font-size: 0.85rem;
            color: var(--jd-hindi);
            margin-top: -2px;
            font-weight: 400;
        }

        /* XL Cards */
        .section-card {
            background: #ffffff;
            border: none;
            border-radius: 24px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
            margin-bottom: 24px;
        }

        /* Legal Warning Header */
        .legal-header {
            background: linear-gradient(135deg, #fff5f5 0%, #ffebeb 100%);
            border: 1px solid #ffcccc;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 30px;
        }

        .ipc-tag {
            background: #fff;
            border-radius: 10px;
            padding: 8px 12px;
            display: inline-block;
            margin: 4px;
            font-size: 0.85rem;
            border: 1px solid #eee;
        }
        .ipc-sub {
    font-size: 0.75rem;
    color: #444;
}

.ipc-punish {
    font-size: 0.72rem;
    color: #222;
    font-weight: 600;
    display: block;
    margin-top: 4px;
}

        /* Form Styling */
        .form-label {
            font-weight: 600;
            margin-bottom: 0;
            color: #333;
        }

        .form-control, .form-select {
            border-radius: 12px;
            padding: 12px 15px;
            border: 1.5px solid #eee;
            background-color: #fafafa;
            transition: 0.3s;
        }

        .form-control:focus {
            background-color: #fff;
            border-color: var(--jd-red);
            box-shadow: 0 0 0 0.25rem rgba(230, 57, 70, 0.1);
        }

        /* Upload Boxes */
        .upload-area {
            border: 2px dashed #ddd;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: 0.3s;
            position: relative;
        }

        .upload-area:hover {
            border-color: var(--jd-red);
            background: #fff5f5;
        }

        .upload-success {
            color: #27ae60;
            font-size: 1.2rem;
            position: absolute;
            top: 10px;
            right: 15px;
            display: none; /* Toggle with JS */
        }

        /* Buttons */
        .btn-jd-primary {
            background: var(--jd-red);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 15px 40px;
            font-weight: 700;
            transition: 0.3s;
            box-shadow: 0 8px 20px rgba(230, 57, 70, 0.3);
        }

        .btn-jd-primary:hover {
            background: var(--jd-dark-red);
            transform: translateY(-2px);
            color: white;
        }

        /* Frosted Modal */
        .frosted-modal .modal-content {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(15px);
            border: none;
            border-radius: 30px;
        }

        .policy-item {
            background: white;
            border-radius: 15px;
            padding: 12px 15px;
            margin-bottom: 10px;
            border-left: 4px solid var(--jd-red);
            box-shadow: 0 4px 10px rgba(0,0,0,0.02);
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

<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-10 col-xl-8">
            
            <div class="legal-header shadow-sm">
                <div class="d-flex align-items-start gap-3 mb-3">
                    <i class="fa-solid fa-scale-balanced text-danger fs-2"></i>
                    <div>
                        <h5 class="fw-bold text-danger mb-0">Legal Notice: Fake or Forged Blood Requests Are Punishable Under IPC.</h5>
                        <span class="hindi-sub text-danger opacity-75 fw-bold">कानूनी सूचना: झूठे या नकली रक्त अनुरोध IPC के तहत दंडनीय अपराध हैं।</span>
                    </div>
                </div>
                <div class="d-flex flex-wrap gap-2">

    <!-- IPC 419/420 -->
    <div class="ipc-tag">
        <strong>IPC 419 / 420:</strong> 
        Impersonation, Cheating & Fraud  
        <br><span class="ipc-sub">छद्मवेश, धोखाधड़ी व ठगी</span>
        <br><span class="ipc-punish">
            Punishment: Up to 3–7 years imprisonment + fine  
            <br>दंड: 3–7 वर्ष की कैद + जुर्माना
        </span>
    </div>

    <!-- IPC 464/468 -->
    <div class="ipc-tag">
        <strong>IPC 464 / 468:</strong> 
        Forgery of Medical Documents  
        <br><span class="ipc-sub">चिकित्सीय दस्तावेज़ों की जालसाज़ी</span>
        <br><span class="ipc-punish">
            Punishment: Up to 7 years imprisonment  
            <br>दंड: 7 वर्ष तक की कैद
        </span>
    </div>

    <!-- IPC 471 -->
    <div class="ipc-tag">
        <strong>IPC 471:</strong> 
        Using Forged Hospital Papers  
        <br><span class="ipc-sub">नकली दस्तावेज़ का उपयोग</span>
        <br><span class="ipc-punish">
            Punishment: Same as forgery (up to 7 years)  
            <br>दंड: जालसाज़ी के समान, 7 वर्ष तक की कैद
        </span>
    </div>

    <!-- WHO/NACO -->
    <div class="ipc-tag">
        <strong>WHO / NACO:</strong> 
        Ethical Blood Issuance Rules  
        <br><span class="ipc-sub">नैतिक रक्त निर्गम दिशानिर्देश</span>
        <br><span class="ipc-punish">
            Violations → License suspension/cancellation  
            <br>उल्लंघन → लाइसेंस निलंबन/रद्द
        </span>
    </div>

</div>

            </div>

            <form id="bloodRequestForm">
                <div class="section-card">
                    <h5 class="fw-bold mb-4 border-bottom pb-2">
                        <i class="fa-solid fa-user-injured text-danger me-2"></i>Patient Details
                        <span class="hindi-sub d-inline ms-2 fs-6">मरीज़ का विवरण</span>
                    </h5>
                    
                    <div class="row g-4">
                        <div class="col-md-8">
                            <label class="form-label">Patient Full Name</label>
                            <span class="hindi-sub">मरीज़ का पूरा नाम</span>
                            <input type="text" class="form-control" placeholder="Enter full name">
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">Age</label>
                            <span class="hindi-sub">आयु</span>
                            <input type="number" class="form-control" placeholder="Years">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Required Blood Group</label>
                            <span class="hindi-sub">आवश्यक रक्त समूह</span>
                            <select class="form-select">
                                <option selected disabled>Select Blood Group</option>
                                <option>A+</option><option>A-</option><option>B+</option><option>B-</option>
                                <option>O+</option><option>O-</option><option>AB+</option><option>AB-</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Category of Request</label>
                            <span class="hindi-sub">अनुरोध का प्रकार</span>
                            <select class="form-select">
                                <option>Emergency (आपातकाल)</option>
                                <option>Surgery (सर्जरी)</option>
                                <option>ICU (आईसीयू)</option>
                                <option>Scheduled (नियोजित)</option>
                            </select>
                        </div>
                        <div class="col-md-12">
                            <label class="form-label">Hospital Name</label>
                            <span class="hindi-sub">अस्पताल का नाम</span>
                            <input type="text" class="form-control" placeholder="Search or enter Hospital Name">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Doctor’s Name</label>
                            <span class="hindi-sub">डॉक्टर का नाम</span>
                            <input type="text" class="form-control" placeholder="Dr. Name">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Attender’s Phone Number</label>
                            <span class="hindi-sub">परिजन का मोबाइल नंबर</span>
                            <input type="tel" class="form-control" placeholder="+91">
                        </div>
                    </div>
                </div>



                <div class="section-card">
                    <h5 class="fw-bold mb-4 border-bottom pb-2">Attender Details <span class="hindi-sub d-inline ms-2 fs-6">परिजन का विवरण</span></h5>
                    <div class="row g-4">
                        <div class="col-md-6">
                            <label class="form-label">Attender ID Type</label>
                            <span class="hindi-sub">परिजन का पहचान प्रकार</span>
                            <select class="form-select">
                                <option>Aadhaar Card</option>
                                <option>Driving License</option>
                                <option>Voter ID</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Attender ID Number</label>
                            <span class="hindi-sub">पहचान पत्र संख्या</span>
                            <input type="text" class="form-control" placeholder="Enter ID Number">
                        </div>
                        <div class="col-12">
                            <div class="id-verification-alert d-flex align-items-center gap-3">
                                <i class="fa-solid fa-id-card-clip fs-3 text-warning"></i>
                                <div>
                                    <p class="mb-0 fw-bold small text-dark">Mandatory: Attender must carry the above original ID to the blood bank for verification.</p>
                                    <span class="hindi-sub text-dark opacity-75">अनिवार्य: परिजन को सत्यापन के लिए ब्लड बैंक में उपरोक्त मूल पहचान पत्र लाना होगा।</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="section-card">
                    <h5 class="fw-bold mb-4 border-bottom pb-2">
                        <i class="fa-solid fa-cloud-arrow-up text-danger me-2"></i>Document Upload
                        <span class="hindi-sub d-inline ms-2 fs-6">दस्तावेज़ अपलोड</span>
                    </h5>
                    <div class="row g-3">
                        <div class="col-md-4">
                            <div class="upload-area">
                                <i class="fa-solid fa-file-signature mb-2"></i>
                                <p class="small mb-0">Hospital Letter Head</p>
                                <span class="hindi-sub x-small">हॉस्पिटल लेटरहेड</span>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="upload-area">
                                <i class="fa-solid fa-file-prescription mb-2"></i>
                                <p class="small mb-0">Doctor's Prescription</p>
                                <span class="hindi-sub x-small">डॉक्टर की पर्ची</span>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="upload-area">
                                <i class="fa-solid fa-camera mb-2"></i>
                                <p class="small mb-0">Patient Live Photo</p>
                                <span class="hindi-sub x-small">मरीज़ की फोटो</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="section-card border-start border-danger border-4">
                    <div class="row">
                        <div class="col-md-1 d-none d-md-block text-center pt-2">
                            <i class="fa-solid fa-circle-info text-danger fs-3"></i>
                        </div>
                        <div class="col-md-11">
                            <p class="mb-2"><strong>Crossmatch Required:</strong> Blood is issued only after compatibility check.
                            <span class="hindi-sub">क्रॉस-मैच अनिवार्य: रक्त केवल संगतता जाँच के बाद दिया जाएगा।</span></p>
                            <p class="mb-0"><strong>Processing Fees:</strong> As per government guidelines.
                            <span class="hindi-sub">सरकारी नियमों के अनुसार प्रोसेसिंग शुल्क लागू होगा।</span></p>
                        </div>
                    </div>
                </div>

                <div class="section-card">
                    <div class="form-check mb-3">
                        <input class="form-check-input" type="checkbox" id="tc1">
                        <label class="form-check-label small fw-bold" for="tc1">
                            I confirm all documents are authentic.
                            <span class="hindi-sub fw-normal">मैं पुष्टि करता/करती हूँ कि सभी दस्तावेज़ वास्तविक हैं।</span>
                        </label>
                    </div>
                    <div class="form-check mb-3">
                        <input class="form-check-input" type="checkbox" id="tc2">
                        <label class="form-check-label small fw-bold" for="tc2">
                            I understand fake requests can lead to IPC legal action.
                            <span class="hindi-sub fw-normal">मैं समझता/समझती हूँ कि झूठा अनुरोध IPC के तहत दंडनीय है।</span>
                        </label>
                    </div>
                </div>

                <div class="text-center">
                    <button type="button" class="btn btn-jd-primary btn-lg px-5" data-bs-toggle="modal" data-bs-target="#verificationModal">
                        Proceed to Verification
                        <span class="d-block small fw-normal opacity-75" style="font-size: 0.9rem;">सत्यापन के लिए आगे बढ़ें</span>
                    </button>
                </div>
            </form>




        </div>
    </div>
</div>

<div class="modal fade frosted-modal" id="verificationModal" tabindex="-1">
    <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content shadow">
            <div class="modal-header border-0 pb-0">
                <div class="text-center w-100">
                    <h5 class="fw-bold text-danger mb-0">Final Verification Before Submitting</h5>
                    <span class="hindi-sub">रक्त अनुरोध सबमिट करने से पहले अंतिम सत्यापन</span>
                </div>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body p-4">
                
                <div class="mb-4">
                    <h6 class="fw-bold"><i class="fa-solid fa-gavel me-2"></i>Legal Accountability (IPC)</h6>
                    <div class="alert alert-danger small py-2">
                        Strict action will be taken for fraudulent uploads. (IPC 420/468).
                        <span class="hindi-sub text-danger">जालसाजी के लिए सख्त कानूनी कार्रवाई की जाएगी।</span>
                    </div>
                </div>

                <h6 class="fw-bold mb-3"><i class="fa-solid fa-hospital-user me-2"></i>Partner Issuance Policies</h6>
                
                <div class="row g-2">
                    <div class="col-md-6">
                        <div class="policy-item">
                            <p class="mb-0 small fw-bold">1. Fixed Processing Fee Only</p>
                            <span class="hindi-sub x-small">केवल निर्धारित प्रोसेसिंग शुल्क लिया जाएगा।</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="policy-item">
                            <p class="mb-0 small fw-bold">2. Mandatory Crossmatch</p>
                            <span class="hindi-sub x-small">क्रॉस-मैच अनिवार्य है।</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="policy-item">
                            <p class="mb-0 small fw-bold">3. Physical Document Verification</p>
                            <span class="hindi-sub x-small">दस्तावेज़ों का भौतिक सत्यापन अनिवार्य।</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="policy-item">
                            <p class="mb-0 small fw-bold">4. Zero 'Donor Replacement' Policy</p>
                            <span class="hindi-sub x-small">पार्टनर 'डोनर लाने' की मांग नहीं कर सकता।</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="policy-item">
                            <p class="mb-0 small fw-bold">5. Hard Copy Letterhead Required</p>
                            <span class="hindi-sub x-small">लेटरहेड की हार्ड कॉपी अनिवार्य।</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="policy-item">
                            <p class="mb-0 small fw-bold">6. Strict Penalty for Overcharging</p>
                            <span class="hindi-sub x-small">अतिरिक्त शुल्क लेने पर कठोर कार्रवाई।</span>
                        </div>
                    </div>
                </div>

                <div class="mt-4 p-3 rounded-4 bg-light text-center small">
                    <p class="mb-0"><strong>WHO/NACO Ethical Note:</strong> Voluntary donation is the foundation of safe blood supply. Exploitation of donors or patients is a crime.
                    <span class="hindi-sub">स्वैच्छिक रक्तदान सुरक्षित रक्त आपूर्ति का आधार है।</span></p>
                </div>

            </div>
            <div class="modal-footer border-0 pt-0 pb-4 justify-content-center gap-3">
                <button class="btn btn-jd-primary px-4 py-2">
                    I Agree & Submit Request
                    <span class="d-block x-small fw-normal">मैं सहमत हूँ और अनुरोध सबमिट करता हूँ</span>
                </button>
                <button class="btn btn-light rounded-pill px-4" data-bs-dismiss="modal">
                    Cancel
                    <span class="d-block x-small text-muted">रद्द करें</span>
                </button>
            </div>
        </div>
    </div>
</div>
</template>