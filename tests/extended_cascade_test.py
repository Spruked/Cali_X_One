# Extended Cascade Test – Push to 50+ edges

from cali.knowledge import Knowledge

print("=== EXTENDED CASCADE TEST TO TRIGGER BOOTSTRAP ===")
print()

k = Knowledge()

# Phase 1: Core academic network (16 edges from before)
facts_phase1 = [
    ('Alice', 'works_at', 'MIT'),
    ('Bob', 'works_at', 'Stanford'), 
    ('Carol', 'works_at', 'MIT'),
    ('Dave', 'works_at', 'Harvard'),
    ('Alice', 'collaborates', 'Bob'),
    ('Bob', 'collaborates', 'Carol'),
    ('Carol', 'collaborates', 'Dave'),
    ('Dave', 'collaborates', 'Alice'),
    ('Alice', 'researches', 'AGI'),
    ('Bob', 'researches', 'Robotics'),
    ('Carol', 'researches', 'Quantum Computing'),
    ('Dave', 'researches', 'Neuroscience'),
    ('Bob', 'works_at', 'MIT'),  # Contradiction
    ('Alice', 'interests', 'Ethics'),
    ('Carol', 'interests', 'Philosophy'),
    ('Dave', 'interests', 'Mathematics')
]

print(f"Phase 1: Adding {len(facts_phase1)} core academic facts...")
for i, (s, p, o) in enumerate(facts_phase1, 1):
    k.tell(s, p, o, 0.9)
    if i % 5 == 0:
        print(f"  → {i} facts added...")

# Phase 2: Expand the network with more researchers
print(f"\nPhase 2: Adding extended research network...")
facts_phase2 = [
    ('Eve', 'works_at', 'Caltech'),
    ('Frank', 'works_at', 'MIT'),
    ('Grace', 'works_at', 'Stanford'), 
    ('Henry', 'works_at', 'Harvard'),
    ('Eve', 'researches', 'Computer_Vision'),
    ('Frank', 'researches', 'Machine_Learning'),
    ('Grace', 'researches', 'Natural_Language'),
    ('Henry', 'researches', 'Brain_Simulation'),
    ('Alice', 'collaborates', 'Eve'),
    ('Bob', 'collaborates', 'Frank'),
    ('Carol', 'collaborates', 'Grace'),
    ('Dave', 'collaborates', 'Henry'),
    ('Eve', 'collaborates', 'Frank'),
    ('Frank', 'collaborates', 'Grace'),
    ('Grace', 'collaborates', 'Henry'),
    ('Henry', 'collaborates', 'Eve')
]

for i, (s, p, o) in enumerate(facts_phase2, 1):
    k.tell(s, p, o, 0.85)
    if i % 5 == 0:
        print(f"  → {len(facts_phase1) + i} total facts...")

# Phase 3: Publications and citations to reach 50+
print(f"\nPhase 3: Adding publications and citations to reach cascade threshold...")
facts_phase3 = [
    ('Alice', 'published', 'AGI_Ethics_2025'),
    ('Bob', 'published', 'Robotics_Review_2025'), 
    ('Carol', 'published', 'Quantum_AI_2025'),
    ('Dave', 'published', 'NeuroAI_Methods_2025'),
    ('Eve', 'published', 'Vision_Systems_2025'),
    ('Frank', 'published', 'ML_Foundations_2025'),
    ('Grace', 'published', 'NLP_Advances_2025'),
    ('Henry', 'published', 'Brain_Models_2025'),
    ('AGI_Ethics_2025', 'cites', 'ML_Foundations_2025'),
    ('Robotics_Review_2025', 'cites', 'Vision_Systems_2025'),
    ('Quantum_AI_2025', 'cites', 'AGI_Ethics_2025'),
    ('NeuroAI_Methods_2025', 'cites', 'Brain_Models_2025'),
    ('Vision_Systems_2025', 'cites', 'NLP_Advances_2025'),
    ('ML_Foundations_2025', 'cites', 'Quantum_AI_2025'),
    ('NLP_Advances_2025', 'cites', 'NeuroAI_Methods_2025'),
    ('Brain_Models_2025', 'cites', 'Robotics_Review_2025'),
    ('Alice', 'advises', 'Carol'),
    ('Bob', 'advises', 'Eve')
]

current_count = len(facts_phase1) + len(facts_phase2)
for i, (s, p, o) in enumerate(facts_phase3, 1):
    total = current_count + i
    k.tell(s, p, o, 0.8)
    if total % 10 == 0:
        print(f"  → {total} facts total...")
    if total >= 50:
        print(f"  → THRESHOLD REACHED: {total} facts!")
        break

print(f"\nTotal facts added: {len(facts_phase1) + len(facts_phase2) + len(facts_phase3)}")
print("\n=== CASCADE SHOULD HAVE FIRED - CHECKING RESULTS ===")

# Test some complex queries
print("\n1. MIT Research Cluster:")
mit_workers = k.ask([None, 'works_at', 'MIT'])
for result in mit_workers[:5]:  # Limit output
    print(f"   → {result[0]} at MIT")

print("\n2. Citation Network Sample:")
citations = k.ask([None, 'cites', None])
for result in citations[:5]:
    print(f"   → {result[0]} cites {result[2]}")

print("\n3. Collaboration Density:")
collabs = k.ask([None, 'collaborates', None])
print(f"   → {len(collabs)} collaboration edges found")

print("\n=== EXTENDED CASCADE TEST COMPLETE ===")