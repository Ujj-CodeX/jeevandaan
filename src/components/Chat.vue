<template>
  <div class="min-vh-100 d-flex flex-column" style="background:#f8f9fa">

    <!-- Navbar -->
    <nav class="navbar bg-white border-bottom px-4 py-3 sticky-top shadow-sm">
      <div class="d-flex align-items-center gap-3 w-100">
        <button class="btn btn-light rounded-circle" @click="$router.back()">
          <i class="fas fa-arrow-left"></i>
        </button>
        <div class="flex-grow-1">
          <h6 class="fw-bold mb-0">
            {{ requestInfo?.hospital_name || 'Blood Bank Chat' }}
          </h6>
          <small class="text-muted">
            <span class="badge rounded-pill me-1"
              :class="requestInfo?.status === 'assigned' ? 'bg-success' : 'bg-warning text-dark'">
              {{ requestInfo?.status }}
            </span>
            {{ requestInfo?.blood_group }} — {{ requestInfo?.quantity }} units
          </small>
        </div>
        <!-- Who am I indicator -->
        <span class="badge rounded-pill px-3 py-2"
          :class="userType === 'donor' ? 'bg-danger' : 'bg-primary'">
          {{ userType === 'donor' ? '🩸 Donor' : '🏥 Partner' }}
        </span>
      </div>
    </nav>

    <!-- OTP Banner — shown to both donor and partner -->
    <div v-if="otpCode && userType === 'donor'" class="container pt-3">
      <div class="alert border-0 rounded-4 text-center shadow-sm"
        style="background: linear-gradient(135deg, #fff5f5, #ffe0e0)">
        <small class="text-muted d-block mb-1 fw-bold text-uppercase">
          {{ userType === 'donor' ? 'Your Verification Code' : 'Donor Verification Code' }}
        </small>
        <h2 class="fw-800 text-danger mb-1 display-5 letter-spacing">
          {{ otpCode }}
        </h2>
        <small class="text-muted">
          {{ userType === 'donor'
            ? '🔐 Show this code at the blood bank counter'
            : '🔐 Ask donor for this code to verify identity'
          }}
        </small>
      </div>
    </div>

    <!-- Chat messages area -->
    <div class="flex-grow-1 container py-3 chat-scroll" ref="chatContainer">

      <!-- Cancel section — donor only -->
<div v-if="userType === 'donor'  " class="bg-white border-top p-3">
    <div class="container">
        <button
            class="btn btn-outline-secondary btn-sm rounded-pill w-100"
            @click="showCancelModal = true"
        >
            <i class="fas fa-times me-1"></i> Cancel Acceptance
        </button>
    </div>
</div>

