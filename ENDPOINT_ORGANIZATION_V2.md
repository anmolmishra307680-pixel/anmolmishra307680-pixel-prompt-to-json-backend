# 🚀 Prompt-to-JSON API v2.1.1 - Endpoint Organization

## 📋 Complete Endpoint Catalog (47 Endpoints)

### 🔐 1. Authentication & Security
**Purpose**: User authentication, token management, and security validation

| Endpoint | Method | Icon | Description | Run Sequence |
|----------|--------|------|-------------|--------------|
| `/api/v1/auth/login` | POST | 🔑 | User login with credentials | **Step 1** |
| `/token` | POST | 🎫 | Generate JWT token | **Step 2** |
| `/api/v1/auth/refresh` | POST | 🔄 | Refresh expired token | **Step 3** |
| `/api/v1/auth/me` | GET | 👤 | Get current user info | **Step 4** |

**Schemas**: `LoginRequest`, `LoginResponse`, `TokenRequest`, `RefreshRequest`, `UserInfo`

---

### ℹ️ 2. System Information & Health
**Purpose**: System status, health checks, and basic information

| Endpoint | Method | Icon | Description | Run Sequence |
|----------|--------|------|-------------|--------------|
| `/` | GET | 🏠 | API root information | **Always Available** |
| `/health` | GET | ❤️ | System health check | **Always Available** |
| `/system-overview` | GET | 📊 | Complete system status | **Step 1** |
| `/system-test` | GET | 🧪 | Run system validation | **Step 2** |

---

### 🤖 3. Core AI Generation Pipeline
**Purpose**: Main AI design generation workflow

| Endpoint | Method | Icon | Description | Run Sequence |
|----------|--------|------|-------------|--------------|
| `/api/v1/generate` | POST | ✨ | Generate V2 (Enhanced) | **Step 1** |
| `/generate` | POST | 🎨 | Generate Spec (Legacy) | **Alternative Step 1** |
| `/api/v1/switch` | POST | 🔄 | Switch Material | **Step 2** |
| `/switch` | POST | 🔧 | Switch Material (Legacy) | **Alternative Step 2** |
| `/api/v1/core/run` | POST | ⚡ | Run Core Pipeline | **Step 3** |

**Schemas**: `GenerateRequestV2`, `GenerateResponse`, `SwitchRequest`, `SwitchResponse`, `CoreRunRequest`, `CoreRunResponse`

---

### 📏 4. Evaluation & Quality Assessment
**Purpose**: Design evaluation, scoring, and quality metrics

| Endpoint | Method | Icon | Description | Run Sequence |
|----------|--------|------|-------------|--------------|
| `/api/v1/evaluate` | POST | 📊 | Evaluate V2 (Enhanced) | **Step 1** |
| `/evaluate` | POST | 📈 | Evaluate Spec (Legacy) | **Alternative Step 1** |
| `/batch-evaluate` | POST | 📋 | Batch Evaluate Multiple | **Step 2** |
| `/reports/{report_id}` | GET | 📄 | Get Evaluation Report | **Step 3** |

**Schemas**: `EvaluateRequest`, `EvaluationResult`

---

### 🔄 5. Reinforcement Learning & Iteration
**Purpose**: AI model training and iterative improvement

| Endpoint | Method | Icon | Description | Run Sequence |
|----------|--------|------|-------------|--------------|
| `/api/v1/iterate` | POST | 🔄 | Iterate V2 (Enhanced) | **Step 1** |
| `/iterate` | POST | 🎯 | Iterate RL (Legacy) | **Alternative Step 1** |
| `/advanced-rl` | POST | 🧠 | Advanced RL Training | **Step 2** |
| `/coordinated-improvement` | POST | 🤝 | Multi-Agent Coordination | **Step 3** |
| `/iterations/{session_id}` | GET | 📊 | Get Iteration Logs | **Step 4** |

**Schemas**: `IterateRequest`, `IterationResult`

---

### ✅ 6. Compliance & Validation
**Purpose**: Design compliance checking and regulatory validation

