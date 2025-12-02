"""
Super-Knowledge-Graph core  –  real recursive layers, real blocks, real pruning
Drop-in replacement for yesterday's toy.
"""
import numpy as np
import torch, torch.nn as nn
import networkx as nx
import sqlite3, json, os, pathlib
from torch_geometric.utils import dense_to_sparse
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv

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
    c.execute("CREATE TABLE IF NOT EXISTS meta(depth INT)")
    c.commit(); c.close()

# ----------  GNN edge scorer ----------
class EdgeScoreGNN(nn.Module):
    def __init__(self, in_dim, hidden=GNN_HIDDEN):
        super().__init__()
        self.conv1 = GCNConv(in_dim, hidden)
        self.conv2 = GCNConv(hidden, 1)
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        return torch.sigmoid(self.conv2(x, edge_index)).squeeze(-1)

# ----------  SKG engine ----------
class SKGCore:
    def __init__(self):
        init_db()
        self.levels   = {}          # nx graphs
        self.adjs     = {}          # numpy matrices
        self.depth    = 0
        self.total_edges = 0        # MISSING COUNTER
        self.bootstrapped = False   # MISSING FLAG
        self.curiosity_goals = []   # track spawned goals
        self.curiosity_daemon = None # daemon thread

    # 1.  ingest base triples → K⁰
    def add_triples(self, triples):
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
        
        self.adjs[0] = nx.adjacency_matrix(g).todense().astype(float)
        self.depth = 1
        detect_and_repair(self)
        
        # ---- FIXED BOOTSTRAP CASCADE ----
        if self.total_edges >= 50 and not self.bootstrapped:
            print("[SKG] 50+ FACTS REACHED – FULL RECURSIVE CASCADE INITIATED")
            self.expand_recursive()
            maybe_invent_predicate(self)
            start_curiosity(self)
            self.bootstrapped = True
        else:
            # Light recursive expansion for real-time processing
            self.expand_recursive()

    # 2.  recursive expansion  Kᵏ → Kᵏ⁺¹
    def expand_recursive(self):
        if getattr(self, '_expanding', False):
            return
        self._expanding = True
        
        while self.depth < MAX_DEPTH:
            k = self.depth
            prev = self.adjs[k-1]

            # local cross-links  C
            C = self._cross_links(prev)
            # non-local proposals X
            X = self._propose_edges(prev)
            # new adjacency
            new_adj = prev + C + X
            new_adj = self._prune(new_adj)

            self.adjs[k] = new_adj
            self.levels[k] = nx.from_numpy_array(new_adj, create_using=nx.DiGraph)
            self.depth += 1
            print(f"[SKG] built level {k}  |V|={new_adj.shape[0]}  density={new_adj.sum()/new_adj.size:.3f}")
        maybe_invent_predicate(self)
        
        self._expanding = False

    # 3.  cross-links = shared nodes
    def _cross_links(self, adj):
        g = nx.from_numpy_array(adj, create_using=nx.DiGraph)
        c = nx.adjacency_matrix(g).todense() * 0.2   # dampen
        return c

    # 4.  non-local proposals via GNN attention
    def _propose_edges(self, adj):
        g = nx.from_numpy_array(adj, create_using=nx.DiGraph)
        edge_index, _ = dense_to_sparse(torch.tensor(adj, dtype=torch.float))
        x = torch.eye(adj.shape[0])
        model = EdgeScoreGNN(x.size(1))
        opt   = torch.optim.Adam(model.parameters(), lr=0.01)
        # dummy target = degree
        target = torch.tensor(list(dict(g.degree()).values()), dtype=torch.float)
        for _ in range(10):  # reduced for testing
            opt.zero_grad()
            out = model(x, edge_index)
            loss = nn.MSELoss()(out, target)
            loss.backward(); opt.step()
        with torch.no_grad():
            scores = model(x, edge_index).numpy()
        proposals = (scores > np.percentile(scores, 95)).astype(float) * 0.15
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