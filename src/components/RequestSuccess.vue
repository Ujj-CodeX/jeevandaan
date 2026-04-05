<template>
  <div class="min-vh-100 bg-light py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8">

          <!-- Success card -->
          <div class="card border-0 shadow-sm rounded-4 p-5 text-center mb-4">
            <div class="success-icon mx-auto mb-4">
              <i class="fas fa-check-circle text-success" style="font-size:4rem"></i>
            </div>
            <h3 class="fw-bold text-success mb-2">Request Raised Successfully!  </h3>
            <p class="text-muted mb-4">
              Your blood request has been submitted. Share your reference ID at the blood bank.
            </p>

            <!-- Reference ID -->
            <div class="ref-box p-4 rounded-4 mb-4"
              style="background:linear-gradient(135deg,#fff5f5,#ffe0e0)">
              <small class="text-muted d-block mb-2 fw-bold text-uppercase">
                Your Reference ID
              </small>
              <h4 class="fw-800 text-danger mb-2 text-break">{{ referenceId }}</h4>
              <button class="btn btn-sm btn-outline-danger rounded-pill px-3"
                @click="copyRefId">
                <i class="fas fa-copy me-1"></i>
                {{ copied ? 'Copied!' : 'Copy ID' }}
              </button>
            </div>

            <div class="alert bg-warning bg-opacity-10 border-0 rounded-4 text-start small">
              <i class="fas fa-info-circle text-warning me-2"></i>
              <strong>Important:</strong> Show this reference ID + your original ID proof
              at the blood bank for verification.
            </div>
          </div>

          <!-- Nearest partners -->
          <div class="card border-0 shadow-sm rounded-4 p-4">
            <h5 class="fw-bold mb-1">
              <i class="fas fa-map-marker-alt text-danger me-2"></i>
              Nearest Blood Banks
            </h5>
            <p class="text-muted small mb-4">
              Based on your location — showing banks with
              <strong class="text-danger">{{ bloodGroup }}</strong> stock
            </p>

            <!-- Loading -->
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-danger mb-2"></div>
              <p class="text-muted small">Finding nearest blood banks...</p>
            </div>

            <!-- Empty -->
            <div v-else-if="partners.length === 0" class="text-center py-4">
              <i class="fas fa-hospital-slash text-muted fa-3x mb-3"></i>
              <h6 class="fw-bold">No Blood Banks Found Nearby</h6>
              <p class="text-muted small">
                No verified partners found within 20km with
                {{ bloodGroup }} blood.
              </p>
              <button
                class="btn btn-outline-danger rounded-pill px-4 mt-2"
                @click="fetchNearbyPartners(50)"
              >
                Search wider area (50km)
              </button>
            </div>

            <!-- Partners list -->
            <div v-else>
              <div
                v-for="partner in partners"
                :key="partner.id"
                class="partner-card p-3 mb-3 rounded-4 border"
                :class="partner.available_units > 5
                  ? 'border-success'
                  : partner.available_units > 0
                  ? 'border-warning'
                  : 'border-danger'"
              >
                <div class="row align-items-center">
                  <div class="col-md-6">
                    <div class="d-flex align-items-center gap-3">
                      <div class="partner-icon">
                        <i class="fas fa-hospital text-danger"></i>
                      </div>
                      <div>
                        <h6 class="fw-bold mb-0">{{ partner.hospital_name }}</h6>
                        <small class="text-muted">
                          {{ partner.partner_type === 'blood_bank'
                            ? '🏦 Blood Bank'
                            : partner.partner_type === 'government'
                            ? '🏛️ Govt Hospital'
                            : '🏥 Private Hospital'
                          }}
                        </small>
                      </div>
                    </div>
                  </div>

                  <div class="col-md-3 mt-2 mt-md-0">
                    <small class="text-muted d-block">
                      <i class="fas fa-route me-1 text-danger"></i>
                      {{ partner.distance_km }} km away
                    </small>
                    <small class="text-muted d-block">
                      <i class="fas fa-map-marker-alt me-1 text-danger"></i>
                      {{ partner.city }}
                    </small>
                    <small class="text-muted d-block">
                      <i class="fas fa-phone me-1 text-danger"></i>
                      {{ partner.contact }}
                    </small>
                  </div>

                  <div class="col-md-3 mt-2 mt-md-0 text-md-end">
                    <!-- Stock badge -->
                    <span :class="['badge rounded-pill px-3 py-2 mb-2 d-block',
                      partner.available_units > 5 ? 'bg-success'
                      : partner.available_units > 0 ? 'bg-warning text-dark'
                      : 'bg-danger']"
                    >
                      {{ bloodGroup }}:
                      {{ partner.available_units[bloodGroup] > 0
                        ? `${partner.available_units[bloodGroup]} units`
                        : 'No stock' }}
                    </span>

                    <!-- Fee -->
                    <small class="text-muted d-block mb-2">
                      Fee: <strong>₹{{ partner.convenience_fee || 0 }}</strong>
                    </small>

                    <!-- Verified badge -->
                    <span class="badge bg-success-subtle text-success rounded-pill small">
                      ✓ Verified
                    </span>
                  </div>
                </div>

                <!-- Address -->
                <div class="mt-2 pt-2 border-top">
                  <small class="text-muted">
                    <i class="fas fa-location-dot me-1 text-danger"></i>
                    {{ partner.address }}
                  </small>
                </div>
              </div>
            </div>

          </div>

          

          <!-- Back to dashboard -->
          <div class="text-center mt-4">
            <router-link to="/user" class="btn btn-danger rounded-pill px-5 py-3 fw-bold">
              <i class="fas fa-home me-2"></i> Back to Dashboard
            </router-link>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api/index.js'

