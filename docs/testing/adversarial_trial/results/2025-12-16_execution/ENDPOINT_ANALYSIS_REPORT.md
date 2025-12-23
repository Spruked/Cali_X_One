# 🔌 **ENDPOINT MAPPING & CONNECTION ANALYSIS**
**Date:** December 16, 2025
**Purpose:** Pre-Cleanup Endpoint Verification & Safety Analysis

---

## 📡 **CRITICAL ENDPOINT INVENTORY**

### **PRIMARY SERVICES - ACTIVE ENDPOINTS**

#### 1. **Main ISS Service (Cali X One Core)**
**Port:** 8003 (internal) → 8006 (external via docker-compose)
**Purpose:** Integration Service System - Core AGI service
**Endpoints:**
- Health check available
- Full API surface through ISS module

**Configuration:**
- `docker-compose.yml`: Port mapping `8006:8003`
- `run_server.py`: Binds to `0.0.0.0:8003`
- Entry point: `iss_module.api.api:app`

**Status:** ✅ ACTIVE - DO NOT DELETE

---

#### 2. **SKG Service (Knowledge Graph)**
**Port:** 8004 (both internal and external)
**Purpose:** Symbolic Knowledge Graph API
**Endpoints:**
- `GET /health` - Health check
- `POST /add` - Add single triple
- `POST /add_batch` - Add multiple triples
- `GET /query` - Query knowledge graph
- `GET /stats` - Graph statistics
- `POST /expand` - Expand knowledge
- `GET /export` - Export graph data
- `POST /curiosity/seed` - Seed curiosity goals
- `GET /curiosity/goals` - Get curiosity goals
- `POST /predicate/invent` - Invent new predicates
- `GET /` - Root endpoint

**Configuration:**
- `docker-compose.yml`: Port mapping `8004:8004`
- Entry point: `skg-core/skg_api.py`

**Files Found:**
- ✅ `skg-core/skg_api.py` (PRIMARY)
- ⚠️ `skg-core/skg_api (2).py` (DUPLICATE - same endpoints)

**Status:** ✅ ACTIVE - DO NOT DELETE PRIMARY FILE

---

#### 3. **UCM Service (Unified Coordination Module)**
**Port:** 8080 (internal) → 8083 (external)
**Purpose:** Integration coordination
**Endpoints:**
- `GET /health` - Health check
- Integration endpoints (via main Dockerfile)

**Configuration:**
- `docker-compose.yml`: Port mapping `8083:8080`
- Depends on: cali-x-one service

**Status:** ✅ ACTIVE - DO NOT DELETE

---

#### 4. **DALS Service (Digital Asset Logistics System)**
**Port:** 8003 (internal) → 8007 (external)
**Purpose:** Digital asset management
**Endpoints:**
- `GET /health` - Health check
- Same API surface as cali-x-one (separate instance)

**Configuration:**
- `docker-compose.yml`: Port mapping `8007:8003`
- Depends on: cali-x-one service

**Status:** ✅ ACTIVE - DO NOT DELETE

---

#### 5. **Vault System Telemetry Dashboard**
**Port:** 8001 (default, configurable)
**Purpose:** Real-time monitoring and telemetry
**Endpoints:**
- `GET /` - Dashboard HTML
- `GET /api/system/status` - System status
- `GET /api/modules/{module_name}` - Module details
- `GET /api/glyphs/recent` - Recent glyphs
- `GET /api/reflections/recent` - Recent reflections
- `GET /api/performance/history` - Performance history

**Configuration:**
- `vault_system/vault_system/telemetry_dashboard/telemetry_dashboard.py`

**Files Found:**
- ✅ `telemetry_dashboard.py` (PRIMARY)
- ⚠️ `telemetry_dashboard (2).py` (DUPLICATE - identical endpoints)

**Status:** ✅ ACTIVE - DO NOT DELETE PRIMARY FILE

---

#### 6. **Vault System Main API**
**Port:** Configurable (not in docker-compose)
**Purpose:** Posterior Helix recursive rethinking
**Endpoints:**
- `POST /rethink` - Trigger rethinking process
- `GET /recursion_log` - Get recursion log
- `GET /vault_stats` - Vault statistics
- `GET /health` - Health check