<!-- Cancel Modal -->


      <!-- Loading -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-danger"></div>
        <p class="text-muted mt-2 small">Loading chat...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="messages.length === 0" class="text-center py-5 text-muted">
        <i class="fas fa-comments fa-3x mb-3 opacity-25"></i>
        <p class="fw-bold">No messages yet</p>
        <small>Send a status update below</small>
      </div>

      <!-- Messages -->
      <div v-else>
        <div v-for="msg in messages" :key="msg.id" class="mb-3">

          <!-- System OTP message — full width centered -->
          <div v-if="msg.sender_type === 'system'" class="text-center my-3">
            <div class="d-inline-block px-4 py-3 rounded-4 shadow-sm"
              style="background: linear-gradient(135deg, #fff5f5, #ffe0e0); max-width:320px">
              <i class="fas fa-shield-alt text-danger mb-2 d-block fs-4"></i>
              <p class="fw-bold mb-1 text-danger small">Donor Verification OTP</p>
              <h3 class="fw-800 text-danger mb-1">{{ msg.otp_code }}</h3>
              <small class="text-muted">
                {{ userType === 'donor'
                  ? 'Show this at the blood bank counter'
                  : 'Ask donor to show this code'
                }}
              </small>
              <div class="mt-2">
                <small class="text-muted smallest">
                  <i class="fas fa-clock me-1"></i>{{ timeAgo(msg.sent_at) }}
                </small>
              </div>
            </div>
          </div>

          <!-- Normal messages -->
          <div v-else
            :class="['d-flex mb-2', isMyMessage(msg) ? 'justify-content-end' : 'justify-content-start']">

            <!-- Sender label -->
            <div :class="['d-flex flex-column', isMyMessage(msg) ? 'align-items-end' : 'align-items-start']">
              <small class="text-muted smallest mb-1 px-2">
                {{ isMyMessage(msg)
                  ? 'You'
                  : msg.sender_type === 'donor' ? '🩸 Donor' : '🏥 Bank'
                }}
              </small>
              <div :class="['chat-bubble px-3 py-2 rounded-4 shadow-sm',
                isMyMessage(msg) ? 'bubble-mine' : 'bubble-theirs']">
                <p class="mb-0 fw-bold small">{{ formatMessage(msg.message) }}</p>
                <small class="opacity-75 smallest">{{ timeAgo(msg.sent_at) }}</small>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <div v-if="showCancelModal" class="modal-overlay" @click.self="showCancelModal = false">
    <div class="bg-white rounded-4 shadow-lg p-4" style="max-width:440px;width:100%">
        <h5 class="fw-bold mb-1 text-danger">Cancel Acceptance</h5>
        <p class="text-muted small mb-4">
            Please provide a valid reason. Your reliability score will be deducted by 10 points.
        </p>

        <!-- IPC warning if multiple cancellations -->
        <div v-if="donor?.cancellation_count >= 2"
            class="alert border-0 rounded-4 mb-3 p-3"
            style="background:#fff5f5">
            <i class="fas fa-gavel text-danger me-2"></i>
            <strong class="text-danger small">Legal Notice</strong>
            <p class="text-danger small mb-0 mt-1">
                Multiple cancellations after accepting requests may invite disciplinary
                action under IPC provisions. Your account may be suspended.
            </p>
        </div>

        <div class="mb-3">
            <label class="small fw-bold text-muted">Reason for cancellation *</label>
            <select class="form-select mb-2" v-model="cancelReason">
                <option disabled value="">Select reason</option>
                <option value="health_issue">Health issue / Not feeling well</option>
                <option value="emergency">Personal emergency</option>
                <option value="transport">Transport issue</option>
                <option value="wrong_blood_group">Wrong blood group request</option>
                <option value="other">Other</option>
            </select>
            <textarea
                class="form-control"
                rows="3"
                v-model="cancelDetail"
                placeholder="Additional details (optional)"
            ></textarea>
        </div>

        <!-- Error -->
        <div v-if="cancelError" class="alert alert-danger border-0 rounded-4 small mb-3">
            {{ cancelError }}
        </div>

        <div class="d-flex gap-2">
            <button
                class="btn btn-danger flex-grow-1 py-3 fw-bold rounded-3"
                @click="cancelAcceptance"
                :disabled="cancelling || !cancelReason"
            >
                <span v-if="cancelling">
                    <span class="spinner-border spinner-border-sm me-2"></span>
                </span>
                <span v-else>Submit & Cancel</span>
            </button>
            <button
                class="btn btn-light flex-grow-1 py-3 rounded-3"
                @click="showCancelModal = false"
            >
                Go Back
            </button>
        </div>
    </div>
