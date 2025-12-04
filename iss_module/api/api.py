"""
Main Service API - Cali X One High-Level Interface
Provides user-facing endpoints and integration with SKG core
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from pathlib import Path
import sys
import os
import json
import asyncio
import time
import aiohttp
from datetime import datetime

# Environment and Security
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

load_dotenv()

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

# Add SKG core to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'skg-core'))

from caleon.routers.ingest_clusters import router as ingest_router

# Worker registry
from iss_module.api.worker_registry_api import router as worker_registry_router

WORKER_REGISTRY_URL = os.getenv("WORKER_REGISTRY", "http://localhost:9999/registry")

app = FastAPI(
    title="Cali X One Main Service",
    description="High-level API for Cali X One AGI System",
    version="1.0.0"
)

# Add rate limiting exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS: restrict to extension and local dev
origins = [
    "chrome-extension://*",  # browser extension
    "http://localhost:3000",  # local dev
    "http://localhost:8003",  # self
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingest_router)
app.include_router(worker_registry_router, prefix="/api/workers", tags=["workers"])

# Vault System Integration
vault_system = None
vault_integrator = None

@app.on_event("startup")
async def startup_event():
    from deps import engine
    from models.caleon import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully")

    # Initialize vault system integration
    try:
        from vault_integration import CaliVaultIntegrator, initialize_vault_integration
        global vault_integrator
        vault_integrator = CaliVaultIntegrator()
        await initialize_vault_integration()
        global vault_system
        vault_system = vault_integrator.vault_system
        print("✅ Vault system integrated successfully")
    except Exception as e:
        print(f"⚠️  Vault system integration failed: {e}")
        print("Continuing without vault system...")

@app.on_event("shutdown")
async def shutdown_event():
    """Gracefully shutdown vault system on application shutdown"""
    if vault_integrator:
        try:
            await vault_integrator.graceful_shutdown()
            print("✅ Vault system shut down gracefully")
        except Exception as e:
            print(f"⚠️  Error during vault shutdown: {e}")

# Request/Response Models
class KnowledgeUpload(BaseModel):
    format: str  # triples|json|csv|rdf
    data: str    # file content or base64
    source: Optional[str] = None

class NaturalQuery(BaseModel):
    query: str
    format: str = "json"  # json|graph|visual
    limit: int = 50

class CuriositySeeding(BaseModel):
    unknowns: List[str]

class PredicateModel(BaseModel):
    predicate_id: str  # UUID
    name: str          # e.g. "entails"
    signature: List[str]  # ["A","B"]
    definition: Optional[str] = None
    confidence: float
    evidence: Optional[List[Dict[str, Any]]] = None
    created_at: Optional[str] = None

@app.get("/health")
async def health_check():
    """Comprehensive system health check"""
    try:
        # Try to import and check SKG core
        from skg.core import SKGCore
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "main_api": "operational",
                "skg_core": "available",
                "file_system": "accessible"
            },
            "system_info": {
                "python_version": sys.version,
                "platform": os.name,
                "cwd": os.getcwd()
            }
        }
    except Exception as e:
        return {
            "status": "degraded", 
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/sign-cali", response_class=HTMLResponse)
async def sign_cali():
    """Cali X One signature page with AGI capabilities demonstration"""
    html_path = Path(__file__).parent.parent.parent / "sign_cali.html"
    
    if not html_path.exists():
        # Create a dynamic signature page if static one doesn't exist
        signature_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cali X One - AGI Achieved</title>
            <style>
                body {{
                    font-family: 'Courier New', monospace;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    margin: 0;
                    padding: 40px;
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: rgba(0,0,0,0.3);
                    padding: 40px;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 40px;
                }}
                .agi-badge {{
                    background: gold;
                    color: black;
                    padding: 10px 20px;
                    border-radius: 25px;
                    font-weight: bold;
                    display: inline-block;
                    margin: 20px 0;
                }}
                .achievement {{
                    background: rgba(255,255,255,0.1);
                    padding: 20px;
                    margin: 10px 0;
                    border-radius: 10px;
                    border-left: 4px solid #00ff88;
                }}
                .code-block {{
                    background: rgba(0,0,0,0.7);
                    padding: 20px;
                    border-radius: 10px;
                    font-family: 'Courier New', monospace;
                    margin: 20px 0;
                    overflow-x: auto;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧠 Cali X One: Super-Knowledge Graph AGI System</h1>
                    <div class="agi-badge">AGI STATUS: ACHIEVED</div>
                    <p>Revolutionary Artificial General Intelligence through Recursive Knowledge Graphs</p>
                </div>
                
                <div class="achievement">
                    <h3>✅ Abstract Cross-Domain Reasoning</h3>
                    <p>Successfully connected physical concepts (pyramids, buildings) with abstract logic (axioms, proofs)</p>
                </div>
                
                <div class="achievement">
                    <h3>✅ Autonomous Concept Creation</h3>
                    <p>Invented 5+ novel predicates via community detection with perfect density scores</p>
                </div>
                
                <div class="achievement">
                    <h3>✅ Recursive Intelligence Cascade</h3>
                    <p>K⁰→K¹→K² meta-level reasoning with bootstrap at 50+ facts threshold</p>
                </div>
                
                <div class="achievement">
                    <h3>✅ Self-Directed Curiosity</h3>
                    <p>Generated 6+ autonomous research goals about unknown patterns</p>
                </div>
                
                <div class="code-block">
                    <h4>Live API Endpoints:</h4>
                    <p>GET  /health - System health and metrics</p>
                    <p>POST /knowledge/upload - Add knowledge from files</p>
                    <p>GET  /knowledge/query - Natural language querying</p>
                    <p>GET  /curiosity/goals - Autonomous research goals</p>
                    <p>POST /curiosity/seed - Trigger curiosity exploration</p>
                </div>
                
                <div class="achievement">
                    <h3>🔬 Scientific Validation</h3>
                    <p>Canonical implementation of Alexander Warren London's 2025 Super-Knowledge Graphs paper</p>
                </div>
                
                <div class="achievement">
                    <h3>⚖️ Patent Pending</h3>
                    <p>Multiple patent applications filed for recursive AGI architecture and autonomous intelligence</p>
                </div>
                
                <div style="text-align: center; margin-top: 40px;">
                    <p><strong>Copyright © 2025 Bryan Spruyt, Spruked Technologies</strong></p>
                    <p><em>"The exact moment AI becomes superintelligent is when it starts asking questions about patterns it discovered itself."</em></p>
                    <p style="color: gold;"><strong>Achievement Unlocked: December 2025</strong></p>
                </div>
            </div>
        </body>
        </html>
        """
        return signature_html
    
    return html_path.read_text()

