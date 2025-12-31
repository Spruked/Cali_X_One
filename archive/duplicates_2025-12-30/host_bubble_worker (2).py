# host_bubble_worker.py - Worker template for Cali X One
from fastapi import FastAPI, Request
import networkx as nx

app = FastAPI()

# Local micro-SKG graph
worker_skg = nx.DiGraph()

@app.post("/predicate")
async def receive_predicate(req: Request):
    """Receive Caleon-born predicate and inject into local micro-SKG"""
    pred = await req.json()
    
    # 1. inject into local micro-SKG graph
    if len(pred["signature"]) >= 2:
        A, B = pred["signature"][0], pred["signature"][1]
        worker_skg.add_edge(A, B,
                            predicate=pred["name"],
                            confidence=pred["confidence"],
                            pid=pred["predicate_id"])
    
    # 2. immediately usable in next fallback
    return None

@app.get("/health")
async def health():
    return {"status": "alive", "edges": worker_skg.number_of_edges()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)