</div>

    <!-- Default message buttons — fixed at bottom -->
    <div class="bg-white border-top p-3 shadow-sm">
      <div class="container">
        <p class="text-muted smallest mb-2 fw-bold text-uppercase">
          Send Status Update:
        </p>
        <div class="d-flex flex-wrap gap-2">
          <button
            v-for="msg in availableMessages"
            :key="msg.value"
            :class="['btn btn-sm rounded-pill fw-bold',
              msg.value === 'unable_to_come' ? 'btn-outline-secondary' : 'btn-outline-danger']"
            @click="sendMessage(msg.value)"
            :disabled="sending"
          >
            <span v-if="sending && sendingMsg === msg.value">
              <span class="spinner-border spinner-border-sm me-1"></span>
            </span>
            {{ msg.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Rating section — shown after donation fulfilled -->
<div v-if="showDonorRating" class="container pb-4">
    <div class="card border-0 shadow-sm rounded-4 p-4">
        <h6 class="fw-bold mb-3 text-center">
            🎉 Donation Complete! Rate your experience
        </h6>

        <!-- Stars -->
        <div class="d-flex justify-content-center gap-2 mb-3">
            <button
                v-for="star in 5"
                :key="star"
                type="button"
                class="btn p-0 fs-3"
                @click="donorRatingForm.stars = star"
            >
                <i :class="['fas fa-star',
                    star <= donorRatingForm.stars ? 'text-warning' : 'text-muted']">
                </i>
            </button>
        </div>

        <textarea
            class="form-control border-0 bg-light mb-3"
            rows="2"
            v-model="donorRatingForm.review"
            placeholder="How was your experience? (optional)">
        </textarea>

        <div v-if="donorRatingError"
            class="alert alert-danger border-0 rounded-4 small mb-2">
            {{ donorRatingError }}
        </div>

        <button
            class="btn btn-danger w-100 py-3 fw-bold rounded-4"
            @click="submitDonorRating"
            :disabled="submittingDonorRating || !donorRatingForm.stars"
        >
            <span v-if="submittingDonorRating">
                <span class="spinner-border spinner-border-sm me-2"></span>
            </span>
            <span v-else>Submit Rating</span>
        </button>

        <button class="btn btn-link text-muted small w-100 mt-1"
            @click="showDonorRating = false">
            Skip for now
        </button>
    </div>
</div>



  </div>
</template>

<script>
import api from '@/api/index.js'

export default {
  name: 'Chat',

  data() {
    return {
      requestId: null,
      requestInfo: null,
      messages: [],
      loading: true,
      sending: false,
      sendingMsg: null,
      otpCode: null,
      userType: null,    // 'donor' or 'partner'
      pollInterval: null,

      showCancelModal: false,
      cancelReason: '',
      cancelDetail: '',
      cancelling: false,
      cancelError: null,
      donor: null,

      // Donor messages
      donorMessages: [
        { value: 'on_the_way', label: '🚗 On my way' },
        { value: 'reached', label: '📍 Reached' },
        { value: 'unable_to_come', label: '❌ Unable to come' },
        { value: 'delayed', label: '⏰ Running late' },
        { value: 'donated', label: '✅ Donation done' },
      ],

      // Partner messages
      partnerMessages: [
        { value: 'waiting_for_donor', label: '⏳ Waiting for donor' },
        { value: 'donor_arrived', label: '✅ Donor arrived' },
        { value: 'please_hurry', label: '⏰ Please hurry' },
        { value: 'donation_received', label: '🩸 Donation received' },
        { value: 'request_cancelled', label: '❌ Request cancelled' },
      ],

      showDonorRating: false,
donorRatingForm: {
    stars: 0,
    review: ''
},
submittingDonorRating: false,
donorRatingError: null,
    }
  }, 

  computed: {

    
    
    availableMessages() {
      return this.userType === 'donor'
        ? this.donorMessages
        : this.partnerMessages
    }
  },

  mounted() {

    this.requestId = this.$route.params.id

    const userType = localStorage.getItem('user_type')
    this.userType = userType === 'partner' ? 'partner' : 'donor'

    // Debug logs
    console.log('requestId:', this.requestId)
    console.log('userType:', this.userType)

    
    const queryOtp = this.$route.query.otp
    const storedOtp = localStorage.getItem(`otp_${this.requestId}`)
    this.otpCode = queryOtp || storedOtp || null

  
    this.fetchDonorInfo()  
    this.fetchMessages()
    this.fetchRequestInfo()

    // ── Step 4: Poll every 8 seconds ──────────
    this.pollInterval = setInterval(() => {
        this.fetchMessages()
    }, 8000)

    
  },

  beforeUnmount() {
    clearInterval(this.pollInterval)
  },

  methods: {

    formatMessage(text) {
  return text.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
},
    // Check if message is from current user
    isMyMessage(msg) {
      return msg.sender_type === this.userType
      
    },

    async fetchMessages() {
    try {
        const response = await api.get(
            `https://jeevandaan-yaal.onrender.com/api/chat/${this.requestId}/history/`,
            { params: { _t: Date.now() } }
        )
        this.messages = Array.isArray(response.data) ? response.data : []

        // Extract OTP from system message
        if (!this.otpCode) {
            const otpMsg = this.messages.find(m => m.sender_type === 'system')
            if (otpMsg) this.otpCode = otpMsg.otp_code
        }

        // Show rating if donation done
        const donationDone = this.messages.find(
            m => m.message === 'donated' || m.message === 'otp_verified'
        )
        if (donationDone && this.userType === 'donor') {
            this.showDonorRating = true
        }

        this.$nextTick(() => {
            const container = this.$refs.chatContainer
            if (container) container.scrollTop = container.scrollHeight
        })

    } catch (err) {
        console.error(err)
    } finally {
        this.loading = false
    }
},

async submitDonorRating() {
    if (!this.donorRatingForm.stars) {
        this.donorRatingError = 'Please select star rating.'
        return
    }

    this.submittingDonorRating = true

    try {
        await api.post(
            `https://jeevandaan-yaal.onrender.com/api/requests/donor/${this.requestId}/rate/`,
            this.donorRatingForm
        )
        this.showDonorRating = false
        alert('Thank you for rating! Your feedback helps us improve.')
    } catch (err) {
        this.donorRatingError = err.response?.data?.error ||
            'Rating failed. Try again.'
    } finally {
        this.submittingDonorRating = false
    }
},

    async fetchRequestInfo() {
    try {
        console.log('Fetching request info as:', this.userType)

        if (this.userType === 'partner') {
            const response = await api.get(
                'https://jeevandaan-yaal.onrender.com/api/requests/donor-requests/'
            )
            console.log('Partner requests:', response.data)
            const req = response.data.find(
                r => r.id === parseInt(this.requestId)
            )
            console.log('Found request:', req)
            if (req) this.requestInfo = req

        } else {
            // Donor — fetch assigned request directly
            const response = await api.get(
                `https://jeevandaan-yaal.onrender.com/api/requests/donor/${this.requestId}/detail/`
            )
            this.requestInfo = response.data
            console.log('requestInfo:', this.requestInfo)
            
        }

    } catch (err) {
        console.error('Request info fetch failed:', err.response?.data || err)
    }
},
    async sendMessage(message) {
      this.sending = true
      this.sendingMsg = message

      try {
        await api.post(`https://jeevandaan-yaal.onrender.com/api/chat/${this.requestId}/send/`, { message })
        await this.fetchMessages()
      } catch (err) {
        const msg = err.response?.data?.error || 'Failed to send message.'
        alert(msg)
        console.error(err)
      } finally {
        this.sending = false
        this.sendingMsg = null
      }
    },

    timeAgo(dateStr) {
      const diff = Math.floor((new Date() - new Date(dateStr)) / 60000)
      if (diff < 1) return 'Just now'
      if (diff < 60) return `${diff} mins ago`
      if (diff < 1440) return `${Math.floor(diff / 60)} hrs ago`
      return `${Math.floor(diff / 1440)} days ago`
    },


    async cancelAcceptance() {
    if (!this.cancelReason) {
        this.cancelError = 'Please select a reason.'
        return
    }

    this.cancelling = true
    this.cancelError = null

    try {
        const response = await api.post(
            `https://jeevandaan-yaal.onrender.com/api/requests/donor/${this.requestId}/cancel/`,
            {
                reason: this.cancelReason,
                detail: this.cancelDetail
            }
        )

        // Check if account locked
        if (response.data.account_locked) {
            alert(
                `⚠️ Your account has been locked due to multiple cancellations.\n\n` +
                `Username: ${response.data.username}\n` +
                `Locked until: ${response.data.locked_until}\n\n` +
                `Multiple cancellations after accepting requests may invite ` +
                `disciplinary action under IPC provisions.`
            )
            localStorage.removeItem('access_token')
            this.$router.push('/')
            return
        }

        this.showCancelModal = false
        alert(`Request cancelled. Reliability score deducted by 10 points.`)
        this.$router.push('/user')

    } catch (err) {
        this.cancelError = err.response?.data?.error || 'Cancellation failed.'
    } finally {
        this.cancelling = false
    }
},

async fetchDonorInfo() {
    if (this.userType !== 'donor') return
    try {
        const response = await api.get('https://jeevandaan-yaal.onrender.com/api/users/profile/')
        this.donor = response.data
    } catch (err) {
        console.error(err)
    }
},
  }
}
</script>

<style scoped>
.fw-800 { font-weight: 800; }
.smallest { font-size: 0.7rem; }
.letter-spacing { letter-spacing: 8px; }

.chat-scroll {
  overflow-y: auto;
  max-height: calc(100vh - 280px);
}
.chat-scroll::-webkit-scrollbar { width: 4px; }
.chat-scroll::-webkit-scrollbar-thumb {
  background: #e0e0e0;
  border-radius: 10px;
}

/* My messages — right side red */
.bubble-mine {
  background: #E63946;
  color: white;
  border-bottom-right-radius: 4px !important;
  max-width: 250px;
}

/* Their messages — left side white */
.bubble-theirs {
  background: white;
  color: #2d3436;
  border: 1px solid #eee;
  border-bottom-left-radius: 4px !important;
  max-width: 250px;
}
</style>