**Configuration:**
- `vault_system/main.py`

**Files Found:**
- ✅ `main.py` (PRIMARY)
- ⚠️ `main (2).py` (DUPLICATE - identical endpoints)

**Status:** ✅ ACTIVE - DO NOT DELETE PRIMARY FILE

---

#### 7. **Worker Registry API**
**Port:** Part of ISS service (8003)
**Purpose:** Worker registration and management
**Endpoints:**
- `POST /api/workers/register` - Register worker
- `POST /api/workers/heartbeat` - Worker heartbeat
- `GET /api/workers/list` - List workers
- `DELETE /api/workers/unregister/{worker_id}` - Unregister worker
- `GET /api/workers/dmn/{worker_id}` - Get DMN details
- `GET /api/workers/dsn/{worker_id}` - Get DSN details

**Configuration:**
- `iss_module/api/worker_registry_api.py`

**Status:** ✅ ACTIVE - DO NOT DELETE

---

#### 8. **Worker Endpoints**

**Josephine Worker:**
- **Port:** 9998 (configurable via JOSEPHINE_PORT env)
- **Registry URL:** `http://localhost:8003/api/workers`
- **Purpose:** AGI worker instance

**Files Found:**
- ✅ `workers/josephine.py` (PRIMARY)
- ⚠️ `workers/josephine (2).py` (DUPLICATE - identical config)

**Bubble Worker:**
- **Port:** 9997 (configurable via BUBBLE_PORT env)
- **WebSocket Port:** 9997
- **Registry URL:** `http://localhost:8003/api/workers`
- **Purpose:** Browser integration worker
- **Supported Extensions:** Chrome, Firefox

**Files Found:**
- ✅ `workers/bubble_worker.py` (PRIMARY)
- ⚠️ `workers/bubble_worker (2).py` (DUPLICATE - identical config)

**Status:** ✅ ACTIVE - DO NOT DELETE PRIMARY FILES

---

### **INACTIVE/COMMENTED SERVICES**

The following services are defined but commented out in docker-compose.yml:

#### Commented Services (Not Currently Active)
1. **cochlear** - Audio processing (no port assigned yet)
2. **resonator** - Resonator pyramid (no port assigned yet)
3. **anterior** - Anterior helix (port 8001 reserved)
4. **posterior** - Posterior helix (port 8005 reserved)
5. **gyro** - Gyro harmonizer (port 8090 reserved)
6. **phonatory** - Phonatory output (no port assigned yet)

**Status:** ⚠️ RESERVED - Ports reserved for future use, not currently active

---

## 🔍 **DUPLICATE FILE ANALYSIS**

### **Category 1: Configuration Files (HIGH RISK)**

| Base File | Duplicate | Endpoint Impact | Action |
|-----------|-----------|-----------------|--------|
| docker-compose.yml | docker-compose (2).yml | Identical port mappings | ⚠️ COMPARE, keep base |
| .env | (2).env | Environment variables | ⚠️ COMPARE, keep current |
| requirements.txt | requirements (2).txt | FastAPI dependencies | ⚠️ COMPARE, keep current |
| Dockerfile | Dockerfile (2) | Build configuration | ⚠️ COMPARE, keep base |

**Risk Level:** HIGH - Wrong config file could break all services

---

### **Category 2: API Implementation Files (CRITICAL)**

| Base File | Duplicate | Endpoints | Action |
|-----------|-----------|-----------|--------|
| skg-core/skg_api.py | skg-core/skg_api (2).py | 11 endpoints | ⚠️ VERIFY IDENTICAL, delete dup |
| vault_system/main.py | vault_system/main (2).py | 4 endpoints | ⚠️ VERIFY IDENTICAL, delete dup |
| vault_system/telemetry_dashboard.py | telemetry_dashboard (2).py | 6 endpoints | ⚠️ VERIFY IDENTICAL, delete dup |

**Risk Level:** CRITICAL - Deleting wrong file breaks API surface

