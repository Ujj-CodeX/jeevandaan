<template>
  <div class="jeevandaan-detail-page bg-light">
    <nav class="navbar sticky-top bg-white shadow-sm py-2">
      <div class="container d-flex justify-content-between align-items-center">
        <span class="fw-bold text-jd-red">
            <img 
    src="@/assets/L1.png" 
    alt="JeevanDaan Logo" 
    width="32" 
    height="32" 
    class="me-2 d-inline-block align-top logo-icon"
  >
            JeevanDaan+ <small class="text-muted">| Protocol</small></span>
        <div class="d-flex align-items-center gap-3">
          <div class="btn-group btn-group-sm">
            <button @click="lang = 'en'" :class="['btn', lang === 'en' ? 'btn-danger' : 'btn-outline-danger']">English</button>
            <button @click="lang = 'hi'" :class="['btn', lang === 'hi' ? 'btn-danger' : 'btn-outline-danger']">हिन्दी</button>
          </div>
        </div>
      </div>
    </nav>

    <section class="container my-5">
      <div class="card border-0 shadow-lg overflow-hidden">
        <div class="row g-0">
          <div class="col-md-4 bg-jd-red text-white p-5 d-flex flex-column justify-content-center">
            <i class="fas fa-ambulance fa-4x mb-4"></i>
            <h2 class="display-6 fw-bold">{{ t.attender.title }}</h2>
            <p class="opacity-75">{{ t.attender.subtitle }}</p>
          </div>
          <div class="col-md-8 p-5 bg-white">
            <h4 class="text-jd-red border-bottom pb-2 mb-4">{{ t.attender.flowTitle }}</h4>
            
            <div class="d-flex mb-4">
              <div class="step-num-circle">1</div>
              <div>
                <h5 class="fw-bold">{{ t.attender.step1T }}</h5>
                <p class="text-muted">{{ t.attender.step1D }}</p>
                <div class="ref-box mt-2">
                  <span class="badge bg-dark">REF: JD-2026-XXXX</span> 
                  <small class="ms-2 text-jd-red fw-bold">← {{ t.attender.refNotice }}</small>
                </div>
              </div>
            </div>

            <div class="d-flex mb-4">
              <div class="step-num-circle">2</div>
              <div>
                <h5 class="fw-bold">{{ t.attender.step2T }}</h5>
                <p class="text-muted">{{ t.attender.step2D }}</p>
                <span class="badge bg-success-subtle text-success border border-success">{{ t.attender.govtRate }}</span>
              </div>
            </div>

            <div class="d-flex">
              <div class="step-num-circle bg-warning text-dark border-0">!</div>
              <div class="policy-alert p-3 rounded-3 w-100">
                <h5 class="fw-bold text-danger"><i class="fas fa-ban me-2"></i>{{ t.attender.noPressureT }}</h5>
                <p class="mb-0 small text-dark fw-medium">{{ t.attender.noPressureD }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="container my-5">
      <div class="row g-4">
        <div class="col-lg-12 text-center mb-3">
          <h2 class="fw-bold">{{ t.donor.sectionTitle }}</h2>
          <p class="text-muted">{{ t.donor.sectionSub }}</p>
        </div>
        <div class="col-md-6">
          <div class="card h-100 border-0 shadow-sm p-4">
            <h4 class="text-success mb-3"><i class="fas fa-user-secret me-2"></i>{{ t.donor.privacyT }}</h4>
            <ul class="list-group list-group-flush">
              <li class="list-group-item px-0 border-0 py-3">
                <i class="fas fa-shield-virus text-success me-2"></i> <strong>{{ t.donor.p1T }}</strong> {{ t.donor.p1D }}
              </li>
              <li class="list-group-item px-0 border-0 py-3">
                <i class="fas fa-phone-slash text-success me-2"></i> <strong>{{ t.donor.p2T }}</strong> {{ t.donor.p2D }}
              </li>
            </ul>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card h-100 border-0 shadow-sm p-4 bg-jd-dark text-white">
            <h4><i class="fas fa-certificate text-warning me-2"></i>{{ t.donor.benefitT }}</h4>
            <p class="small opacity-75 mt-3">{{ t.donor.benefitD }}</p>
            <div class="mt-4 pt-3 border-top border-secondary">
              <small class="text-warning fw-bold">{{ t.donor.legalNotice }}</small>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="container my-5 pb-5">
      <div class="card bg-white border-0 shadow-lg p-5">
        <h2 class="text-center mb-5 fw-bold">{{ t.partner.title }}</h2>
        <div class="row text-center g-4">
          <div class="col-md-4">
            <div class="partner-icon-box mb-3"><i class="fas fa-id-check"></i></div>
            <h5>{{ t.partner.verifyT }}</h5>
            <p class="small text-muted">{{ t.partner.verifyD }}</p>
          </div>
          <div class="col-md-4">
            <div class="partner-icon-box mb-3 bg-jd-red text-white"><i class="fas fa-campground"></i></div>
            <h5>{{ t.partner.campT }}</h5>
            <p class="small text-muted">{{ t.partner.campD }}</p>
          </div>
          <div class="col-md-4">
            <div class="partner-icon-box mb-3"><i class="fas fa-hand-holding-heart"></i></div>
            <h5>{{ t.partner.noAskT }}</h5>
            <p class="small text-muted">{{ t.partner.noAskD }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      lang: 'en',
      content: {
        en: {
          attender: {
            title: "Attender & Needy", subtitle: "Getting blood without the stress of hunting donors.",
            flowTitle: "Verified Execution Flow",
            step1T: "Digital Request & Reference ID", step1D: "Fill your requirements. Our system generates a unique Reference Number instantly.",
            refNotice: "Show this at the Center",
            step2T: "Fixed Processing Fee", step2D: "Pay only the fixed testing/processing fee per unit. No donation of money for blood.",
            govtRate: "Government Mandated Rates Only",
            noPressureT: "The 'No-Replacement' Law", noPressureD: "Partners/Banks cannot force you to bring a donor to get blood. All stock is managed by JeevanDaan+ via regular volunteer camps."
          },
          donor: {
            sectionTitle: "Donor Privacy & Ethics", sectionSub: "Your identity is your power, and we keep it safe.",
            privacyT: "Data Protection Protocol",
            p1T: "Identity Cloaking:", p1D: "Your name is only visible as 'Verified Hero' to the seeker.",
            p2T: "Direct Call Shield:", p2D: "Seekers can only contact you through the app's secure bridge.",
            benefitT: "Impact & Reliability", benefitD: "Every donation earns you Life-Points and a digital certificate recognized by partners.",
            legalNotice: "We strictly follow HIPAA & NBTC Privacy Standards."
          },
          partner: {
            title: "Partner & Bank Execution",
            verifyT: "Reference Verification", verifyD: "Partners verify your data using the JD-Ref ID to ensure accuracy.",
            campT: "Regular Camp Refilling", campD: "We refill bank stocks through organized volunteer camps, not patient replacements.",
            noAskT: "Zero Ask Policy", noAskD: "Hospitals are forbidden from asking attenders for blood replacements."
          }
        },
        hi: {
          attender: {
            title: "तीमारदार और जरूरतमंद", subtitle: "डोनर्स ढूंढने के तनाव के बिना रक्त प्राप्त करें।",
            flowTitle: "सत्यापित कार्य प्रक्रिया",
            step1T: "डिजिटल अनुरोध और रेफरेंस आईडी", step1D: "अपनी आवश्यकताएं भरें। हमारा सिस्टम तुरंत एक यूनिक रेफरेंस नंबर बनाता है।",
            refNotice: "इसे केंद्र पर दिखाएं",
            step2T: "निश्चित प्रोसेसिंग शुल्क", step2D: "प्रति यूनिट केवल निश्चित परीक्षण/प्रोसेसिंग शुल्क का भुगतान करें। रक्त के लिए कोई अतिरिक्त पैसा नहीं।",
            govtRate: "केवल सरकारी निर्धारित दरें",
            noPressureT: "'नो-रिप्लेसमेंट' कानून", noPressureD: "पार्टनर/बैंक आपको रक्त प्राप्त करने के लिए डोनर लाने के लिए मजबूर नहीं कर सकते। सभी स्टॉक जीवनदान+ द्वारा नियमित स्वयंसेवी शिविरों के माध्यम से प्रबंधित किया जाता है।"
          },
          donor: {
            sectionTitle: "दाता गोपनीयता और नैतिकता", sectionSub: "आपकी पहचान आपकी शक्ति है, और हम इसे सुरक्षित रखते हैं।",
            privacyT: "डेटा सुरक्षा प्रोटोकॉल",
            p1T: "पहचान छुपाना:", p1D: "आपका नाम चाहने वाले को केवल 'सत्यापित हीरो' के रूप में दिखाई देता है।",
            p2T: "डायरेक्ट कॉल शील्ड:", p2D: "चाहने वाले केवल ऐप के सुरक्षित ब्रिज के माध्यम से आपसे संपर्क कर सकते हैं।",
            benefitT: "प्रभाव और विश्वसनीयता", benefitD: "हर डोनेशन पर आपको 'लाइफ-पॉइंट्स' और पार्टनर्स द्वारा मान्यता प्राप्त डिजिटल प्रमाणपत्र मिलता है।",
            legalNotice: "हम HIPAA और NBTC गोपनीयता मानकों का सख्ती से पालन करते हैं।"
          },
          partner: {
            title: "पार्टनर और बैंक निष्पादन",
            verifyT: "रेफरेंस सत्यापन", verifyD: "पार्टनर सटीकता सुनिश्चित करने के लिए JD-Ref ID का उपयोग करके आपके डेटा को सत्यापित करते हैं।",
            campT: "नियमित कैंप रिफिलिंग", campD: "हम मरीज के बदले (Replacement) के बजाय संगठित स्वयंसेवी शिविरों के माध्यम से बैंक स्टॉक भरते हैं।",
            noAskT: "जीरो आस्क पॉलिसी", noAskD: "अस्पतालों को तीमारदारों से ब्लड रिप्लेसमेंट मांगने की सख्त मनाही है।"
          }
        }
      }
    };
  },
  computed: { t() { return this.content[this.lang]; } }
}
</script>

<style scoped>
.text-jd-red { color: #D32F2F; }
.bg-jd-red { background: #D32F2F; }
.bg-jd-dark { background: #1a1a1a; }

.step-num-circle {
  width: 35px; height: 35px; border: 2px solid #D32F2F; color: #D32F2F;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-weight: bold; margin-right: 20px; flex-shrink: 0;
}

.ref-box { background: #f8f9fa; border: 1px dashed #ccc; padding: 10px; border-radius: 8px; }
.policy-alert { background: #fff8e1; border-left: 5px solid #ffc107; }

.partner-icon-box {
  width: 70px; height: 70px; background: #eee; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto; font-size: 1.8rem; color: #D32F2F;
}

.navbar { border-bottom: 2px solid #D32F2F; }
</style>