| Endpoint | Method | Icon | Description | Run Sequence |
|----------|--------|------|-------------|--------------|
| `/api/v1/compliance/run_case` | POST | ✅ | Run Compliance Case | **Step 1** |
| `/api/v1/compliance/feedback` | POST | 💬 | Compliance Feedback | **Step 2** |
| `/api/v1/pipeline/run` | POST | 🔧 | Run Compliance Pipeline | **Step 3** |

**Schemas**: `ComplianceRequest`, `ComplianceFeedbackRequest`

---

### 🖼️ 7. Preview & Visualization
**Purpose**: 3D previews, geometry, and visual rendering

| Endpoint | Method | Icon | Description | Run Sequence |
|----------|--------|------|-------------|--------------|
| `/geometry/{case_id}` | GET | 📐 | Get Geometry Data | **Step 1** |
| `/api/v1/three-js/{spec_id}` | GET | 🎮 | Get Three.js Data | **Step 2** |
| `/api/v1/preview/refresh` | POST | 🔄 | Refresh Preview | **Step 3** |
| `/api/v1/preview/verify` | GET | ✅ | Verify Preview URL | **Step 4** |
| `/api/v1/preview/cleanup` | POST | 🧹 | Cleanup Stale Previews | **Step 5** |

---

### 📱 8. Mobile & Cross-Platform
**Purpose**: Mobile-optimized endpoints for React Native/Expo

| Endpoint | Method | Icon | Description | Run Sequence |
|----------|--------|------|-------------|--------------|
| `/api/v1/mobile/generate` | POST | 📱 | Mobile Generate | **Step 1** |
| `/api/v1/mobile/switch` | POST | 🔄 | Mobile Switch | **Step 2** |

**Schemas**: `MobileGenerateRequest`, `MobileSwitchRequest`

---

### 🥽 9. VR/AR & Immersive Tech
**Purpose**: Virtual and Augmented Reality integration

| Endpoint | Method | Icon | Description | Run Sequence |
|----------|--------|------|-------------|--------------|
| `/api/v1/vr/generate` | POST | 🥽 | VR Generate | **Step 1** |
| `/api/v1/vr/preview` | GET | 👁️ | Get VR Preview | **Step 2** |
| `/api/v1/vr/scene` | POST | 🌐 | Create VR Scene | **Step 3** |
| `/api/v1/ar/overlay` | POST | 📲 | AR Overlay | **Step 4** |

**Schemas**: `VRGenerateRequest`, `VRSceneRequest`, `VRPreviewResponse`, `AROverlayRequest`

---

### 🖥️ 10. Frontend & UI Integration
**Purpose**: Frontend session management and UI flow tracking

| Endpoint | Method | Icon | Description | Run Sequence |
|----------|--------|------|-------------|--------------|
| `/api/v1/ui/session` | POST | 🖥️ | Create UI Session | **Step 1** |
| `/api/v1/ui/flow` | POST | 📊 | Log UI Flow | **Step 2** |
| `/api/v1/ui/summary` | GET | 📋 | Get UI Test Summary | **Step 3** |

---

### 📊 11. Monitoring & Analytics
**Purpose**: System monitoring, metrics, and performance tracking

| Endpoint | Method | Icon | Description | Run Sequence |
|----------|--------|------|-------------|--------------|
| `/metrics` | GET | 📊 | Prometheus Metrics (Public) | **Always Available** |
| `/basic-metrics` | GET | 📈 | Basic Metrics | **Step 1** |
| `/api/v1/metrics/detailed` | GET | 📊 | Detailed Metrics | **Step 2** |
| `/agent-status` | GET | 🤖 | Agent Status | **Step 3** |
| `/cache-stats` | GET | 💾 | Cache Statistics | **Step 4** |

---

### 🗄️ 12. Data Management & Logging
**Purpose**: Data persistence, logging, and administrative tasks

| Endpoint | Method | Icon | Description | Run Sequence |
|----------|--------|------|-------------|--------------|
| `/log-values` | POST | 📝 | Log Values | **Step 1** |
| `/cli-tools` | GET | 🛠️ | Get CLI Tools | **Step 2** |
| `/admin/prune-logs` | POST | 🧹 | Prune Logs | **Admin Only** |

**Schemas**: `LogValuesRequest`

---

## 🔄 Complete Task Flow Sequences

