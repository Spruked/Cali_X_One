# cognition/skg/invent_predicate.py  (70 lines)
import networkx as nx
from networkx.algorithms import community

def maybe_invent_predicate(core, thresh=0.8):
    if len(core.levels) < 3:  # need at least 3 levels
        return
    
    # Prevent infinite recursion when adding invented predicates
    if getattr(core, '_inventing_predicate', False):
        return
        
    g = core.levels[2]                      # meta-meta graph
    if g.number_of_edges() < 5: return
    
    # Set flag to prevent recursion
    core._inventing_predicate = True
    try:
        # greedy modularity
        clusters = community.greedy_modularity_communities(g)
        for c in clusters:
            if len(c) < 3: continue
            density = nx.density(g.subgraph(c))
            if density > thresh:
                name = f"cluster_{abs(hash(tuple(sorted(c))))}"[:12]
                print(f"[SKG] invented predicate  {name} (density={density:.2f})")
                # inject back into K⁰ as a synthetic predicate
                core.add_triples([(name, "isA", "invented_predicate")])
                for n in c:
                    core.add_triples([(n, "member_of", name)])
    finally:
        # Clear flag
        core._inventing_predicate = False