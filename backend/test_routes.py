#!/usr/bin/env python3

from main import app
from fastapi.testclient import TestClient

# Test available routes
client = TestClient(app)

print('=== TESTING AVAILABLE ROUTES ===')

# Test root
response = client.get('/')
print(f'GET /: {response.status_code}')

# Test health
response = client.get('/health')
print(f'GET /health: {response.status_code}')

# Test documents routes
response = client.get('/api/documents/cases/case-001/documents')
print(f'GET /api/documents/cases/case-001/documents: {response.status_code}')

response = client.get('/api/documents/doc-001')
print(f'GET /api/documents/doc-001: {response.status_code}')

# Test cases routes
response = client.get('/api/cases/')
print(f'GET /api/cases/: {response.status_code}')

response = client.get('/api/cases/case-001')
print(f'GET /api/cases/case-001: {response.status_code}')

# Test playbooks routes
response = client.get('/api/playbooks/')
print(f'GET /api/playbooks/: {response.status_code}')

# Test legal research routes
response = client.get('/api/legal-research/categories')
print(f'GET /api/legal-research/categories: {response.status_code}')

# Test admin routes
response = client.get('/api/admin/stats')
print(f'GET /api/admin/stats: {response.status_code}')

print('\n=== TESTING OPENAPI SPEC ===')
response = client.get('/openapi.json')
print(f'GET /openapi.json: {response.status_code}')
if response.status_code == 200:
    openapi_spec = response.json()
    print(f'Available paths: {len(openapi_spec["paths"])} endpoints')
    print('Sample paths:')
    for path in list(openapi_spec["paths"].keys())[:10]:
        print(f'  - {path}')