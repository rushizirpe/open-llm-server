import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_metrics():
    response = client.get("/v1/metrics")
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Check for the presence of metrics fields
    assert "cpu_usage" in json_response
    assert "memory_usage" in json_response
    assert "disk_usage" in json_response
    
    # Check if values are floats (or integers)
    assert isinstance(json_response["cpu_usage"], (int, float))
    assert isinstance(json_response["memory_usage"], (int, float))
    assert isinstance(json_response["disk_usage"], (int, float))