### 🎯 **Primary Workflow: AI Design Generation**
```
1. 🔑 POST /api/v1/auth/login → Get JWT token
2. ✨ POST /api/v1/generate → Generate design
3. 📊 POST /api/v1/evaluate → Evaluate quality
4. 🔄 POST /api/v1/switch → Modify materials
5. 📐 GET /geometry/{case_id} → Get 3D data
6. ✅ POST /api/v1/compliance/run_case → Check compliance
```

### 📱 **Mobile Workflow**
```
1. 🔑 POST /api/v1/auth/login → Authenticate
2. 📱 POST /api/v1/mobile/generate → Mobile generate
3. 🔄 POST /api/v1/mobile/switch → Mobile switch
4. 🖥️ POST /api/v1/ui/session → Track session
```

### 🥽 **VR/AR Workflow**
```
1. 🔑 POST /api/v1/auth/login → Authenticate
2. 🥽 POST /api/v1/vr/generate → Generate VR scene
3. 🌐 POST /api/v1/vr/scene → Create scene
4. 📲 POST /api/v1/ar/overlay → Add AR overlay
```

### 🔄 **RL Training Workflow**
```
1. 🔑 POST /api/v1/auth/login → Authenticate
2. 🎯 POST /api/v1/iterate → Start iteration
3. 🧠 POST /advanced-rl → Advanced training
4. 🤝 POST /coordinated-improvement → Multi-agent
5. 📊 GET /iterations/{session_id} → Get results
```

### 📊 **Monitoring Workflow**
```
1. ❤️ GET /health → Check health
2. 📊 GET /system-overview → System status
3. 📈 GET /basic-metrics → Basic metrics
4. 🤖 GET /agent-status → Agent status
5. 💾 GET /cache-stats → Cache performance
```

---

## 🔒 Security & Authentication Matrix

| Security Level | Endpoints | Requirements |
|----------------|-----------|--------------|
| **🌐 Public** | `/health`, `/metrics`, `/` | None |
| **🔑 API Key Only** | `/token`, `/api/v1/auth/login` | X-API-Key header |
| **🛡️ Full Auth** | All other endpoints | X-API-Key + JWT Bearer token |

---

## 📊 Schema Categories

### 🔐 **Authentication Schemas**
- `LoginRequest`, `LoginResponse`, `TokenRequest`, `RefreshRequest`, `UserInfo`

### 🤖 **AI Generation Schemas**
- `GenerateRequestV2`, `GenerateResponse`, `SwitchRequest`, `SwitchResponse`

### 📊 **Evaluation Schemas**
- `EvaluateRequest`, `EvaluationResult`, `IterateRequest`

### ✅ **Compliance Schemas**
- `ComplianceRequest`, `ComplianceFeedbackRequest`

### 📱 **Mobile Schemas**
- `MobileGenerateRequest`, `MobileSwitchRequest`

### 🥽 **VR/AR Schemas**
- `VRGenerateRequest`, `VRSceneRequest`, `VRPreviewResponse`, `AROverlayRequest`

### 🔧 **System Schemas**
- `CoreRunRequest`, `CoreRunResponse`, `LogValuesRequest`

### ⚠️ **Error Schemas**
- `HTTPValidationError`, `ValidationError`

---

## 🎯 Quick Reference by Use Case

### 👨‍💻 **For Frontend Developers**
```
Authentication: /api/v1/auth/login → /token
Generation: /api/v1/generate → /api/v1/switch
UI Tracking: /api/v1/ui/session → /api/v1/ui/flow
```

### 📱 **For Mobile Developers**
```
Auth: /api/v1/auth/login
Mobile: /api/v1/mobile/generate → /api/v1/mobile/switch
```

### 🥽 **For VR/AR Developers**
```
Auth: /api/v1/auth/login
VR: /api/v1/vr/generate → /api/v1/vr/scene
AR: /api/v1/ar/overlay
```

### 🔬 **For QA/Testing**
```
Health: /health → /system-test
Metrics: /basic-metrics → /api/v1/metrics/detailed
```

### 👨‍💼 **For DevOps/Admin**
```
Monitoring: /metrics → /agent-status → /cache-stats
Maintenance: /admin/prune-logs → /api/v1/preview/cleanup
```

---

**🎉 Total: 47 Endpoints across 12 functional sections with complete authentication and monitoring coverage!**