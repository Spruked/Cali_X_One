"""
Worker Registry API
Manages worker registration, heartbeats, and DMN/DSN coordination
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
import json

router = APIRouter()

# In-memory worker registry (replace with Redis/DB in production)
worker_registry = {}
heartbeat_timeout = 30  # seconds

class WorkerRegistration(BaseModel):
    worker_id: str
    worker_type: str  # "josephine", "bubble_worker", etc.
    capabilities: List[str]
    endpoint: str
    metadata: Optional[Dict[str, Any]] = {}

class WorkerHeartbeat(BaseModel):
    worker_id: str
    status: str = "alive"
    load: float = 0.0
    last_task: Optional[str] = None

@router.post("/register")
async def register_worker(registration: WorkerRegistration):
    """Register a new worker"""
    worker_registry[registration.worker_id] = {
        "registration": registration.dict(),
        "last_heartbeat": datetime.now(),
        "status": "registered"
    }
    return {"status": "registered", "worker_id": registration.worker_id}

@router.post("/heartbeat")
async def worker_heartbeat(heartbeat: WorkerHeartbeat):
    """Receive heartbeat from worker"""
    if heartbeat.worker_id not in worker_registry:
        raise HTTPException(status_code=404, detail="Worker not registered")

    worker_registry[heartbeat.worker_id].update({
        "last_heartbeat": datetime.now(),
        "status": heartbeat.status,
        "load": heartbeat.load,
        "last_task": heartbeat.last_task
    })
    return {"status": "acknowledged"}

@router.get("/list")
async def list_workers():
    """List all registered workers with status"""
    current_time = datetime.now()

    workers = []
    for worker_id, data in worker_registry.items():
        last_heartbeat = data["last_heartbeat"]
        is_alive = (current_time - last_heartbeat).seconds < heartbeat_timeout

        workers.append({
            "worker_id": worker_id,
            "status": "alive" if is_alive else "dead",
            "last_heartbeat": last_heartbeat.isoformat(),
            "registration": data["registration"],
            "current_load": data.get("load", 0.0),
            "last_task": data.get("last_task")
        })

    return {"workers": workers, "total": len(workers)}

@router.delete("/unregister/{worker_id}")
async def unregister_worker(worker_id: str):
    """Unregister a worker"""
    if worker_id not in worker_registry:
        raise HTTPException(status_code=404, detail="Worker not found")

    del worker_registry[worker_id]
    return {"status": "unregistered", "worker_id": worker_id}

@router.get("/dmn/{worker_id}")
async def get_dmn_status(worker_id: str):
    """Get DMN (Decision Management Network) status for worker"""
    if worker_id not in worker_registry:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Placeholder - integrate with actual DMN logic
    return {
        "worker_id": worker_id,
        "dmn_status": "active",
        "connected_workers": len(worker_registry) - 1,
        "network_health": "good"
    }

@router.get("/dsn/{worker_id}")
async def get_dsn_status(worker_id: str):
    """Get DSN (Distributed Service Network) status for worker"""
    if worker_id not in worker_registry:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Placeholder - integrate with actual DSN logic
    return {
        "worker_id": worker_id,
        "dsn_status": "active",
        "service_endpoints": list(worker_registry.keys()),
        "network_load": sum(w.get("load", 0.0) for w in worker_registry.values())
    }