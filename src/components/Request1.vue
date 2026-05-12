
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
<nav class="navbar navbar-expand-lg sticky-top bg-white border-bottom">
    <div class="container">
        <a class="navbar-brand fw-bold text-danger" href="#">
            JeevanDaan<span class="text-dark">+</span>
        </a>
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav mx-auto">
                <li class="nav-item">
                    <router-link class="nav-link" to="/user">Home</router-link>
                </li>
            </ul>
        </div>
    </div>
</nav>

<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-10 col-xl-8">

            <!-- Legal Header — kept as is -->
            <div class="legal-header shadow-sm">
                <div class="d-flex align-items-start gap-3 mb-3">
                    <i class="fa-solid fa-scale-balanced text-danger fs-2"></i>
                    <div>
                        <h5 class="fw-bold text-danger mb-0">
                            Legal Notice: Fake or Forged Blood Requests Are Punishable Under IPC.
                        </h5>
                        <span class="hindi-sub text-danger opacity-75 fw-bold">
                            कानूनी सूचना: झूठे या नकली रक्त अनुरोध IPC के तहत दंडनीय अपराध हैं।
                        </span>
                    </div>
                </div>
                <div class="d-flex flex-wrap gap-2">
                    <div class="ipc-tag">
                        <strong>IPC 419 / 420:</strong> Impersonation, Cheating & Fraud
                        <br><span class="ipc-sub">छद्मवेश, धोखाधड़ी व ठगी</span>
                        <span class="ipc-punish">Punishment: Up to 3–7 years imprisonment + fine</span>
                    </div>
                    <div class="ipc-tag">
                        <strong>IPC 464 / 468:</strong> Forgery of Medical Documents
                        <br><span class="ipc-sub">चिकित्सीय दस्तावेज़ों की जालसाज़ी</span>
                        <span class="ipc-punish">Punishment: Up to 7 years imprisonment</span>
                    </div>
                    <div class="ipc-tag">
                        <strong>IPC 471:</strong> Using Forged Hospital Papers
                        <br><span class="ipc-sub">नकली दस्तावेज़ का उपयोग</span>
                        <span class="ipc-punish">Punishment: Same as forgery (up to 7 years)</span>
                    </div>
                </div>
            </div>

            <!-- Error/Success alerts -->
            <div v-if="error" class="alert alert-danger rounded-4 mb-4">
                <i class="fas fa-exclamation-circle me-2"></i>{{ error }}
            </div>

            <form @submit.prevent="openVerificationModal">

                <!-- Patient Details -->
                <div class="section-card">
                    <h5 class="fw-bold mb-4 border-bottom pb-2">
                        <i class="fa-solid fa-user-injured text-danger me-2"></i>
                        Patient Details
                        <span class="hindi-sub d-inline ms-2 fs-6">मरीज़ का विवरण</span>
                    </h5>
                    <div class="row g-4">
                        <div class="col-md-8">
                            <label class="form-label">Patient Full Name</label>
                            <span class="hindi-sub">मरीज़ का पूरा नाम</span>
                            <input
                                type="text"
                                class="form-control"
                                v-model="form.patient_name"
                                placeholder="Enter full name"
                                required
                            >
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">Age</label>
                            <span class="hindi-sub">आयु</span>
                            <input
                                type="number"
                                class="form-control"
                                v-model="form.patient_age"
                                placeholder="Years"
                                required
                            >
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Required Blood Group</label>
                            <span class="hindi-sub">आवश्यक रक्त समूह</span>
                            <select class="form-select" v-model="form.blood_group" required>
                                <option disabled value="">Select Blood Group</option>
                                <option>A+</option><option>A-</option>
                                <option>B+</option><option>B-</option>
                                <option>O+</option><option>O-</option>
                                <option>AB+</option><option>AB-</option>
                            </select>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Units Required</label>
                            <span class="hindi-sub">यूनिट की संख्या</span>
                            <input
                                type="number"
                                class="form-control"
                                v-model="form.quantity"
                                placeholder="Units"
                                min="1"
                                required
                            >
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Urgency</label>
                            <span class="hindi-sub">अत्यावश्यकता</span>
                            <select class="form-select" v-model="form.urgency" required>
                                <option value="critical">Critical (आपातकाल)</option>
                                <option value="urgent">Urgent (अत्यावश्यक)</option>
                                <option value="normal">Normal (सामान्य)</option>
                            </select>
                        </div>
                        <div class="col-md-12">
                            <label class="form-label">Hospital Name</label>
                            <span class="hindi-sub">अस्पताल का नाम</span>
                            <input
                                type="text"
                                class="form-control"
                                v-model="form.hospital_name"
                                placeholder="Enter Hospital Name"
                                required
                                minlength="3"
                                maxlength="100"
                                pattern="[A-Za-z\s.&'-]{3,100}"
                            >
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">City</label>
                            <span class="hindi-sub">शहर</span>
                            <input
                                type="text"
                                class="form-control"
                                v-model="form.city"
                                placeholder="City"
                                required
                                @input="handleCity"
                                maxlength="50"
                            >
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Doctor's Name</label>
                            <span class="hindi-sub">डॉक्टर का नाम</span>
                            <input
                                type="text"
                                class="form-control"
                                v-model="form.doctor_name"
                                @input="handleDoctorName"
                                placeholder="Dr. Name"
                                required
                                maxlength="60"
                            >
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Doctor's Phone</label>
                            <span class="hindi-sub">डॉक्टर का नंबर</span>
                            <input
                                type="tel"
                                class="form-control"
                                v-model="form.doctor_phone"
                                 @input="handlePhone('doctor_phone')"
                                placeholder="+91XXXXXXXXXX"
                                
                            >
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Attender's Phone</label>
                            <span class="hindi-sub">परिजन का मोबाइल नंबर</span>
                            <input
                                type="tel"
                                class="form-control"
                                v-model="form.attender_phone"
                                @input="handlePhone('attender_phone')"
                                placeholder="+91XXXXXXXXXX"
                                required
                            >
                        </div>
                    </div>
                </div>

                <!-- Attender Details -->
                <div class="section-card">
                    <h5 class="fw-bold mb-4 border-bottom pb-2">
                        Attender Details
                        <span class="hindi-sub d-inline ms-2 fs-6">परिजन का विवरण</span>
                    </h5>
                    <div class="row g-4">
                        <div class="col-md-6">
                            <label class="form-label">Attender Full Name</label>
                            <span class="hindi-sub">परिजन का नाम</span>
                            <input
                                type="text"
                                class="form-control"
                                v-model="form.attender_name"
                                placeholder="Full Name"
                                required
                                maxlength="60"
                            >
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Attender ID Type</label>
                            <span class="hindi-sub">परिजन का पहचान प्रकार</span>
                            <select class="form-select" v-model="form.id_type" required>
                                <option disabled value="">Select ID Type</option>
                                <option>Aadhaar Card</option>
                                <option>Driving License</option>
                                <option>Voter ID</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Attender ID Number</label>
                            <span class="hindi-sub">पहचान पत्र संख्या</span>
                            <input
                                type="text"
                                class="form-control"
                                v-model="form.id_no"
                                placeholder="Enter ID Number"
                                @input="handleIdInput"
                                required
                            >
                        </div>
                    </div>
                </div>

                <!-- Document Upload -->
                <div class="section-card">
                    <h5 class="fw-bold mb-4 border-bottom pb-2">
                        <i class="fa-solid fa-cloud-arrow-up text-danger me-2"></i>
                        Document Upload
                        <span class="hindi-sub d-inline ms-2 fs-6">दस्तावेज़ अपलोड</span>
                    </h5>
                    <div class="row g-3">

                        <!-- Doctor Letterhead -->
                        <div class="col-md-4">
                            <div
                                class="upload-area"
                                :class="uploads.letterhead ? 'border-success' : ''"
                                @click="triggerUpload('letterhead')"
                            >
                                <input
                                    type="file"
                                    ref="letterheadInput"
                                    @change="handleFileChange($event, 'letterhead')"
                                    accept="image/*,application/pdf"
                                    style="display:none" 
                                    required
                                >
                                <div v-if="uploadProgress.letterhead">
                                    <div class="spinner-border spinner-border-sm text-danger mb-2"></div>
                                    <p class="small mb-0">Uploading...</p>
                                </div>
                                <div v-else-if="uploads.letterhead">
                                    <i class="fas fa-check-circle text-success fs-3 mb-2"></i>
                                    <p class="small mb-0 text-success fw-bold">Letterhead Uploaded  </p>
                                </div>
                                <div v-else>
                                    <i class="fa-solid fa-file-signature mb-2 fs-3 text-muted"></i>
                                    <p class="small mb-0 fw-bold">Hospital Letter Head</p>
                                    <span class="hindi-sub x-small">हॉस्पिटल लेटरहेड</span>
                                    <p class="smallest text-muted mt-1">Click to upload</p>
                                </div>
                            </div>
                        </div>

                        <!-- Patient Photo -->
                        <div class="col-md-4">
                            <div
                                class="upload-area"
                                :class="uploads.patient_photo ? 'border-success' : ''"
                                @click="triggerUpload('patient_photo')"
                            >
                                <input
                                    type="file"
                                    ref="patientPhotoInput"
                                    @change="handleFileChange($event, 'patient_photo')"
                                    accept="image/*"
                                    style="display:none"
                                    required
                                >
                                <div v-if="uploadProgress.patient_photo">
                                    <div class="spinner-border spinner-border-sm text-danger mb-2"></div>
                                    <p class="small mb-0">Uploading...</p>
                                </div>
                                <div v-else-if="uploads.patient_photo">
                                    <img
                                        :src="uploads.patient_photo"
                                        class="img-fluid rounded-3 mb-2"
                                        style="height:80px;object-fit:cover"
                                    >
                                    <p class="small mb-0 text-success fw-bold">Photo Uploaded  </p>
                                </div>
                                <div v-else>
                                    <i class="fa-solid fa-camera mb-2 fs-3 text-muted"></i>
                                    <p class="small mb-0 fw-bold">Patient Live Photo</p>
                                    <span class="hindi-sub x-small">मरीज़ की फोटो</span>
                                    <p class="smallest text-muted mt-1">Click to upload</p>
                                </div>
                            </div>
                        </div>

                        <!-- Attender ID Proof -->
                        <div class="col-md-4">
                            <div
                                class="upload-area"
                                :class="uploads.attender_id_proof ? 'border-success' : ''"
                                @click="triggerUpload('attender_id_proof')"
                            >
                                <input
                                    type="file"
                                    ref="attenderIdInput"
                                    @change="handleFileChange($event, 'attender_id_proof')"
                                    accept="image/*,application/pdf"
                                    style="display:none"
                                    required
                                >
                                <div v-if="uploadProgress.attender_id_proof">
                                    <div class="spinner-border spinner-border-sm text-danger mb-2"></div>
                                    <p class="small mb-0">Uploading...</p>
                                </div>
                                <div v-else-if="uploads.attender_id_proof">
                                    <i class="fas fa-check-circle text-success fs-3 mb-2"></i>
                                    <p class="small mb-0 text-success fw-bold">ID Proof Uploaded  </p>
                                </div>
                                <div v-else>
                                    <i class="fa-solid fa-id-card mb-2 fs-3 text-muted"></i>
                                    <p class="small mb-0 fw-bold">Attender ID Proof</p>
                                    <span class="hindi-sub x-small">परिजन का पहचान पत्र</span>
                                    <p class="smallest text-muted mt-1">Click to upload</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Info card — kept as is -->
                <div class="section-card border-start border-danger border-4">
                    <div class="row">
                        <div class="col-md-1 d-none d-md-block text-center pt-2">
                            <i class="fa-solid fa-circle-info text-danger fs-3"></i>
                        </div>
                        <div class="col-md-11">
                            <p class="mb-2">
                                <strong>Crossmatch Required:</strong> Blood is issued only after compatibility check.
                                <span class="hindi-sub">क्रॉस-मैच अनिवार्य।</span>
                            </p>
                            <p class="mb-0">
                                <strong>Processing Fees:</strong> As per government guidelines.
                                <span class="hindi-sub">सरकारी नियमों के अनुसार शुल्क लागू होगा।</span>
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Terms -->
                <div class="section-card">
                    <div class="form-check mb-3">
                        <input
                            class="form-check-input"
                            type="checkbox"
                            id="tc1"
                            v-model="terms.authentic"
                            required
                        >
                        <label class="form-check-label small fw-bold" for="tc1">
                            I confirm all documents are authentic.
                            <span class="hindi-sub fw-normal">मैं पुष्टि करता/करती हूँ कि सभी दस्तावेज़ वास्तविक हैं।</span>
                        </label>
                    </div>
                    <div class="form-check mb-3">
                        <input
                            class="form-check-input"
                            type="checkbox"
                            id="tc2"
                            v-model="terms.legal"
                            required
                        >
                        <label class="form-check-label small fw-bold" for="tc2">
                            I understand fake requests can lead to IPC legal action.
                            <span class="hindi-sub fw-normal">मैं समझता/समझती हूँ कि झूठा अनुरोध IPC के तहत दंडनीय है।</span>
                        </label>
                    </div>
                </div>

                <div class="text-center">
                    <button
                        type="submit"
                        class="btn btn-jd-primary btn-lg px-5"
                        :disabled="!canSubmit"
                    >
                        <span v-if="submitting">
                            <span class="spinner-border spinner-border-sm me-2"></span>
                            Submitting...
                        </span>
                        <span v-else>
                            Proceed to Verification
                            <span class="d-block small fw-normal opacity-75">
                                सत्यापन के लिए आगे बढ़ें
                            </span>
                        </span>
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Verification Modal — kept as is + submit button wired -->
<div class="modal fade frosted-modal" id="verificationModal" tabindex="-1">
    <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content shadow">
            <div class="modal-header border-0 pb-0">
                <div class="text-center w-100">
                    <h5 class="fw-bold text-danger mb-0">
                        Final Verification Before Submitting
                    </h5>
                    <span class="hindi-sub">रक्त अनुरोध सबमिट करने से पहले अंतिम सत्यापन</span>
                </div>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body p-4">
                <div class="mb-4">
                    <h6 class="fw-bold">
                        <i class="fa-solid fa-gavel me-2"></i>Legal Accountability (IPC)
                    </h6>
                    <div class="alert alert-danger small py-2">
                        Strict action will be taken for fraudulent uploads. (IPC 420/468).
                        <span class="hindi-sub text-danger">जालसाजी के लिए सख्त कानूनी कार्रवाई की जाएगी।</span>
                    </div>
                </div>

                <h6 class="fw-bold mb-3">
                    <i class="fa-solid fa-hospital-user me-2"></i>Partner Issuance Policies
                </h6>
                <div class="row g-2">
                    <div class="col-md-6">
                        <div class="policy-item">
                            <p class="mb-0 small fw-bold">1. Fixed Processing Fee Only</p>
                            <span class="hindi-sub x-small">केवल निर्धारित प्रोसेसिंग शुल्क।</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="policy-item">
                            <p class="mb-0 small fw-bold">2. Mandatory Crossmatch</p>
                            <span class="hindi-sub x-small">क्रॉस-मैच अनिवार्य।</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="policy-item">
                            <p class="mb-0 small fw-bold">3. Physical Document Verification</p>
                            <span class="hindi-sub x-small">दस्तावेज़ों का भौतिक सत्यापन।</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="policy-item">
                            <p class="mb-0 small fw-bold">4. Zero 'Donor Replacement' Policy</p>
                            <span class="hindi-sub x-small">डोनर लाने की मांग नहीं।</span>
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
                            <span class="hindi-sub x-small">अतिरिक्त शुल्क पर कठोर कार्रवाई।</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-footer border-0 pt-0 pb-4 justify-content-center gap-3">
                <button
                    class="btn btn-jd-primary px-4 py-2"
                    @click="submitRequest"
                    :disabled="submitting"
                >
                    <span v-if="submitting">
                        <span class="spinner-border spinner-border-sm me-2"></span>
                        Submitting...
                    </span>
                    <span v-else>
                        I Agree & Submit Request
                        <span class="d-block x-small fw-normal">
                            मैं सहमत हूँ और अनुरोध सबमिट करता हूँ
                        </span>
                    </span>
                </button>
                <button
                    class="btn btn-light rounded-pill px-4"
                    data-bs-dismiss="modal"
                    id="closeModalBtn"
                >
                    Cancel
                </button>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import api from '@/api/index.js'
