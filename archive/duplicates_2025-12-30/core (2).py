"""
Super-Knowledge-Graph core  –  real recursive layers, real blocks, real pruning
Drop-in replacement for yesterday's toy.
"""
import numpy as np
import networkx as nx
import sqlite3, json, os, pathlib
from sklearn.metrics.pairwise import cosine_similarity
from pybreaker import CircuitBreaker

# ----------  config ----------
MAX_DEPTH      = 3          # how many recursive levels
GNN_HIDDEN     = 32
PRUNE_THRESH   = 0.05       # percentile
DB_FILE        = pathlib.Path(os.environ.get("UCM_SKG_DB", "ucm_skg.db"))

# ----------  tiny utils ----------
def conn():
    DB_FILE.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_FILE)

def init_db():
    c = conn()
    for lvl in range(MAX_DEPTH):
        c.execute(f"CREATE TABLE IF NOT EXISTS level_{lvl}(i INT, j INT, weight REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS edges(source INT, predicate TEXT, target INT, weight REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS meta(depth INT)")
    c.commit(); c.close()

# ----------  Resilience Manager ----------
class ResilienceManager:
    def __init__(self):
        self.db_breaker = CircuitBreaker(
            fail_max=5,
            reset_timeout=60
        )
    
    def protected_db_call(self, query_func):
        return self.db_breaker.call(query_func)

# ----------  Bulkhead Isolation ----------
class Bulkhead:
    def __init__(self):
        from asyncio import Semaphore
        self.db_semaphore = Semaphore(10)  # Limit DB calls
        self.analytics_semaphore = Semaphore(5)  # Limit ML calls

# ----------  Sharding Manager ----------
class ShardingManager:
    def __init__(self):
        self.shard_map = self.load_shard_config()
    
    def load_shard_config(self):
        return {}  # Placeholder
    
    def get_shard(self, tenant_id: str) -> str:
        import hashlib
        hash_val = int(hashlib.md5(tenant_id.encode()).hexdigest(), 16)
        return f"shard_{hash_val % 64}"

# ----------  Tiered Storage ----------
class TieredStorage:
    def __init__(self):
        self.hot = None  # Redis placeholder
        self.warm = None  # PostgreSQL placeholder
        self.cold = None  # S3 placeholder
    
    def get_triple(self, triple_id: str, age_days: int):
        if age_days < 7:
            return None  # hot.get
        elif age_days < 90:
            return None  # warm.get
        else:
            return None  # cold.get

# ----------  ML Ops Manager ----------
class MLOpsManager:
    def __init__(self):
        import mlflow
        mlflow.set_tracking_uri("postgresql://mlflow:pass@db:5432/mlflow")
    
    def auto_train_embeddings(self, tenant_id: str):
        pass  # Placeholder

# ----------  Event Sourcing Manager ----------
class EventSourcingManager:
    def __init__(self):
        self.streams = None  # KafkaStreams placeholder
    
    def process_triple_events(self):
        pass  # Placeholder

# ----------  Compliance Manager ----------
class ComplianceManager:
    def __init__(self, db_url: str):
        self.db_url = db_url
    
    def enforce_retention_policy(self, tenant_id: str):
        pass  # Placeholder
    
    def gdpr_erase(self, tenant_id: str, user_id: str):
        pass  # Placeholder

# ----------  SKG engine ----------

