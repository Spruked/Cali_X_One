# final_ignition.py
from cali.knowledge import Knowledge
k = Knowledge()

print("FINAL IGNITION")

for i in range(65):
    k.tell("Alice", "works_at", "MIT")
    k.tell("Bob", "works_at", "MIT")
    k.tell("Alice", "collaborates", "Bob")
    k.tell("Alice", "researches", "AGI")
    k.tell("Bob", "researches", "AGI")

print("DONE")