---

### **Category 3: Worker Files (MEDIUM RISK)**

| Base File | Duplicate | Port | Action |
|-----------|-----------|------|--------|
| workers/josephine.py | josephine (2).py | 9998 | ⚠️ VERIFY IDENTICAL, delete dup |
| workers/bubble_worker.py | bubble_worker (2).py | 9997 | ⚠️ VERIFY IDENTICAL, delete dup |

**Risk Level:** MEDIUM - Workers can be restarted if issues occur

---

### **Category 4: Utility Scripts (LOW RISK)**

| Base File | Duplicate | Port Impact | Action |
|-----------|-----------|-------------|--------|
| run_server.py | run_server (2).py | 8003 binding | ✅ IDENTICAL - Safe to delete dup |
| benchmark.py | benchmark (2).py | No endpoints | ✅ Safe to delete dup |
| deps.py | deps (2).py | No endpoints | ✅ Safe to delete dup |

**Risk Level:** LOW - No endpoint impact

---

### **Category 5: Documentation/Data (NO RISK)**

| Base File | Duplicate | Endpoint Impact | Action |
|-----------|-----------|-----------------|--------|
| README.md | README (2).md | None | ✅ Safe to delete dup |
| LICENSE | LICENSE (2) | None | ✅ Safe to delete dup |
| *.db files | *.db (2) files | None | ⚠️ BACKUP first, then delete |

**Risk Level:** NONE - No endpoint impact

---

## 🛡️ **SAFETY RECOMMENDATIONS**

### **PHASE 1: VERIFICATION (DO THIS FIRST)**

#### Step 1.1: Compare Critical API Files
```powershell
# Compare skg_api files
$file1 = Get-Content "skg-core\skg_api.py"
$file2 = Get-Content "skg-core\skg_api (2).py"
Compare-Object $file1 $file2

# If identical (no output), safe to delete duplicate
# If different, STOP and investigate
```

#### Step 1.2: Compare Worker Files
```powershell
# Compare josephine workers
Compare-Object (Get-Content "workers\josephine.py") (Get-Content "workers\josephine (2).py")

# Compare bubble workers
Compare-Object (Get-Content "workers\bubble_worker.py") (Get-Content "workers\bubble_worker (2).py")
```

#### Step 1.3: Compare Configuration Files
```powershell
# Compare docker-compose
Compare-Object (Get-Content "docker-compose.yml") (Get-Content "docker-compose (2).yml")

# Compare requirements
Compare-Object (Get-Content "requirements.txt") (Get-Content "requirements (2).txt")
```

---

### **PHASE 2: SAFE DELETION STRATEGY**

#### Priority 1: Delete Confirmed Identical Files
**Only after verification shows no differences:**
- `run_server (2).py` - ✅ Confirmed identical
- Documentation duplicates (README, LICENSE)
- Utility script duplicates (benchmark, deps)

#### Priority 2: Archive Then Delete API Duplicates
**After verification:**
1. Create archive: `archive/api_duplicates_2025-12-16/`
2. Copy all duplicate API files to archive
3. Delete from source
4. Test all endpoints with curl/Postman
5. Keep archive for 1 week

#### Priority 3: Database Cleanup
**Critical - data loss risk:**
1. Backup ALL .db files: `backup/databases_2025-12-16/`
2. Compare sizes: `ucm_skg.db` (24KB) vs `ucm_skg (2).db` (20KB) ⚠️
3. Determine which has latest data
4. Keep current, delete old
5. NEVER delete without backup

---

### **PHASE 3: POST-CLEANUP VERIFICATION**

#### Test All Endpoints
```bash
# Test ISS Service
curl http://localhost:8006/health

# Test SKG Service  
curl http://localhost:8004/health

# Test UCM Service
curl http://localhost:8083/health

# Test DALS Service
curl http://localhost:8007/health

# Test Worker Registry
curl http://localhost:8006/api/workers/list
```

#### Verify Workers Can Connect
```bash
# Check worker connectivity
# Workers should successfully register with registry at 8003
```

---

## 📊 **ENDPOINT SUMMARY**

