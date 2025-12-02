# cognition/skg/contradiction.py  (60 lines)
MUTEX_PRED = {"loves": "hates", "bornIn": "diedIn", "worksAt": "firedFrom"}

def detect_and_repair(core):
    g = core.levels[0]          # base graph
    removals = []
    for s, o, d in g.edges(data=True):
        p = d.get("predicate")
        if p and p in MUTEX_PRED:
            opposite = MUTEX_PRED[p]
            # Check for opposite predicate on same edge
            for s2, o2, d2 in g.edges(data=True):
                if s2 == s and o2 == o and d2.get("predicate") == opposite:
                    # Remove lower weight edge
                    weight1 = d.get("weight", 1.0)
                    weight2 = d2.get("weight", 1.0)
                    if weight1 >= weight2:
                        removals.append((s2, o2))
                    else:
                        removals.append((s, o))
                    print(f"[SKG] repaired contradiction {s}-{p}/{opposite}-{o}")
    # Remove contradictory edges
    for s, o in removals:
        if g.has_edge(s, o):
            g.remove_edge(s, o)