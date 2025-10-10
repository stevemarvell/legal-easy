#!/usr/bin/env python3

from main import app
from fastapi.testclient import TestClient

# Test cases API
client = TestClient(app)

print('=== TESTING CASES API ===')

# Test getting all cases
response = client.get('/api/cases/')
print(f'GET /api/cases/: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Number of cases: {len(data)}')
    if data:
        print(f'First case: {data[0].get("id")} - {data[0].get("title")}')
        print(f'Case type: {data[0].get("case_type")}')
        print(f'Status: {data[0].get("status")}')

# Test getting specific case
response = client.get('/api/cases/case-001')
print(f'\nGET /api/cases/case-001: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Case: {data.get("title")}')
    print(f'Client: {data.get("client_name")}')
    print(f'Documents: {len(data.get("documents", []))}')

# Test case statistics
response = client.get('/api/cases/statistics')
print(f'\nGET /api/cases/statistics: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Total cases: {data.get("total_cases")}')
    print(f'Active cases: {data.get("active_cases")}')
    print(f'Under review: {data.get("under_review_cases")}')
    print(f'Recent activity: {data.get("recent_activity_count")}')
else:
    print(f'Error: {response.text}')