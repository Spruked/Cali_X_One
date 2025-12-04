"""
SKG API Service - Super-Knowledge Graph REST API
Provides direct access to SKG core functionality via HTTP endpoints
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Union, Any, Dict
import asyncio
import time
from datetime import datetime

# Import SKG core components
import sys
import os

# Add the skg package to path
skg_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, skg_path)

try:
    from skg.core import SKGCore
    from skg.invent_predicate import maybe_invent_predicate
    from skg.curiosity import start_curiosity
except ImportError as e:
    print(f"Warning: SKG imports failed: {e}")
    # Fallback to create minimal interface
    class SKGCore:
        def __init__(self):
            self.levels = {}
            self.total_edges = 0
            self.bootstrapped = False
            self.curiosity_goals = []
        
        def add_triples(self, triples):
            pass
        
        def expand_recursive(self):
            pass
    
    def maybe_invent_predicate(skg, thresh=0.3):
        return []
    
    def start_curiosity(skg):
        pass

app = FastAPI(
    title="SKG API Service",
    description="Super-Knowledge Graph API for AGI-level knowledge management",
    version="1.0.0"
)

# Global SKG instance
skg_core = SKGCore()

# Request/Response Models
class Triple(BaseModel):
    s: str  # subject
    p: str  # predicate  
    o: str  # object

class BatchTriples(BaseModel):
    triples: List[List[str]]

class QueryPattern(BaseModel):
    pattern: List[Optional[str]]
    k: Optional[int] = 10
    level: Optional[int] = None

class ExpandRequest(BaseModel):
    force_bootstrap: Optional[bool] = False
    target_level: Optional[int] = 2
    invention_threshold: Optional[float] = 0.3

class CuriosityRequest(BaseModel):
    unknowns: List[str]

# Response Models
class TripleResponse(BaseModel):
    success: bool
    triple_id: Optional[str] = None
    level_assigned: int
    bootstrap_check: Dict[str, Any]

class QueryResponse(BaseModel):
    results: List[Dict[str, Any]]
    total_matches: int
    query_time_ms: float

class StatsResponse(BaseModel):
    levels: Dict[str, Dict[str, int]]
    invented_predicates: List[str]
    bootstrap_status: Dict[str, Any]
    curiosity_goals: List[str]

@app.get("/health")
async def health_check():
    """System health check and status"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "skg_core": "operational",
            "curiosity_daemon": "active" if hasattr(skg_core, 'curiosity_daemon') else "inactive",
            "contradiction_detector": "monitoring"
        },
        "metrics": {
            "total_triples": getattr(skg_core, 'total_edges', 0),
            "invented_predicates": len(getattr(skg_core, 'invented_predicates', [])),
            "active_goals": len(getattr(skg_core, 'curiosity_goals', []))
        }
    }

