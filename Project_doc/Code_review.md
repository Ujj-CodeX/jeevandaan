## Axios Interceptors:
src/api/index.js

- Axios interceptors middleware ki tarah kaam karte hain. Request interceptor har outgoing request me JWT Authorization header attach karta hai. Response interceptor 401 Unauthorized ko intercept karta hai, refresh token se naya access token leta hai, original request ko retry karta hai, aur concurrent 401 requests ke liye queue maintain karta hai taaki sirf ek refresh call ho. Agar refresh bhi fail ho jaye to user ko logout karke login page par redirect kar deta hai.

-- Flow

Vue Component
(User clicks Login / Profile / Any API)
        │
        ▼
api.get() / api.post()
(API request starts)
        │
        ▼
Axios Request Interceptor
(Request bhejne se pehle execute hota hai)
        │
        ▼
Read access_token from localStorage
(Existing JWT nikalo)
        │
        ▼
Attach Authorization Header
(Bearer <access_token> add karo)
        │
        ▼
HTTP Request Sent
(Request Django Backend ko gaya)
        │
        ▼
───────────────────────────────
Backend Processing
(Authentication + Permission + View)
───────────────────────────────
        │
        ├──────────────► 200 OK
        │                 (Token valid hai)
        │
        │                 ▼
        │          Axios Response Interceptor
        │          (Response receive)
        │                 │
        │                 ▼
        │          Return Response to Component
        │          (UI update)
        │
        │
        └──────────────► 401 Unauthorized
                          (Access Token Expired)
                                │
                                ▼
                     Response Interceptor Trigger
                     (401 detect hua)
                                │
                                ▼
                   Check _retry Flag
                   (Infinite retry loop avoid)
                                │
                                ▼
                   Check isRefreshing
                                │
             ┌──────────────────┴──────────────────┐
             │                                     │
             │                                     │
             ▼                                     ▼
      FALSE (No Refresh Running)          TRUE (Refresh Running)
             │                                     │
             ▼                                     ▼
      isRefreshing = true               Add Request to Queue
      (Lock Refresh)                    (Wait silently)
             │                                     │
             ▼                                     │
      Read refresh_token                           │
      (localStorage)                               │
             │                                     │
             ▼                                     │
      POST /api/auth/refresh/                      │
      (Backend se new token maango)               │
             │                                     │
             ▼                                     │
     ┌───────────────┴────────────────┐            │
     │                                │            │
     ▼                                ▼            │
Refresh Success                 Refresh Failed      │
(New Tokens)                    (Expired/Invalid)   │
     │                                │            │
     ▼                                ▼            │
Store New Access Token         Remove Tokens        │
(Update localStorage)          (Cleanup)            │
     │                                │            │
     ▼                                ▼            │
Store New Refresh Token       Redirect Login        │
(Rotation Support)            (Session End)         │
     │                                │            │
     ▼                                ▼            │
Resolve Queue                Reject All Requests ◄──┘
(Waiting requests continue)
     │
     ▼
Update Authorization Header
(New Access Token)
     │
     ▼
Retry Original Request
(Same API automatically)
     │
     ▼
Backend Again
(Now token valid)
     │
     ▼
200 OK
     │
     ▼
Return Response
     │
     ▼
Vue Component Receives Data
(UI Successfully Updated)


## 
