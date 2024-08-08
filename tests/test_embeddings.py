# tests/test_embeddings.py

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_embeddings_success():
    # Define input data for the embeddings request
    data = {
        "input": ["text to embed"],
        "model": "nomic-ai/nomic-embed-text-v1"
    }
    
    response = client.post("/v1/embeddings", json=data)
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Check if response contains "data" field
    assert "data" in json_response
    assert isinstance(json_response["data"], list)
    assert len(json_response["data"]) > 0

def test_create_embeddings_failure():
    # Define input data with missing fields
    data = {
        "input": "text to embed"  # `model` field is missing
    }
    
    response = client.post("/v1/embeddings", json=data)
    
    assert response.status_code == 422  # Expect validation error