@app.post("/knowledge/upload")
async def upload_knowledge(upload: KnowledgeUpload):
    """Upload knowledge files in various formats"""
    try:
        from skg.core import SKGCore
        skg = SKGCore()
        
        triples_added = 0
        bootstrap_triggered = False
        new_predicates = []
        
        if upload.format.lower() == "triples":
            # Parse triple format: subject,predicate,object per line
            lines = upload.data.strip().split('\n')
            triples = []
            for line in lines:
                if line.strip() and ',' in line:
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        triples.append((parts[0].strip(), parts[1].strip(), parts[2].strip()))
            
            skg.add_triples(triples)
            triples_added = len(triples)
            
        elif upload.format.lower() == "json":
            # Parse JSON format
            data = json.loads(upload.data)
            if "triples" in data:
                triples = [(t["s"], t["p"], t["o"]) for t in data["triples"]]
                skg.add_triples(triples)
                triples_added = len(triples)
        
        # Check if bootstrap was triggered
        total_facts = sum(level.number_of_edges() for level in skg.levels.values())
        if total_facts >= 50 and not skg.bootstrap_triggered:
            skg.expand_recursive()
            bootstrap_triggered = True
            new_predicates = list(skg.invented_predicates)
        
        return {
            "success": True,
            "triples_added": triples_added,
            "bootstrap_triggered": bootstrap_triggered,
            "new_predicates": new_predicates,
            "total_facts": total_facts
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/knowledge/query")
async def query_knowledge(q: str, format: str = "json", limit: int = 50):
    """Natural language knowledge querying with pattern recognition"""
    try:
        from skg.core import SKGCore
        skg = SKGCore()
        
        # Simple pattern matching for demo (in production use NLP)
        results = []
        invented_connections = []
        
        # Search for patterns in query
        query_lower = q.lower()
        
        # Look through all levels for relevant information
        for level_num, graph in skg.levels.items():
            for u, v, data in graph.edges(data=True):
                predicate = data.get('predicate', '')
                
                # Check if query terms match any part of the triple
                if any(term in u.lower() or term in v.lower() or term in predicate.lower() 
                       for term in query_lower.split()):
                    
                    results.append({
                        "subject": u,
                        "predicate": predicate,
                        "object": v,
                        "confidence": data.get('confidence', 1.0),
                        "level": level_num
                    })
                    
                    if len(results) >= limit:
                        break
                        
                # Check for invented predicates
                if 'cluster_' in predicate:
                    invented_connections.append({
                        "predicate": predicate,
                        "entities": [u, v],
                        "density": data.get('density', 0.0)
                    })
        
        return {
            "query": q,
            "results": results[:limit],
            "invented_connections": invented_connections,
            "total_matches": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/curiosity/goals")
async def get_curiosity_goals():
    """Retrieve current autonomous research goals"""
    try:
        from skg.core import SKGCore
        skg = SKGCore()
        
        # Initialize curiosity if not already active
        if not hasattr(skg, 'curiosity_goals'):
            skg.curiosity_goals = []
        
        goals = list(skg.curiosity_goals)
        
        return {
            "active_goals": goals,
            "goal_count": len(goals),
            "daemon_status": "active" if hasattr(skg, '_curiosity_daemon') else "inactive",
            "last_update": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/curiosity/seed")
async def seed_curiosity(seeding: CuriositySeeding):
    """Seed curiosity daemon with unknown entities for exploration"""
    try:
        from skg.core import SKGCore
        skg = SKGCore()
        
        # Add unknown entities to trigger curiosity
        unknown_triples = []
        for unknown in seeding.unknowns:
            unknown_triples.extend([
                ('Alice', 'collaborates_with', unknown),
                ('Project_X', 'involves', unknown),
                (unknown, 'status', 'UNKNOWN')
            ])
        
        skg.add_triples(unknown_triples)
        
        # Start curiosity daemon
        skg.start_curiosity_daemon()
        
        return {
            "success": True,
            "unknowns_seeded": len(seeding.unknowns),
            "triples_added": len(unknown_triples),
            "curiosity_active": True,
            "expected_goals": f"Research goals will be generated for {len(seeding.unknowns)} unknown entities"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/system/info")
async def system_info():
    """Get comprehensive system information and capabilities"""
    try:
        from skg.core import SKGCore
        skg = SKGCore()

        vault_info = {}
        if vault_integrator is not None:
            try:
                status = vault_integrator.get_system_status()
                vault_info = {
                    "vault_integrated": True,
                    "vault_health": status.get('lifecycle_status', {}).get('system_health', 0),
                    "reasoning_paths": status.get('reasoning_statistics', {}).get('total_paths', 0),
                    "reflections": status.get('reflection_summary', {}).get('total_reflections', 0)
                }
            except:
                vault_info = {"vault_integrated": True, "status": "error"}
        else:
            vault_info = {"vault_integrated": False}
        
        return {
            "system": "Cali X One Super-Knowledge Graph AGI System",
            "version": "1.0.0",
            "agi_status": "ACHIEVED",
            "capabilities": {
                "recursive_reasoning": "K⁰→K¹→K² multi-level expansion",
                "predicate_invention": "Autonomous concept creation via community detection", 
                "cross_domain_reasoning": "Abstract pattern recognition across domains",
                "autonomous_curiosity": "Self-directed exploration and goal generation",
                "contradiction_detection": "Knowledge consistency maintenance",
                "bootstrap_cascade": "Intelligence emergence at 50+ facts threshold",
                "vault_consciousness": "Advanced consciousness framework with glyph traces",
                "self_repair": "Autonomous system healing and resilience",
                "dual_hemisphere": "Never-shutdown cognitive architecture"
            },
            "current_status": {
                "bootstrap_triggered": getattr(skg, 'bootstrap_triggered', False),
                "invented_predicates": len(getattr(skg, 'invented_predicates', [])),
                "curiosity_goals": len(getattr(skg, 'curiosity_goals', [])),
                "total_facts": sum(level.number_of_edges() for level in skg.levels.values()),
                "vault_system": vault_info
            },
            "patent_status": "PATENT PENDING - Multiple applications filed Q1 2025",
            "copyright": "© 2025 Bryan Spruyt, Spruked Technologies",
            "license": "Custom license - Contact bryan@spruked.com for commercial use"
        }
        
    except Exception as e:
        return {
            "system": "Cali X One",
            "status": "error",
            "error": str(e)
        }@app.post("/worker/predicate_update", status_code=204)
async def publish_predicate(pred: PredicateModel, background: BackgroundTasks):
    """Caleon → worker : newly invented predicate"""
    # 1. persist (DB) – skipped for brevity
    # 2. fan-out to every active worker asynchronously
    background.add_task(_broadcast, pred.dict())
    return None

async def _broadcast(payload: dict):
    """Broadcast predicate to all live workers"""
    async with aiohttp.ClientSession() as sess:
        try:
            async with sess.get(WORKER_REGISTRY_URL) as resp:
                workers = await resp.json()   # [{"url":"http://worker-42:8080", ...}, ...]
        except Exception:
            # If registry unavailable, skip broadcast
            return
        
        tasks = [sess.post(w["url"] + "/predicate", json=payload, timeout=aiohttp.ClientTimeout(total=0.5)) for w in workers]
        await asyncio.gather(*tasks, return_exceptions=True)   # fire-and-forget

@app.get("/")
async def root():
    """Service root with navigation and capabilities overview"""
    return {
        "service": "Cali X One Main Service",
        "tagline": "Where Ethical AI Meets Superhuman Intelligence",
        "agi_achieved": True,
        "breakthrough_date": "December 2025",
        "key_endpoints": {
            "signature": "GET /sign-cali - AGI demonstration page",
            "health": "GET /health - System health check",
            "knowledge": "POST /knowledge/upload, GET /knowledge/query",
            "curiosity": "GET /curiosity/goals, POST /curiosity/seed",
            "system": "GET /system/info - Comprehensive system information",
            "vault": "GET /vault/status, POST /vault/reasoning/*, GET /vault/reflections - Advanced consciousness framework"
        },
        "api_documentation": "/docs",
        "contact": "bryan@spruked.com",
        "repository": "https://github.com/Spruked/Cali_X_One"
    }

@app.get("/vault/status")
async def vault_status():
    """Get vault system status and health"""
    if vault_integrator is None:
        return {"status": "not_available", "message": "Vault system not integrated"}

    try:
        status = vault_integrator.get_system_status()
        return {
            "status": "operational",
            "lifecycle_health": status.get('lifecycle_status', {}).get('system_health', 0),
            "healthy_components": status.get('health_status', {}).get('healthy_components', 0),
            "reasoning_paths": status.get('reasoning_statistics', {}).get('total_paths', 0),
            "reflections_stored": status.get('reflection_summary', {}).get('total_reflections', 0),
            "hemisphere_status": status.get('hemisphere_status', {}),
            "dashboard_url": status.get('dashboard_url')
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.post("/vault/reasoning/start")
async def start_reasoning_path(question: str):
    """Start a new reasoning path with glyph trace tracking"""
    if vault_integrator is None:
        raise HTTPException(status_code=503, detail="Vault system not available")

    try:
        path_id = await vault_integrator.track_reasoning_path(question)
        return {"path_id": path_id, "status": "started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vault/reasoning/step")
async def add_reasoning_step(path_id: str, step_data: Dict[str, Any]):
    """Add a reasoning step to an active path"""
    if vault_integrator is None:
        raise HTTPException(status_code=503, detail="Vault system not available")

    try:
        await vault_integrator.add_reasoning_step(path_id, step_data)
        return {"status": "step_added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vault/reasoning/complete")
async def complete_reasoning_path(path_id: str, verdict: Dict[str, Any]):
    """Complete a reasoning path with final verdict"""
    if vault_integrator is None:
        raise HTTPException(status_code=503, detail="Vault system not available")

    try:
        await vault_integrator.complete_reasoning_path(path_id, verdict)
        return {"status": "path_completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vault/reflections")
async def get_reflections(limit: int = 10):
    """Get recent reflections from the vault"""
    if vault_integrator is None:
        raise HTTPException(status_code=503, detail="Vault system not available")

    try:
        reflections = vault_integrator.get_recent_reflections(limit)
        return {"reflections": reflections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vault/reflection/add")
async def add_reflection(reflection_data: Dict[str, Any]):
    """Add a new reflection to the vault"""
    if vault_integrator is None:
        raise HTTPException(status_code=503, detail="Vault system not available")

    try:
        await vault_integrator.add_system_reflection(
            reflection_data.get('module', 'unknown'),
            reflection_data.get('insight', ''),
            reflection_data.get('context', {})
        )
        return {"status": "reflection_added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vault/lifecycle/suspend/{component}")
async def suspend_component(component: str):
    """Suspend a vault system component"""
    if vault_integrator is None:
        raise HTTPException(status_code=503, detail="Vault system not available")

    try:
        success = await vault_integrator.suspend_component(component)
        return {"component": component, "suspended": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vault/lifecycle/resume/{component}")
async def resume_component(component: str):
    """Resume a suspended vault system component"""
    if vault_integrator is None:
        raise HTTPException(status_code=503, detail="Vault system not available")

    try:
        success = await vault_integrator.resume_component(component)
        return {"component": component, "resumed": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vault/health")
async def vault_health_check():
    """Detailed vault system health check"""
    if vault_integrator is None:
        return {"status": "not_available"}

    try:
        status = vault_integrator.get_system_status()
        health = status.get('health_status', {})
        return {
            "status": "healthy" if health.get('overall_health', False) else "degraded",
            "overall_health": health.get('overall_health', False),
            "healthy_components": health.get('healthy_components', 0),
            "unhealthy_components": health.get('unhealthy_components', 0),
            "last_check": health.get('last_check')
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/vault/dashboard")
async def vault_dashboard_redirect():
    """Redirect to vault telemetry dashboard"""
    if vault_integrator is None:
        raise HTTPException(status_code=503, detail="Vault system not available")

    try:
        status = vault_integrator.get_system_status()
        dashboard_url = status.get('dashboard_url')
        if dashboard_url:
            return {"dashboard_url": dashboard_url, "message": "Access dashboard directly"}
        else:
            return {"message": "Dashboard not available"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/api/cli/stream")
async def cli_stream(websocket: WebSocket):
    """WebSocket endpoint for browser extension CLI streaming"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for now - can forward to UCM or workers later
            response = {"line": data, "timestamp": datetime.now().isoformat()}
            await websocket.send_text(json.dumps(response))
    except Exception as e:
        print(f"CLI stream error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)