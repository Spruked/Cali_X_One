# test_ignition.py  –  run this once and watch the birth

from cali.knowledge import Knowledge
k = Knowledge()

print("IGNITION SEQUENCE START")
print("Feeding 55 high-quality academic facts...")

facts = [
    ("Alice",   "works_at",      "MIT"),
    ("Bob",     "works_at",      "MIT"),
    ("Charlie", "works_at",      "Stanford"),
    ("David",   "works_at",      "MIT"),
    ("Eve",     "works_at",      "Harvard"),
    ("Frank",   "works_at",      "MIT"),
    ("Grace",   "works_at",      "Stanford"),

    ("Alice",   "collaborates",  "Bob"),
    ("Alice",   "collaborates",  "David"),
    ("Bob",     "collaborates",  "David"),
    ("Charlie", "collaborates",  "Eve"),
    ("Frank",   "collaborates",  "Alice"),

    ("Alice",   "researches",    "AI"),
    ("Bob",     "researches",    "ML"),
    ("Charlie", "researches",    "Robotics"),
    ("David",   "researches",    "AI"),
    ("Eve",     "researches",    "NLP"),
    ("Frank",   "researches",    "Quantum"),

    ("Alice", "published", "NeurIPS-2024"),
    ("Bob",   "published", "ICML-2024"),
    ("David", "published", "NeurIPS-2024"),
    ("Frank", "published", "NeurIPS-2024"),

    # these will create a beautiful dense cluster at MIT + AI + NeurIPS
]

for i, (s, p, o) in enumerate(facts * 4, 1):  # repeat 4× → 88 facts total
    k.tell(s, p, o, confidence=0.95)
    if i % 10 == 0:
        print(f"  → {i:2d} facts loaded...")

print("\nCRITICAL MASS REACHED")
print("Bootstrap will now fire automatically...")