### **Active Services Count:** 8
### **Total Active Endpoints:** 40+
### **Reserved Ports:** 6 (for future services)
### **Worker Ports:** 2 (9997, 9998)

### **Port Allocation Map**
```
8003 - ISS Core (internal)
8004 - SKG Service
8006 - ISS Core (external)
8007 - DALS Service
8083 - UCM Service
8080 - UCM Service (internal)
9997 - Bubble Worker + WebSocket
9998 - Josephine Worker

RESERVED:
8001 - Anterior Helix (commented)
8005 - Posterior Helix (commented)
8090 - Gyro Harmonizer (commented)
```

---

## ⚠️ **CRITICAL WARNINGS**

### **DO NOT DELETE THESE FILES WITHOUT VERIFICATION:**
1. ❌ `skg-core/skg_api.py` - Contains all 11 SKG endpoints
2. ❌ `vault_system/main.py` - Contains vault API (4 endpoints)
3. ❌ `vault_system/telemetry_dashboard.py` - Contains dashboard (6 endpoints)
4. ❌ `iss_module/api/worker_registry_api.py` - Contains worker management (6 endpoints)
5. ❌ `workers/josephine.py` - Josephine worker implementation
6. ❌ `workers/bubble_worker.py` - Bubble worker with WebSocket
7. ❌ `docker-compose.yml` - Service orchestration configuration
8. ❌ `run_server.py` - Server entry point

### **SAFE TO DELETE (AFTER VERIFICATION):**
1. ✅ `run_server (2).py` - Confirmed identical to base
2. ✅ `README (2).md` - Documentation duplicate
3. ✅ `LICENSE (2)` - License duplicate
4. ✅ Documentation duplicates in vault_system/
5. ✅ Utility script duplicates (after comparison)

### **REQUIRES INVESTIGATION:**
1. ⚠️ `ucm_skg.db` vs `ucm_skg (2).db` - Different sizes (24KB vs 20KB)
2. ⚠️ `.venv/` directory - 39,000+ duplicate files
3. ⚠️ Configuration files - Need line-by-line comparison

---

## 🎯 **CLEANUP DECISION MATRIX**

| File Type | Compare First? | Backup First? | Delete Dup? |
|-----------|----------------|---------------|-------------|
| API Files | ✅ YES | ✅ YES | After verification |
| Config Files | ✅ YES | ✅ YES | After review |
| Worker Files | ✅ YES | ✅ YES | After verification |
| Database Files | ✅ YES | ✅ YES (CRITICAL) | After data check |
| Documentation | ❌ NO | ❌ NO | ✅ YES |
| Utility Scripts | ✅ YES | ❌ NO | After verification |

---

## 📝 **RECOMMENDED CLEANUP ORDER**

1. **Create full backup** (workspace + databases)
2. **Compare all API files** (skg_api, main, telemetry_dashboard)
3. **Compare worker files** (josephine, bubble_worker)
4. **Compare configuration files** (docker-compose, requirements, .env)
5. **Test current system** (all endpoints responding)
6. **Archive duplicates** (don't delete yet)
7. **Delete confirmed identical files** (documentation, utility scripts)
8. **Test after each deletion** (endpoint health checks)
9. **Monitor for 1 week** (ensure no regressions)
10. **Permanent deletion** (remove archive after verification period)

---

## 🚦 **CLEANUP STATUS**

**Current Status:** 🔴 **ANALYSIS COMPLETE - AWAITING APPROVAL**

**Endpoints Mapped:** ✅ 40+ endpoints identified and documented
**Risk Assessment:** ✅ Critical files flagged
**Backup Plan:** ✅ Defined
**Verification Steps:** ✅ Documented
**Rollback Plan:** ✅ Archive strategy defined

**Next Action:** REQUIRE EXPLICIT APPROVAL before proceeding with any file deletion

---

**Report Generated:** December 16, 2025
**Report Type:** Pre-Cleanup Endpoint Safety Analysis
**Status:** ✅ ENDPOINT MAPPING COMPLETE - NO DELETIONS PERFORMED YET
