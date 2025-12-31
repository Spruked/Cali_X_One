import json, jsonschema, os, hashlib
from pathlib import Path

VAULT_ROOT = Path(os.getenv("SEED_VAULT_PATH", "/app/seed_vault"))
INDEX_FILE = VAULT_ROOT / "index.json"
SCHEMA_DIR = VAULT_ROOT.parent / "schemas"

class SeedVault:
    def __init__(self):
        self.index = json.loads(INDEX_FILE.read_text())
        self._validate_index()
        self.cache = {}

    def _validate_index(self):
        schema = json.loads((SCHEMA_DIR / "vault-index-v1.1.0.json").read_text())
        jsonschema.validate(self.index, schema)

    def load(self, vault_id: str):
        if vault_id in self.cache:
            return self.cache[vault_id]
        section = next(s for s in self.index["vaults"] if s["id"] == vault_id)
        data = {}
        for file in section["files"]:
            path = VAULT_ROOT / file
            data.update(json.loads(path.read_text()))
        self.cache[vault_id] = data
        return data

    def verify_hash(self, path: Path):
        expect = json.loads(path.read_text())["access_control"]["hash"]
        got = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if got != expect:
            raise RuntimeError(f"Hash mismatch {path}")