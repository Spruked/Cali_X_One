"""
End-to-End Testing for SKG Enhanced API
Tests the FastAPI endpoints using TestClient
"""

import pytest
from fastapi.testclient import TestClient
from skg_api import app

client = TestClient(app)

def test_health_check():
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    print("✅ Health check passed")

def test_add_triple():
    """Test adding a triple"""
    triple = {"s": "Alice", "p": "works_at", "o": "MIT"}
    response = client.post("/add", json=triple)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print("✅ Add triple passed")

def test_query_triples():
    """Test querying triples"""
    response = client.get("/query?pat=[Alice,null,null]")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    print("✅ Query triples passed")

def test_stats():
    """Test stats endpoint"""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "levels" in data
    print("✅ Stats passed")

def test_batch_add():
    """Test batch add triples"""
    triples = [
        ["Bob", "knows", "Alice"],
        ["Charlie", "studies", "AI"]
    ]
    response = client.post("/add_batch", json={"triples": triples})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print("✅ Batch add passed")

def test_expand():
    """Test expand endpoint"""
    response = client.post("/expand", json={"force_bootstrap": True})
    if response.status_code != 200:
        print(f"Status: {response.status_code}, Response: {response.text}")
    assert response.status_code == 200
    print("✅ Expand passed")

if __name__ == "__main__":
    print("🚀 Running SKG Enhanced End-to-End Tests")
    test_health_check()
    test_add_triple()
    test_query_triples()
    test_stats()
    test_batch_add()
    test_expand()
    print("🎉 All tests passed!")