#!/usr/bin/env python3
"""
🎯 Direct Predicate Invention Test
=====================================
Create data specifically designed to trigger predicate invention.
"""

import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'skg-core'))

from skg.core import SKGCore
from skg.invent_predicate import maybe_invent_predicate
import networkx as nx
import time

def create_clustered_test():
    print("🎯 Creating targeted predicate invention test...")
    skg = SKGCore()
    
    # Create TWO distinct clusters that should be recognized as patterns
    
    # CLUSTER 1: FOUNDATION PATTERN (Physical dependencies)
    foundation_cluster = [
        ('Pyramid', 'requires', 'Foundation'),
        ('Bridge', 'requires', 'Foundation'), 
        ('Building', 'requires', 'Foundation'),
        ('Tower', 'requires', 'Foundation'),
        ('Foundation', 'supports', 'Pyramid'),
        ('Foundation', 'supports', 'Bridge'),
        ('Foundation', 'supports', 'Building'),
        ('Foundation', 'supports', 'Tower'),
    ]
    
    # CLUSTER 2: LOGIC PATTERN (Abstract dependencies)  
    logic_cluster = [
        ('Theorem', 'requires', 'Axiom'),
        ('Proof', 'requires', 'Axiom'),
        ('Logic', 'requires', 'Axiom'),
        ('Reasoning', 'requires', 'Axiom'),
        ('Axiom', 'enables', 'Theorem'),
        ('Axiom', 'enables', 'Proof'),
        ('Axiom', 'enables', 'Logic'),
        ('Axiom', 'enables', 'Reasoning'),
    ]
    
    # Add clusters sequentially
    print("\n📊 Adding Foundation Pattern cluster...")
    for fact in foundation_cluster:
        skg.add_triples([fact])
        
    print("📊 Adding Logic Pattern cluster...")  
    for fact in logic_cluster:
        skg.add_triples([fact])
        
    # Add filler facts to reach 50+ and trigger bootstrap
    print("📊 Adding filler facts for bootstrap...")
    for i in range(35):  # 16 cluster facts + 35 filler = 51 total
        skg.add_triples([(f'Entity_{i}', 'relates_to', f'Target_{i}')])
    
    print(f"\n🔍 Current state:")
    print(f"  Total edges in level 0: {skg.levels[0].number_of_edges()}")
    print(f"  Bootstrap triggered: {getattr(skg, 'bootstrapped', False)}")
    
    # Check level structure
    for level_num in range(3):
        if level_num in skg.levels:
            level = skg.levels[level_num]
            print(f"  Level {level_num}: {level.number_of_nodes()} nodes, {level.number_of_edges()} edges")
    
    # Manual predicate invention attempt
    print(f"\n🤖 Attempting predicate invention...")
    maybe_invent_predicate(skg, thresh=0.5)  # Lower threshold to catch clusters
    
    # Check results
    invented_predicates = []
    for u, v, d in skg.levels[0].edges(data=True):
        pred = d.get('predicate', '')
        if 'cluster_' in pred or 'isA' in pred:
            invented_predicates.append((u, pred, v))
            print(f"  🎯 FOUND: {u} --[{pred}]--> {v}")
    
    print(f"\n📈 Result: {len(invented_predicates)} invented predicates")
    return skg, invented_predicates

if __name__ == "__main__":
    skg, predicates = create_clustered_test()
    if len(predicates) > 0:
        print("\n🚀 SUCCESS: Predicate invention achieved!")
        print("   The system successfully identified abstract patterns!")
    else:
        print("\n⏳ No predicates invented - may need different clustering")