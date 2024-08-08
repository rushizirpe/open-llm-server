# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


