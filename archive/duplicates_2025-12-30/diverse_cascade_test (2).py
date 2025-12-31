# UCM Caleon Test Script – Varied Fact Cascade

from cali.knowledge import Knowledge

print("=== DIVERSE FACT CASCADE TEST ===")
print("Testing: contradictions, cycles, cross-domain diversity")
print()

k = Knowledge()

print("Phase 1: Institution Diversity")
k.tell('Alice', 'works_at', 'MIT')
k.tell('Bob', 'works_at', 'Stanford')
k.tell('Carol', 'works_at', 'MIT')
k.tell('Dave', 'works_at', 'Harvard')

print("\nPhase 2: Collaboration Cycles")
k.tell('Alice', 'collaborates', 'Bob')
k.tell('Bob', 'collaborates', 'Carol')
k.tell('Carol', 'collaborates', 'Dave')
k.tell('Dave', 'collaborates', 'Alice')

print("\nPhase 3: Research Domain Diversity")
k.tell('Alice', 'researches', 'AGI')
k.tell('Bob', 'researches', 'Robotics')
k.tell('Carol', 'researches', 'Quantum Computing')
k.tell('Dave', 'researches', 'Neuroscience')

print("\nPhase 4: Contradiction Test (Bob at two institutions)")
k.tell('Bob', 'works_at', 'MIT')  # Bob now works at both Stanford AND MIT

print("\nPhase 5: Cross-domain Interest Links")
k.tell('Alice', 'interests', 'Ethics')
k.tell('Carol', 'interests', 'Philosophy')
k.tell('Dave', 'interests', 'Mathematics')

print("\n=== FACT SEEDING COMPLETE – CASCADE SHOULD IGNITE ===")
print()

print("=== POST-CASCADE QUERY TESTS ===")
print()

print("1. Who collaborates with Alice?")
alice_collabs = k.ask(['Alice', 'collaborates', None])
for result in alice_collabs:
    print(f"   → Alice collaborates with {result[2]}")

print()
print("2. Who researches Robotics?")
robotics_researchers = k.ask([None, 'researches', 'Robotics'])
for result in robotics_researchers:
    print(f"   → {result[0]} researches Robotics")

print()
print("3. Where does Bob work? (Should show contradiction)")
bob_workplace = k.ask(['Bob', 'works_at', None])
for result in bob_workplace:
    print(f"   → Bob works at {result[2]} (weight: {result[3] if len(result) > 3 else 'unknown'})")

print()
print("4. Who works at MIT?")
mit_workers = k.ask([None, 'works_at', 'MIT'])
for result in mit_workers:
    print(f"   → {result[0]} works at MIT")

print()
print("5. Full collaboration network:")
all_collabs = k.ask([None, 'collaborates', None])
for result in all_collabs:
    print(f"   → {result[0]} ↔ {result[2]}")

print()
print("=== DIVERSITY ANALYSIS COMPLETE ===")