# ----------  SKG engine ----------
class SKGCore:
    def __init__(self, tenant_id: str = "default"):
        init_db()
        self.tenant_id = tenant_id
        self.levels   = {}          # nx graphs
        self.adjs     = {}          # numpy matrices
        self.depth    = 0
        self.total_edges = 0        # MISSING COUNTER
        self.bootstrapped = False   # MISSING FLAG
        self.curiosity_goals = []   # track spawned goals
        self.curiosity_daemon = None # daemon thread
        
        # Enterprise components
        self.resilience = ResilienceManager()
        self.bulkhead = Bulkhead()
        self.sharding = ShardingManager()
        self.tiered_storage = TieredStorage()
        self.invented_predicates = []
        self.ml_ops = MLOpsManager()
        self.event_sourcing = EventSourcingManager()
        self.compliance = ComplianceManager("dbname=skg user=skg")  # Placeholder connection

    # 1.  ingest base triples → K⁰
    async def add_triples(self, triples):
        # Use bulkhead for isolation
        async def _add():
            # Initialize graph if it doesn't exist
            if 0 not in self.levels:
                self.levels[0] = nx.DiGraph()
            
            g = self.levels[0]
            old_count = g.number_of_edges()
            
            # Add new triples to existing graph
            for s, p, o in triples:
                g.add_edge(s, o, predicate=p, weight=1.0)
            
            self.total_edges += len(triples)
            print(f"[SKG] added {len(triples)} edges → total {self.total_edges}")
            
            # Store in tiered storage
            for s, p, o in triples:
                await self.tiered_storage.store_triple(f"{s}_{p}_{o}", {"subject": s, "predicate": p, "object": o})
            
            # Emit event
            await self.event_sourcing.emit_event("skg.triple.created", {
                "tenant_id": self.tenant_id,
                "triples": triples
            })
            
            self.adjs[0] = nx.adjacency_matrix(g).todense().astype(float)
            self.depth = 1
            detect_and_repair(self)
            
            # ---- FIXED BOOTSTRAP CASCADE ----
            if self.total_edges >= 50 and not self.bootstrapped:
                print("[SKG] 50+ FACTS REACHED – FULL RECURSIVE CASCADE INITIATED")
                await self.expand_recursive()
                maybe_invent_predicate(self)
                start_curiosity(self)
                self.bootstrapped = True
            else:
                # Light recursive expansion for real-time processing
                await self.expand_recursive()
        
        # Protect with circuit breaker
        return await self.resilience.protected_db_call(_add)

    # 2.  recursive expansion  Kᵏ → Kᵏ⁺¹
    async def expand_recursive(self):
        if getattr(self, '_expanding', False):
            return
        self._expanding = True
        
        while self.depth < MAX_DEPTH:
            k = self.depth
            prev = self.adjs[k-1]

            # local cross-links  C
            C = self._cross_links(prev)
            # non-local proposals X
            X = await self._propose_edges(prev)
            # new adjacency
            new_adj = prev + C + X
            new_adj = self._prune(new_adj)

            self.adjs[k] = new_adj
            self.levels[k] = nx.from_numpy_array(new_adj, create_using=nx.DiGraph)
            self.depth += 1
            print(f"[SKG] built level {k}  |V|={new_adj.shape[0]}  density={new_adj.sum()/new_adj.size:.3f}")
        maybe_invent_predicate(self)
        
    async def enforce_compliance(self):
        """Enforce retention and compliance policies"""
        await self.compliance.enforce_retention_policy(self.tenant_id)
    
    async def gdpr_erase_user(self, user_id: str):
        """GDPR right to erasure"""
        await self.compliance.gdpr_erase(self.tenant_id, user_id)

    # 3.  cross-links = shared nodes
    def _cross_links(self, adj):
        g = nx.from_numpy_array(adj, create_using=nx.DiGraph)
        c = nx.adjacency_matrix(g).todense() * 0.2   # dampen
        return c

    # 4.  non-local proposals via GNN attention
    def _propose_edges(self, adj):
        # Pure CPU method: cosine similarity on adjacency matrix
        if adj.size == 0 or adj.sum() == 0:
            return np.zeros_like(adj)
        
        # Compute cosine similarity between rows (node representations)
        similarities = cosine_similarity(adj)
        
        # Flatten to get scores
        scores = similarities.flatten()
        
        # Threshold at 95th percentile
        threshold = np.percentile(scores, 95)
        proposals = (scores > threshold).astype(float).reshape(adj.shape) * 0.15
        
        return proposals

    # 5.  prune low weights
    def _prune(self, adj):
        thresh = np.percentile(adj[adj>0], PRUNE_THRESH*100)
        adj[adj < thresh] = 0
        return adj

    # 6.  persist level to SQLite
    def _persist_level(self, lvl, adj):
        c = conn()
        c.execute(f"DELETE FROM level_{lvl}")
        rows = [(int(i), int(j), float(adj[i,j]))
                for i in range(adj.shape[0]) for j in range(adj.shape[1]) if adj[i,j]>0]
        c.executemany(f"INSERT INTO level_{lvl} VALUES (?,?,?)", rows)
        
        # Also populate edges table for UCM compatibility
        c.execute("DELETE FROM edges")
        rows_edges = [(int(i), 'related', int(j), float(adj[i,j]))
                      for i in range(adj.shape[0]) for j in range(adj.shape[1]) if adj[i,j]>0]
        c.executemany("INSERT INTO edges VALUES (?,?,?,?)", rows_edges)
        
        c.execute("REPLACE INTO meta(depth) VALUES (?)", (lvl+1,))
        c.commit(); c.close()

    # 7.  assemble full SKG block matrix
    def block_matrix(self):
        blocks = [[self.adjs.get(min(i,j), np.zeros_like(self.adjs[0])) if abs(i-j)<=1
                   else np.zeros_like(self.adjs[0]) for j in range(self.depth)]
                  for i in range(self.depth)]
        return np.block(blocks)

    # Curiosity daemon control methods
    def start_curiosity_daemon(self):
        """Start the curiosity daemon if not already running"""
        # Turn OFF curiosity for now to avoid docker issues
        return
        
        import threading
        if self.curiosity_daemon is None or not self.curiosity_daemon.is_alive():
            from .curiosity import curiosity_loop
            self.curiosity_daemon = threading.Thread(
                target=curiosity_loop, 
                args=(self,), 
                daemon=True
            )
            self.curiosity_daemon.start()

    def stop_curiosity_daemon(self):
        """Stop the curiosity daemon"""
        if self.curiosity_daemon and self.curiosity_daemon.is_alive():
            # Note: daemon threads will stop when main program exits
            # For more control, we'd need a stop event mechanism
            pass

