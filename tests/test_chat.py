# tests/test_chat.py

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_chat_completion_success():
    # Define input data for the chat completion request
    data = {
        "model": "openai-community/gpt2",
        "messages": [{"role": "user", "content": "Hello, world!"}],
        "max_tokens": 50
    }
    
    response = client.post("/v1/chat/completions", json=data)
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Check if response contains "choices" field
    assert "choices" in json_response
    assert isinstance(json_response["choices"], list)
    assert len(json_response["choices"]) > 0

def test_create_chat_completion_failure():
    # Define input data with missing fields
    data = {
        "model": "openai-community/gpt2",
        "messages": []
    }
    
    response = client.post("/v1/chat/completions", json=data)
    
    assert response.status_code == 422  # Expect validation error