import { uploadToCloudinary } from '@/utils/cloudinary.js'

export default {
    name: 'UserRequest',

    data() {
        return {
            submitting: false,
            error: null,

            // Form data
            form: {
                patient_name: '',
                patient_age: '',
                blood_group: '',
                quantity: 1,
                urgency: 'normal',
                hospital_name: '',
                city: '',
                doctor_name: '',
                doctor_phone: '',
                attender_name: '',
                attender_phone: '',
                id_type: 'Aadhaar Card',
                id_no: '',
                // Cloudinary URLs — filled after upload
                doctor_letterhead: '',
                patient_photo: '',
                attender_id_proof: '',
            },

            // Upload state
            uploads: {
                letterhead: null,
                patient_photo: null,
                attender_id_proof: null,
            },

            uploadProgress: {
                letterhead: false,
                patient_photo: false,
                attender_id_proof: false,
            },

            // Terms
            terms: {
                authentic: false,
                legal: false,
            }
        }
    },

    computed: {
        canSubmit() {
            return (
                this.terms.authentic &&
                this.terms.legal &&
                this.uploads.letterhead &&
                this.uploads.patient_photo &&
                !this.submitting
            )
        }
    },

    methods: {
        // ── Trigger file input ───────────────────
        triggerUpload(type) {
            const refs = {
                letterhead: 'letterheadInput',
                patient_photo: 'patientPhotoInput',
                attender_id_proof: 'attenderIdInput',
            }
            this.$refs[refs[type]].click()
        },

        // ── Handle file change + upload ──────────
        async handleFileChange(event, type) {
            const file = event.target.files[0]
            if (!file) return

            this.uploadProgress[type] = true

            try {
                const url = await uploadToCloudinary(file, `jeevandaan/${type}`)
                this.uploads[type] = url

                // Map to form fields
                if (type === 'letterhead') this.form.doctor_letterhead = url
                if (type === 'patient_photo') this.form.patient_photo = url
                if (type === 'attender_id_proof') this.form.attender_id_proof = url

                console.log(`${type} uploaded:`, url)
            } catch (err) {
                this.error = `Failed to upload ${type}. Please try again.`
                console.error(err)
            } finally {
                this.uploadProgress[type] = false
            }
        },

        // ── Open verification modal ──────────────
        openVerificationModal() {
            if (!this.canSubmit) {
                this.error = 'Please fill all required fields, upload documents and accept terms.'
                return
            }
            this.error = null
            // Open Bootstrap modal
            const modal = new window.bootstrap.Modal(
                document.getElementById('verificationModal')
            )
            modal.show()
        },

        // ── Submit request ────────────────────────
        async submitRequest() {
            this.submitting = true
            this.error = null

            try {

                // Id validation
                if (!this.form.id_type) {
        throw new Error("Please select ID type");
      }

      // ID Number validation (based on type)
      let idRegex;

      switch (this.form.id_type) {
  case "Aadhaar Card":
    idRegex = /^\d{12}$/;
    break;

  case "Voter ID":
    idRegex = /^[A-Z]{3}\d{7}$/;
    break;

  case "Driving License":
    idRegex = /^[A-Z0-9]{8,16}$/;
    break;
}

      if (!idRegex.test(this.form.id_no)) {
        throw new Error("Invalid ID number");
      }

                // FRONTEND VALIDATION (FIRST STEP)
               const phoneRegex = /^[6-9]\d{9}$/;

               if (!this.form.hospital_name.trim()) {
              throw new Error("Hospital name is required");
               }

              if (!this.form.city.trim()) {
               throw new Error("City is required");
               }

             if (!this.form.doctor_name.trim()) {
               throw new Error("Doctor name is required");
               }

              if (!phoneRegex.test(this.form.attender_phone)) {
             throw new Error("Invalid attender phone number");
           }

           if (this.form.doctor_phone && !phoneRegex.test(this.form.doctor_phone)) {
             throw new Error("Invalid doctor phone number");
             }

               
                const token = localStorage.getItem('access_token')
                if (!token) {
                    this.$router.push('/login')
                    return
                }

                const response = await api.post(
                    'https://api.jeevandaan.online/api/requests/attender/create/',
                    this.form
                )

                // Close modal
                document.getElementById('closeModalBtn').click()

                // Redirect to success page with reference ID
                this.$router.push({
                    name: 'RequestSuccess',
                    query: {
                        ref: response.data.reference_id,
                        blood_group: this.form.blood_group,
                        city: this.form.city
                    }
                })

            } catch (err) {
                if (err.response?.data) {
                    const errors = err.response.data
                    const firstError = Object.values(errors)[0]
                    this.error = Array.isArray(firstError)
                        ? firstError[0]
                        : firstError
                } else {
                    this.error = 'Something went wrong. Please try again.'
                }
                console.error(err)
            } finally {
                this.submitting = false
            }
        },

        // Form-handlers

        handleCity() {
  this.form.city = this.form.city
    .replace(/[^\p{L}\s]/gu, '')
    .replace(/\s{2,}/g, ' ')
    .slice(0, 50);

},
handleDoctorName() {
  this.form.doctor_name = this.form.doctor_name
    .replace(/[^\p{L}\s.'-]/gu, '')
    .replace(/\s{2,}/g, ' ')
    .slice(0, 60);
},
handlePhone(field) {
  let val = this.form[field].replace(/\D/g, '');

  // Indian number must be 10 digits
  if (val.length > 10) val = val.slice(0, 10);

  this.form[field] = val;
},
handleIdInput() {
  let val = this.form.id_no.toUpperCase();

  if (this.form.id_type === "Aadhaar Card") {
    // Only digits, max 12
    val = val.replace(/\D/g, '').slice(0, 12);
  } 
  else if (this.form.id_type === "Voter ID") {
    // Format: ABC1234567
    val = val.replace(/[^A-Z0-9]/g, '').slice(0, 10);
  } 
  else if (this.form.id_type === "Driving License") {
    // DL is alphanumeric (state + digits)
    val = val.replace(/[^A-Z0-9]/g, '').slice(0, 16);
  }

  this.form.id_no = val;
}
    }
}
</script>