# ----------  Flask service wrapper (same URLs as before) ----------
# Import Flask for web service
from flask import Flask, request, jsonify

# Import our SKG enhancement modules
from .contradiction import detect_and_repair
from .invent_predicate import maybe_invent_predicate
from .curiosity import start_curiosity
class SKGService:
    def __init__(self, db_path=None):
        if db_path: os.environ["UCM_SKG_DB"] = db_path
        self.core = SKGCore()
        self.app  = Flask("skg")
        self._routes()

    def _routes(self):
        self.app.add_url_rule("/add",  "add",  self._add,  methods=["POST"])
        self.app.add_url_rule("/query","query",self._query,methods=["GET"])

    def _add(self):
        data = request.get_json(force=True)
        triples = [(data["s"], data["p"], data["o"])]
        self.core.add_triples(triples)
        self.core.expand_recursive()
        return jsonify({"status":"ok", "depth":self.core.depth})

    def _query(self):
        pat = json.loads(request.args.get("pat"))
        # for now just return base-level edges (can extend to meta later)
        g = self.core.levels[0]
        match = [(u,v,d) for u,v,d in g.edges(data=True)
                 if (pat[0] is None or u==pat[0]) and
                    (pat[1] is None or d.get("predicate")==pat[1]) and
                    (pat[2] is None or v==pat[2])]
        return jsonify(match[:int(request.args.get("k", 10))])
    def start(self, port=7777):
        start_curiosity(self.core)
        self.app.run(host="0.0.0.0", port=port, debug=False)
        self.app.run(host="0.0.0.0", port=port, debug=False)

    def add(self, s, p, o, weight=1.0):
        self.core.add_triples([(s,p,o)])
        self.core.expand_recursive()
        # ---- per-edge bootstrap trigger ----
        if self.core.levels[0].number_of_edges() % 50 == 0 and self.core.levels[0].number_of_edges() > 0:
            print(f"[SKG] ➜  {self.core.levels[0].number_of_edges()} base facts – bootstrap")
            self.core.expand_recursive()
            maybe_invent_predicate(self.core)
            start_curiosity(self.core)
        
        # ---- per-edge bootstrap trigger ----
        if self.core.levels[0].number_of_edges() % 50 == 0 and self.core.levels[0].number_of_edges() > 0:
            print(f"[SKG] ➜  {self.core.levels[0].number_of_edges()} base facts – bootstrap")
            self.core.expand_recursive()
            maybe_invent_predicate(self.core)
            start_curiosity(self.core)

    def query(self, pat, k=10):
        g = self.core.levels[0]
        match = [(u,v,d) for u,v,d in g.edges(data=True)
                 if (pat[0] is None or u==pat[0]) and
                    (pat[1] is None or d.get("predicate")==pat[1]) and
                    (pat[2] is None or v==pat[2])]
        return match[:k]

# ----------  convenience client ----------
class Knowledge:
    def __init__(self, db_path=None):
        self.svc = SKGService(db_path)
    def add(self, s, p, o, w=1.0):
        self.svc.core.add_triples([(s,p,o)])
        self.svc.core.expand_recursive()
    def query(self, pat, k=10):
        return self.svc._query_internal(pat, k)
    def _query_internal(self, pat, k):
        g = self.svc.core.levels[0]
        match = [(u,v,d) for u,v,d in g.edges(data=True)
                 if (pat[0] is None or u==pat[0]) and
                    (pat[1] is None or d.get("predicate")==pat[1]) and
                    (pat[2] is None or v==pat[2])]
        return match[:k]