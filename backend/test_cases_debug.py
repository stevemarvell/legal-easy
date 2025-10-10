#!/usr/bin/env python3

from main import app
from fastapi.testclient import TestClient

# Debug cases API issues
client = TestClient(app)

print('=== DEBUGGING CASES API ===')

# Test cases list
response = client.get('/api/cases/')
print(f'GET /api/cases/: {response.status_code}')
if response.status_code != 200:
    print(f'Error: {response.text}')

# Test specific case
response = client.get('/api/cases/case-001')
print(f'GET /api/cases/case-001: {response.status_code}')
if response.status_code != 200:
    print(f'Error: {response.text}')

# Test case statistics
response = client.get('/api/cases/statistics')
print(f'GET /api/cases/statistics: {response.status_code}')
if response.status_code != 200:
    print(f'Error: {response.text}')