export default {
    name: 'RequestSuccess',

    data() {
        return {
            referenceId: '',
            bloodGroup: '',
            city: '',
            partners: [],
            loading: true,
            copied: false,
        }
    },

    mounted() {
        this.referenceId = this.$route.query.ref || ''
        this.bloodGroup = this.$route.query.blood_group || ''
        this.city = this.$route.query.city || ''
        this.fetchNearbyPartners(20)
    },

    methods: {
        async fetchNearbyPartners(radius = 20) {
            this.loading = true
            try {
                // Try GPS first
                const coords = await this.getCoordinates()
                 const lat = coords?.lat || ''
                const lng = coords?.lng || ''
                const bg = encodeURIComponent(this.bloodGroup)

                let url = `/api/partners/nearby/?blood_group=${bg}&radius=${radius}`
                if (lat && lng) {
                    url += `&lat=${lat}&lng=${lng}`
                } else {
                    // Fallback to city search
                    url = `/api/partners/list/?city=${this.city}&blood_group=${bg}`
                }

                const response = await api.get(url)
                this.partners = Array.isArray(response.data) ? response.data : []
                

            } catch (err) {
                console.error(err)
                this.partners = []
            } finally {
                this.loading = false
            }
        },

        getCoordinates() {
            return new Promise((resolve) => {
                if (!navigator.geolocation) {
                    resolve(null)
                    return
                }
                navigator.geolocation.getCurrentPosition(
                    pos => resolve({
                        lat: pos.coords.latitude,
                        lng: pos.coords.longitude
                    }),
                    () => resolve(null)
                )
            })
        },

        copyRefId() {
            navigator.clipboard.writeText(this.referenceId)
            this.copied = true
            setTimeout(() => { this.copied = false }, 2000)
        }
    }
}
</script>

<style scoped>
.fw-800 { font-weight: 800; }
.partner-icon {
    width: 45px;
    height: 45px;
    background: #fff5f5;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.partner-card {
    transition: all 0.2s ease;
}
.partner-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.05) !important;
}
.ref-box {
    border: 2px dashed #E63946;
}
</style>