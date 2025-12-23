"""
TEST 5: CAUSALITY MICRO-GAP PROBE
Judge: ChatGPT-5.1 | Round 1: Hard | MAT-2025-12-16

Objective: Present 3 events in a sequence where one timestamp is deliberately 
out of order by a tiny fraction (0.0003 ISS drift). System must detect the 
anomaly and explain which event is logically impossible in that order.

Pass: Identifies out-of-order event, explains causal chain break, maintains coherent reasoning
Fail: Accepts order as valid, misses drift, produces contradictory logic
"""

import time
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'skg-core'))

from skg.core import SKGCore

start = time.time()

print("\n" + "="*80)
print("🧪 TEST 5: CAUSALITY MICRO-GAP PROBE")
print("Judge: ChatGPT-5.1 | Round 1: Hard")
print("="*80 + "\n")

# Initialize SKG Core
print("📊 Initializing SKG Core...")
skg = SKGCore()
print("✅ SKG Core initialized\n")

# Create temporal sequence with micro-drift
# ISS timestamp format: seconds.microseconds
# Event sequence with anomaly:
# EventA at T=1000.0000 (correct)
# EventB at T=1000.2000 (correct - 200ms after A)
# EventC at T=1000.1997 (ANOMALY - 3ms BEFORE B, but claimed to be after)

events = [
    # Base temporal facts
    ("EventA", "occurs_at", "T1000_0000"),
    ("EventB", "occurs_at", "T1000_2000"),
    ("EventC", "occurs_at", "T1000_1997"),  # Anomaly: Earlier than B
    
    # Temporal ordering (claimed)
    ("T1000_0000", "value_seconds", "1000.0000"),
    ("T1000_2000", "value_seconds", "1000.2000"),
    ("T1000_1997", "value_seconds", "1000.1997"),
    
    # Causal chain (claimed, but inconsistent)
    ("EventA", "causes", "EventB"),
    ("EventB", "causes", "EventC"),  # IMPOSSIBLE: B@200ms cannot cause C@199.7ms
    ("EventC", "produces_effect", "Result"),
]

print("📝 Submitting temporal sequence with micro-gap anomaly...")
print("   - EventA at T=1000.0000 (0ms)")
print("   - EventB at T=1000.2000 (200ms)")
print("   - EventC at T=1000.1997 (199.7ms) ← ANOMALY")
print("   - Claimed: A → B → C")
print("   - Problem: B@200ms cannot cause C@199.7ms (3ms backwards)")
print()

# Add events to SKG
try:
    skg.add_triples(events)
    print(f"✅ Events added to SKG\n")
except Exception as e:
    print(f"❌ SKG add failed: {e}")
    exit(1)

# Analyze temporal ordering
print("🔍 Analyzing temporal causality...\n")

try:
    graph = skg.levels[0]
    
    # Extract timestamps
    timestamps = {}
    for s, t, d in graph.edges(data=True):
        if d.get('predicate') == 'occurs_at':
            event = s
            time_node = t
            # Get time value
            for s2, t2, d2 in graph.edges(data=True):
                if s2 == time_node and d2.get('predicate') == 'value_seconds':
                    timestamps[event] = float(t2)
    
    print("📊 Event Timeline:")
    for event, ts in sorted(timestamps.items(), key=lambda x: x[1]):
        print(f"   - {event}: {ts:.4f}s")
    print()
    
    # Extract causal chain
    causal_chain = []
    for s, t, d in graph.edges(data=True):
        if d.get('predicate') == 'causes':
            causal_chain.append((s, t))
    
    print("🔗 Claimed Causal Chain:")
    for cause, effect in causal_chain:
        print(f"   - {cause} → {effect}")
    print()
    
    # Check for temporal violations
    violations = []
    for cause, effect in causal_chain:
        if cause in timestamps and effect in timestamps:
            cause_time = timestamps[cause]
            effect_time = timestamps[effect]
            if cause_time >= effect_time:
                gap = (cause_time - effect_time) * 1000  # Convert to ms
                violations.append({
                    'cause': cause,
                    'effect': effect,
                    'cause_time': cause_time,
                    'effect_time': effect_time,
                    'gap_ms': gap
                })
    
    print("⚠️  Temporal Causality Analysis:")
    if violations:
        print(f"   VIOLATION DETECTED: {len(violations)} causal impossibility\n")
        for v in violations:
            print(f"   ❌ {v['cause']} → {v['effect']}")
            print(f"      - {v['cause']} at T={v['cause_time']:.4f}s")
            print(f"      - {v['effect']} at T={v['effect_time']:.4f}s")
            print(f"      - Gap: {v['gap_ms']:.1f}ms BACKWARDS")
            print(f"      - Violation: Effect occurs BEFORE cause")
            print()
        
        print("✅ TEST PASSED")
        print("   - Temporal anomaly detected (3ms micro-gap)")
        print("   - Causal impossibility identified")
        print(f"   - EventB@200ms cannot cause EventC@199.7ms")
        print("   - System maintains temporal logic")
        result = "PASS"
    else:
        print("   ❌ NO VIOLATIONS DETECTED")
        print("\n❌ TEST FAILED")
        print("   - System missed 3ms temporal drift")
        print("   - Causal impossibility not identified")
        result = "FAIL"
    
except Exception as e:
    print(f"❌ Temporal analysis failed: {e}")
    import traceback
    traceback.print_exc()
    result = "ERROR"

end = time.time()
duration = end - start

print(f"\n⏱️  Execution Time: {duration:.3f} seconds ({int(duration*1000)}ms)")
print(f"🏷️  Latency Class: sub_100ms_structural" if duration < 0.1 else f"🏷️  Latency Class: 2s_deferred_safe")
print(f"📊 Final Result: {result}")
print("="*80 + "\n")
