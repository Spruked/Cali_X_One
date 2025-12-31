import sys, os
# SKG is in local skg-core
_UCM_SKG = os.path.join(os.path.dirname(__file__), "..", "skg-core")
sys.path.insert(0, _UCM_SKG)

# 2.  import the real SKG engine
from skg.core import SKGService   # now found

class Knowledge:
    __slots__ = ("_skg",)
    def __init__(self, db_path=None):
        self._skg = SKGService(db_path or "cali_skg.db")
    #  same API Cali expects
    def tell(self, sub, pred, obj, confidence=1.0):
        self._skg.add(sub, pred, obj, confidence)
    def ask(self, pattern, top_k=10):
        # pattern = [sub,pred,obj]  None = wildcard
        return self._skg.query(pattern, top_k)
    def save(self): pass   # SKG is already persistent
    def load(self): pass   # mount happens at init