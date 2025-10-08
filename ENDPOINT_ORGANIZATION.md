# 🚀 API Endpoints Organization - Task Flow Sequence

## 🔐 Authentication & Security
**Entry Point - Required for all protected endpoints**

| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `POST /token` | POST | Create JWT token (API key required) | **Step 1** |
| `POST /api/v1/auth/login` | POST | Enhanced JWT login with refresh tokens | **Step 1** |
| `POST /api/v1/auth/refresh` | POST | Refresh access token | **Ongoing** |

---

## 🏠 Core Information & Health
**System status and basic information**

| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `GET /` | GET | Root endpoint with API info | **Entry** |
| `GET /health` | GET | Public health check (no auth required) | **Monitoring** |
| `GET /system-overview` | GET | Comprehensive system status | **Admin** |

---

## 🤖 AI Generation Pipeline
**Main task flow: Prompt → Spec → Evaluation → Iteration**

### Step 1: Generate Design Specifications
| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `POST /generate` | POST | Generate specification from prompt (Legacy) | **Step 2A** |
| `POST /api/v1/generate` | POST | Enhanced generation with v2 schema | **Step 2B** |

### Step 2: Modify & Switch Materials
| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `POST /api/v1/switch` | POST | Switch object materials/properties | **Step 3** |

### Step 3: Evaluate Designs
| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `POST /evaluate` | POST | Evaluate specification (Legacy) | **Step 4A** |
| `POST /api/v1/evaluate` | POST | Enhanced evaluation endpoint | **Step 4B** |

### Step 4: Iterative Improvement
| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `POST /iterate` | POST | RL iterations with detailed logs | **Step 5A** |
| `POST /api/v1/iterate` | POST | Enhanced RL iteration endpoint | **Step 5B** |
| `POST /advanced-rl` | POST | Advanced RL training with policy gradients | **Step 5C** |

---

## 🔄 Advanced Coordination
**Multi-agent orchestration and batch processing**

| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `POST /coordinated-improvement` | POST | Multi-agent coordination for optimal results | **Step 6** |
| `POST /batch-evaluate` | POST | Process multiple specs/prompts | **Batch** |
| `GET /agent-status` | GET | Get status of all AI agents | **Monitoring** |

---

## 🏗️ Compliance & Geometry Pipeline
**Building compliance and geometry generation**

| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `POST /api/v1/compliance/run_case` | POST | Run compliance check | **Compliance 1** |
| `POST /api/v1/compliance/feedback` | POST | Send compliance feedback | **Compliance 2** |
| `GET /geometry/{case_id}` | GET | Get geometry file for case | **Compliance 3** |
| `POST /api/v1/pipeline/run` | POST | End-to-end compliance pipeline | **Full Pipeline** |

---

## 🖼️ Preview & Visualization
**Image generation and preview management**

| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `POST /api/v1/preview/refresh` | POST | Force refresh preview for spec | **Visual 1** |
| `GET /api/v1/preview/verify` | GET | Verify signed preview URL | **Visual 2** |
| `POST /api/v1/preview/cleanup` | POST | Cleanup stale preview URLs | **Maintenance** |
| `GET /api/v1/three-js/{spec_id}` | GET | Get Three.js formatted data | **3D Render** |

---

## 📱 Mobile & Cross-Platform
**Mobile-optimized endpoints for React Native/Expo**

| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `POST /api/v1/mobile/generate` | POST | Mobile-optimized generate endpoint | **Mobile 1** |
| `POST /api/v1/mobile/switch` | POST | Mobile-optimized switch endpoint | **Mobile 2** |

---

## 🥽 VR/AR Integration
**Virtual and Augmented Reality support**

| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `POST /api/v1/vr/generate` | POST | VR scene generation | **VR 1** |
| `POST /api/v1/ar/overlay` | POST | AR overlay creation | **AR 1** |

---

## 🖥️ Frontend Integration & Testing
**UI testing and frontend support**

| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `POST /api/v1/ui/session` | POST | Create UI testing session | **UI 1** |
| `POST /api/v1/ui/flow` | POST | Log UI testing flow | **UI 2** |
| `GET /api/v1/ui/summary` | GET | Get UI testing summary | **UI 3** |

---

## 📊 Monitoring & Metrics
**Performance monitoring and system metrics**

| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `GET /metrics` | GET | Public Prometheus metrics | **Public** |
| `GET /api/v1/metrics/detailed` | GET | Detailed metrics with authentication | **Protected** |
| `GET /basic-metrics` | GET | Basic metrics endpoint | **Simple** |
| `GET /cache-stats` | GET | Cache performance statistics | **Performance** |

---

## 📋 Data Management & Logs
**Data retrieval and logging**

| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `GET /reports/{report_id}` | GET | Retrieve full report from DB | **Data 1** |
| `GET /iterations/{session_id}` | GET | Get iteration logs for session | **Data 2** |
| `POST /log-values` | POST | Store HIDG values per day | **Logging** |

---

## 🛠️ Administration & Utilities
**System administration and maintenance**

| Endpoint | Method | Description | Flow Position |
|----------|--------|-------------|---------------|
| `GET /cli-tools` | GET | Get available CLI tools and commands | **Admin 1** |
| `GET /system-test` | GET | Run basic system tests | **Admin 2** |
| `POST /admin/prune-logs` | POST | Prune old logs for scalability | **Maintenance** |

---

## 🔄 Typical Task Flow Sequence

### **Standard Design Generation Flow:**
```
1. POST /token (Get authentication)
2. POST /api/v1/generate (Generate design)
3. POST /api/v1/switch (Modify materials - optional)
4. POST /api/v1/evaluate (Evaluate design)
5. POST /api/v1/iterate (Improve with RL - optional)
6. GET /api/v1/three-js/{spec_id} (Get 3D data)
```

### **Compliance Pipeline Flow:**
```
1. POST /token (Get authentication)
2. POST /api/v1/pipeline/run (Full compliance pipeline)
3. GET /geometry/{case_id} (Download geometry)
4. POST /api/v1/compliance/feedback (Send feedback)
```

### **Mobile Development Flow:**
```
1. POST /token (Get authentication)
2. POST /api/v1/mobile/generate (Mobile generation)
3. POST /api/v1/mobile/switch (Mobile switching)
```

### **Advanced Coordination Flow:**
```
1. POST /token (Get authentication)
2. POST /coordinated-improvement (Multi-agent coordination)
3. GET /agent-status (Check agent status)
4. POST /batch-evaluate (Batch processing)
```

---

## 📈 Total Endpoints: **47 Active Endpoints**
- **🔐 Authentication**: 3 endpoints
- **🤖 AI Generation**: 8 endpoints  
- **🏗️ Compliance**: 4 endpoints
- **🖼️ Preview**: 4 endpoints
- **📱 Mobile**: 2 endpoints
- **🥽 VR/AR**: 2 endpoints
- **🖥️ Frontend**: 3 endpoints
- **📊 Monitoring**: 4 endpoints
- **📋 Data**: 3 endpoints
- **🛠️ Admin**: 3 endpoints
- **🏠 Core**: 3 endpoints

**All endpoints are production-ready with enterprise authentication, rate limiting, and comprehensive error handling.**