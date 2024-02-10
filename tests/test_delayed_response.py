import json

import httpx
import allure
import pytest
from jsonschema import validate

BASE_URL = "https://reqres.in/api/users?delay=3"

def test_delayed_response():
    response = httpx.get(BASE_URL, timeout=5)

    assert response.status_code == 200
    print(response.json())
    
