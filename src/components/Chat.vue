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
    <div v-if="otpCode" class="container pt-3">
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
                <p class="mb-0 fw-bold small">{{ msg.message_display }}</p>
                <small class="opacity-75 smallest">{{ timeAgo(msg.sent_at) }}</small>
              </div>
            </div>
          </div>

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
        { value: 'on_the_way', label: '⏳ Waiting for donor' },
        { value: 'reached', label: '✅ Donor arrived' },
        { value: 'delayed', label: '⏰ Please hurry' },
        { value: 'donated', label: '🩸 Donation received' },
        { value: 'unable_to_come', label: '❌ Request cancelled' },
      ],
    }
  },

  computed: {
    // Show messages based on who is logged in
    availableMessages() {
      return this.userType === 'donor'
        ? this.donorMessages
        : this.partnerMessages
    }
  },

  mounted() {
    this.requestId = this.$route.params.id
    this.userType = localStorage.getItem('user_type') || 'donor'

    // Get OTP
    const queryOtp = this.$route.query.otp
    const storedOtp = localStorage.getItem(`otp_${this.requestId}`)
    this.otpCode = queryOtp || storedOtp || null

    this.fetchMessages()
    this.fetchRequestInfo()

    // Poll every 8 seconds
    this.pollInterval = setInterval(() => {
      this.fetchMessages()
    }, 8000)
  },

  beforeUnmount() {
    clearInterval(this.pollInterval)
  },

  methods: {
    // Check if message is from current user
    isMyMessage(msg) {
      return msg.sender_type === this.userType
    },

    async fetchMessages() {
      try {
        const response = await api.get(`/api/chat/${this.requestId}/history/`)
        this.messages = Array.isArray(response.data) ? response.data : []

        // Extract OTP from system message if not already set
        if (!this.otpCode) {
          const otpMsg = this.messages.find(m => m.sender_type === 'system')
          if (otpMsg) this.otpCode = otpMsg.otp_code
        }

        // Scroll to bottom
        this.$nextTick(() => {
          const container = this.$refs.chatContainer
          if (container) container.scrollTop = container.scrollHeight
        })

      } catch (err) {
        console.error('Chat fetch failed:', err)
      } finally {
        this.loading = false
      }
    },

    async fetchRequestInfo() {
      try {
        // Different endpoint based on user type
        if (this.userType === 'donor') {
          const response = await api.get(`/api/requests/donor/list/`)
          const req = response.data.find(r => r.id === parseInt(this.requestId))
          if (req) this.requestInfo = req
        } else {
          // Partner fetches from their active requests
          const response = await api.get(`/api/requests/donor/list/`)
          const req = response.data.find(r => r.id === parseInt(this.requestId))
          if (req) this.requestInfo = req
        }
      } catch (err) {
        console.error('Request info fetch failed:', err)
      }
    },

    async sendMessage(message) {
      this.sending = true
      this.sendingMsg = message

      try {
        await api.post(`/api/chat/${this.requestId}/send/`, { message })
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
    }
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