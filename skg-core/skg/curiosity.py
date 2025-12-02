# cognition/skg/curiosity.py  (80 lines)
import networkx as nx
import threading, time, random
from collections import defaultdict

ENTROPY_THRESH = 0.75

def entropy(cluster):
    n = len(cluster)
    unknown = sum(1 for u, v in cluster if u == "UNKNOWN" or v == "UNKNOWN")
    return unknown / n if n else 0

def curiosity_loop(core, interval=30):
    while True:
        time.sleep(interval)
        
        # Scan all levels for UNKNOWN patterns
        for level_num in [0, 1, 2]:
            g = core.levels.get(level_num)
            if not g: continue
            
            # Look for UNKNOWN entities/relationships
            unknown_edges = []
            for u, v, d in g.edges(data=True):
                if "UNKNOWN" in str(u) or "UNKNOWN" in str(v) or "UNKNOWN" in str(d):
                    unknown_edges.append((u, v, d))
            
            # Generate goals for each UNKNOWN pattern
            for u, v, d in unknown_edges:
                if "UNKNOWN" in str(u):
                    goal = f"Research identity of {u} connected to {v}"
                elif "UNKNOWN" in str(v):
                    goal = f"Research identity of {v} connected to {u}"
                else:
                    goal = f"Research relationship {d} between {u} and {v}"
                # Store goals in core object
                if not hasattr(core, 'curiosity_goals'):
                    core.curiosity_goals = []
                core.curiosity_goals.append(goal)
                print(f"[Curiosity] spawned goal  {goal}")

def start_curiosity(core):
    threading.Thread(target=curiosity_loop, args=(core,), daemon=True).start()

def cali_add_goal(goal):
    # Placeholder: integrate with Cali's goal system
    print(f"[Curiosity] Would add goal: {goal}")