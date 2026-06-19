import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
})

// Auto attach JWT token to every request
api.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// ── Refresh-token rotation handling ──────────────────────
// Jab access token expire hoke 401 aaye, automatically refresh
// karke original request retry karo. Multiple requests fail hon
// saath mein toh sirf EK refresh call ho — baaki queue mein wait karein.

let isRefreshing = false
let refreshQueue = []

function resolveQueue(token) {
    refreshQueue.forEach(cb => cb(token))
    refreshQueue = []
}

api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config

        // Sirf 401 pe try karo, aur ek hi baar retry karo (loop na bane)
        if (error.response?.status === 401 && !originalRequest._retry) {

            // Refresh endpoint khud fail ho gaya — yahin se logout karo, retry mat karo
            if (originalRequest.url.includes('/api/auth/refresh/')) {
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                localStorage.removeItem('user_type')
                window.location.href = '/#/login'
                return Promise.reject(error)
            }

            originalRequest._retry = true

            // Agar already koi refresh chal raha hai, queue mein wait karo
            if (isRefreshing) {
                return new Promise((resolve, reject) => {
                    refreshQueue.push((newToken) => {
                        if (newToken) {
                            originalRequest.headers.Authorization = `Bearer ${newToken}`
                            resolve(api(originalRequest))
                        } else {
                            reject(error)
                        }
                    })
                })
            }

            isRefreshing = true

            try {
                const refreshToken = localStorage.getItem('refresh_token')
                if (!refreshToken) {
                    throw new Error('No refresh token available')
                }

                const res = await axios.post(
                    `${import.meta.env.VITE_API_URL}/api/auth/refresh/`,
                    { refresh: refreshToken }
                )

                const newAccess = res.data.access
                const newRefresh = res.data.refresh

                // ── IMPORTANT: rotation ki wajah se refresh token bhi badal gaya
                localStorage.setItem('access_token', newAccess)
                localStorage.setItem('refresh_token', newRefresh)

                resolveQueue(newAccess)
                isRefreshing = false

                originalRequest.headers.Authorization = `Bearer ${newAccess}`
                return api(originalRequest)

            } catch (refreshError) {
                resolveQueue(null)
                isRefreshing = false

                // Refresh fail — clean logout
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                localStorage.removeItem('user_type')
                window.location.href = '/#/login'

                return Promise.reject(refreshError)
            }
        }

        return Promise.reject(error)
    }
)

export default api