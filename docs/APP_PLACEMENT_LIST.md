# ✅ **PERMANENT APP PLACEMENT LIST (FINAL)**

**This is the new law of the land.**

---

## **1. DALS (Digital Asset Logistics System)**

**Role:** Central brainstem. Everything reports *to* DALS.
**Runs:** **Docker ONLY**
**Port:** **8003**
**Start Command:** `python run_server.py` or Docker Compose
📌 Files confirmed: `run_server.py` launches ISS/DALS at 8003

---

## **2. DALS Dashboard (Web UI)**

**Role:** Human interface. Buttons, graphs, logs.
**Runs:** **Local Python process during dev** → **Docker later**
**Port:** **8005**
📌 Confirmed in dashboard_server.py (starts 8005)

---

## **3. UCM (Unified Cognition Module) – Caleon Prime**

**Role:** The AI core.
**Runs:** **VS Code / Local ONLY during dev**
**Port:** **8000**
**Notes:**

* Never Dockerize until stable
* This is now the *only* active UCM instance
* Everything else connects *to* this one

---

## **4. Cali X One (Cohost / Articulation LLM)**

**Role:** Your on-camera speaking partner.
**Runs:** **Ollama Local**
**Port:** `11435`
**Model:** `phi3:mini`
**Rule:** UCM calls her. DALS never touches her directly.

---

## **5. GOAT System (Knowledge NFT Builder)**

**Runs:** **Docker ONLY**
**Port:** **9001**
**Notes:** GOAT reports to DALS via telemetry lines.

---

## **6. TrueMark Mint Engine**

**Runs:** **Docker ONLY**
**Port:** **9002**

---

## **7. CertSig (When Enabled Again)**

**Runs:** **Docker ONLY**
**Port:** **9003**
**Status:** Currently **disabled** until further build.

---

## **8. Phonatory Output Module (Coqui TTS)**

**Runs:** Local Python
**Port:** **8021**
**Notes:** Only alive when UCM needs speech.

---

## **9. Cochlear Processor**

**Runs:** Local Python
**Port:** **8020**

---

## **10. Alpha Worker Registry (internal DALS)**

**Runs:** Inside DALS container
**Port:** **no external port**
**Notes:** Only DALS sees it.

---

# ✅ **THE FINAL MAP YOU FOLLOW FROM THIS MOMENT ON**

| System                 | Dev           | Production  | Port      |
| ---------------------- | ------------- | ----------- | --------- |
| **DALS ISS Core**      | Docker        | Docker      | **8003**  |
| **DALS Dashboard**     | Local Python  | Docker      | **8005**  |
| **UCM / Caleon Prime** | Local VS Code | TBD later   | **8000**  |
| **Cali X One (Phi-3)** | Ollama local  | Same        | **11435** |
| **GOAT**               | Docker        | Docker      | **9001**  |
| **TrueMark**           | Docker        | Docker      | **9002**  |
| **CertSig**            | Off for now   | Off for now | **9003**  |
| **POM (Coqui)**        | Local         | Local       | **8021**  |
| **Cochlear**           | Local         | Local       | **8020**  |

---

# ✅ **NEXT STEP**

You say the word and I'll generate:

**→ The updated folder config files for ALL apps.
→ The updated docker-compose.yml.
→ The updated environment variables.
→ Cleanup commands to purge all old Docker ghosts so nothing fights you.**

Just say: **"Lock it in."**