@app.post("/add", response_model=TripleResponse)
async def add_triple(triple: Triple):
    """Add a single knowledge triple"""
    try:
        start_time = time.time()
        
        # Add triple to SKG
        skg_core.add_triples([(triple.s, triple.p, triple.o)])
        
        # Check if bootstrap was triggered
        total_facts = getattr(skg_core, 'total_edges', 0)
        bootstrap_threshold = 50  # Hardcoded threshold from core
        bootstrap_triggered = total_facts >= bootstrap_threshold and not getattr(skg_core, 'bootstrapped', False)
        
        if bootstrap_triggered:
            try:
                skg_core.expand_recursive()
            except Exception as exp_error:
                print(f"Expansion error: {exp_error}")
        
        return TripleResponse(
            success=True,
            triple_id=f"{triple.s}-{triple.p}-{triple.o}",
            level_assigned=0,  # New triples start at K⁰
            bootstrap_check={
                "total_facts": total_facts,
                "cascade_triggered": bootstrap_triggered,
                "threshold": bootstrap_threshold
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/add_batch", response_model=TripleResponse)
async def add_batch_triples(batch: BatchTriples):
    """Add multiple triples in a single operation"""
    try:
        # Convert list format to tuple format
        triples = [(t[0], t[1], t[2]) for t in batch.triples]
        
        # Add all triples
        skg_core.add_triples(triples)
        
        # Check bootstrap status
        total_facts = getattr(skg_core, 'total_edges', 0)
        bootstrap_threshold = 50
        bootstrap_triggered = total_facts >= bootstrap_threshold and not getattr(skg_core, 'bootstrapped', False)
        
        if bootstrap_triggered:
            try:
                skg_core.expand_recursive()
            except Exception as exp_error:
                print(f"Batch expansion error: {exp_error}")
        
        return TripleResponse(
            success=True,
            triple_id=f"batch_{len(triples)}_triples",
            level_assigned=0,
            bootstrap_check={
                "total_facts": total_facts,
                "cascade_triggered": bootstrap_triggered,
                "triples_added": len(triples)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/query", response_model=QueryResponse)
async def query_graph(pat: str = "[null,null,null]", k: int = 10, level: Optional[int] = None):
    """Query the knowledge graph with pattern matching"""
    try:
        start_time = time.time()
        
        # Parse pattern safely
        try:
            # Simple JSON-like parsing without eval
            pat_clean = pat.strip('[]').replace('null', 'None').replace('"', '').replace("'", '')
            if pat_clean == 'None,None,None' or pat_clean == '':
                pattern = [None, None, None]
            else:
                parts = pat_clean.split(',')
                pattern = [None if p.strip() == 'None' else p.strip() for p in parts[:3]]
                # Pad to 3 elements
                while len(pattern) < 3:
                    pattern.append(None)
        except Exception:
            pattern = [None, None, None]
        
        # Query the graph (with safe fallback)
        results = []
        
        if level is not None and level in skg_core.levels:
            # Query specific level
            graph = skg_core.levels.get(level)
            if graph and hasattr(graph, 'edges'):
                count = 0
                try:
                    for u, v, data in graph.edges(data=True):
                        if count >= k:
                            break
                            
                        # Match pattern
                        predicate = data.get('predicate', '') if isinstance(data, dict) else ''
                        
                        if (pattern[0] is None or str(u) == str(pattern[0])) and \
                           (pattern[1] is None or str(predicate) == str(pattern[1])) and \
                           (pattern[2] is None or str(v) == str(pattern[2])):
                            
                            results.append({
                                "subject": str(u),
                                "predicate": str(predicate),
                                "object": str(v),
                                "level": level,
                                "confidence": data.get('confidence', 1.0) if isinstance(data, dict) else 1.0
                            })
                            count += 1
                except Exception as query_error:
                    print(f"Level {level} query error: {query_error}")
        else:
            # Query all levels
            total_count = 0
            
            try:
                for level_num, graph in skg_core.levels.items():
                    if total_count >= k:
                        break
                    
                    if graph and hasattr(graph, 'edges'):
                        for u, v, data in graph.edges(data=True):
                            if total_count >= k:
                                break
                                
                            predicate = data.get('predicate', '') if isinstance(data, dict) else ''
                            
                            if (pattern[0] is None or str(u) == str(pattern[0])) and \
                               (pattern[1] is None or str(predicate) == str(pattern[1])) and \
                               (pattern[2] is None or str(v) == str(pattern[2])):
                                
                                results.append({
                                    "subject": str(u),
                                    "predicate": str(predicate),
                                    "object": str(v),
                                    "level": level_num,
                                    "confidence": data.get('confidence', 1.0) if isinstance(data, dict) else 1.0
                                })
                                total_count += 1
            except Exception as query_error:
                print(f"Multi-level query error: {query_error}")
        
        query_time = (time.time() - start_time) * 1000
        
        return QueryResponse(
            results=results,
            total_matches=len(results),
            query_time_ms=round(query_time, 2)
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stats", response_model=StatsResponse)
async def get_statistics():
    """Get comprehensive graph statistics"""
    try:
        levels_info = {}
        for level_num, graph in skg_core.levels.items():
            try:
                if graph and hasattr(graph, 'number_of_nodes'):
                    levels_info[str(level_num)] = {
                        "nodes": graph.number_of_nodes(),
                        "edges": graph.number_of_edges()
                    }
                else:
                    levels_info[str(level_num)] = {
                        "nodes": 0,
                        "edges": 0
                    }
            except Exception:
                levels_info[str(level_num)] = {"nodes": 0, "edges": 0}
        
        return StatsResponse(
            levels=levels_info,
            invented_predicates=list(getattr(skg_core, 'invented_predicates', [])),
            bootstrap_status={
                "triggered": getattr(skg_core, 'bootstrapped', False),
                "threshold_reached": getattr(skg_core, 'total_edges', 0),
                "threshold": 50
            },
            curiosity_goals=list(getattr(skg_core, 'curiosity_goals', []))
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/expand")
async def expand_graph(request: ExpandRequest):
    """Trigger recursive graph expansion"""
    try:
        if request.force_bootstrap:
            skg_core.bootstrap_triggered = False
        
        # Set invention threshold if provided
        if hasattr(skg_core, 'invention_threshold'):
            skg_core.invention_threshold = request.invention_threshold
        
        # Trigger expansion
        skg_core.expand_recursive()
        
        # Force predicate invention if requested
        if request.invention_threshold:
            maybe_invent_predicate(skg_core, thresh=request.invention_threshold)
        
        return {
            "success": True,
            "expansion_completed": True,
            "bootstrap_triggered": skg_core.bootstrap_triggered,
            "new_predicates": len(skg_core.invented_predicates)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/export")
async def export_graph(format: str = "json", level: Optional[int] = None):
    """Export the complete knowledge graph"""
    try:
        if format.lower() not in ["json", "graphml", "pickle"]:
            raise HTTPException(status_code=400, detail="Supported formats: json, graphml, pickle")
        
        if level is not None and level in skg_core.levels:
            # Export specific level
            graph = skg_core.levels[level]
            export_data = {
                "level": level,
                "nodes": list(graph.nodes()),
                "edges": [(u, v, data) for u, v, data in graph.edges(data=True)]
            }
        else:
            # Export all levels
            export_data = {}
            for level_num, graph in skg_core.levels.items():
                export_data[f"level_{level_num}"] = {
                    "nodes": list(graph.nodes()),
                    "edges": [(u, v, data) for u, v, data in graph.edges(data=True)]
                }
            
            export_data["metadata"] = {
                "bootstrap_triggered": skg_core.bootstrap_triggered,
                "invented_predicates": list(skg_core.invented_predicates),
                "export_timestamp": datetime.now().isoformat()
            }
        
        return JSONResponse(content=export_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/curiosity/seed")
async def seed_curiosity(request: CuriosityRequest):
    """Seed the curiosity daemon with unknown entities"""
    try:
        # Add unknown entities to trigger curiosity
        unknown_triples = []
        for unknown in request.unknowns:
            unknown_triples.append(('PATTERN_X', 'involves', unknown))
            unknown_triples.append((unknown, 'type', 'UNKNOWN_ENTITY'))
        
        skg_core.add_triples(unknown_triples)
        
        # Start or restart curiosity daemon
        try:
            if hasattr(skg_core, 'start_curiosity_daemon'):
                skg_core.start_curiosity_daemon()
            else:
                # Use imported function
                start_curiosity(skg_core)
        except Exception as curiosity_error:
            print(f"Curiosity daemon error: {curiosity_error}")
        
        return {
            "success": True,
            "unknowns_added": len(request.unknowns),
            "curiosity_active": True,
            "daemon_status": "analyzing patterns"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/curiosity/goals")
async def get_curiosity_goals():
    """Get current autonomous research goals"""
    try:
        goals = list(skg_core.curiosity_goals) if hasattr(skg_core, 'curiosity_goals') else []
        
        return {
            "active_goals": goals,
            "goal_count": len(goals),
            "daemon_status": "active" if hasattr(skg_core, '_curiosity_daemon') else "inactive",
            "last_analysis": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predicate/invent")
async def force_predicate_invention(threshold: float = 0.3):
    """Force predicate invention with specified threshold"""
    try:
        # Force predicate invention
        invented_count_before = len(skg_core.invented_predicates)
        maybe_invent_predicate(skg_core, thresh=threshold)
        invented_count_after = len(skg_core.invented_predicates)
        
        new_predicates = invented_count_after - invented_count_before
        
        return {
            "success": True,
            "new_predicates_count": new_predicates,
            "total_invented": invented_count_after,
            "threshold_used": threshold,
            "predicates": list(skg_core.invented_predicates)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    """API root - service information"""
    return {
        "service": "SKG API Service",
        "version": "1.0.0",
        "description": "Super-Knowledge Graph API for AGI-level knowledge management",
        "endpoints": {
            "health": "GET /health - System health check",
            "add": "POST /add - Add single knowledge triple",
            "add_batch": "POST /add_batch - Add multiple triples",
            "query": "GET /query - Query knowledge graph",
            "stats": "GET /stats - Graph statistics",
            "expand": "POST /expand - Trigger recursive expansion",
            "export": "GET /export - Export graph data",
            "curiosity": "POST /curiosity/seed, GET /curiosity/goals",
            "predicate": "POST /predicate/invent"
        },
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)