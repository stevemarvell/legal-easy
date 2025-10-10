#!/usr/bin/env python3

from main import app
from fastapi.testclient import TestClient

# Test the case documents endpoint
client = TestClient(app)

print('=== TESTING CASE DOCUMENTS ENDPOINT ===')

# Test getting documents for case-001
response = client.get('/api/documents/cases/case-001/documents')

print(f'Status Code: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Number of documents: {len(data)}')
    if data:
        print(f'First document ID: {data[0].get("id")}')
        print(f'First document name: {data[0].get("name")}')
        print(f'First document type: {data[0].get("type")}')
        print(f'Analysis completed: {data[0].get("analysis_completed")}')
    
    print('\nAll document IDs:')
    for doc in data:
        print(f'  - {doc.get("id")}: {doc.get("name")}')
else:
    print(f'Error: {response.text}')

print('\n=== TESTING INDIVIDUAL DOCUMENT ENDPOINT ===')

# Test getting a specific document
response = client.get('/api/documents/doc-001')

print(f'Status Code: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Document ID: {data.get("id")}')
    print(f'Document name: {data.get("name")}')
    print(f'Case ID: {data.get("case_id")}')
    print(f'Analysis completed: {data.get("analysis_completed")}')
else:
    print(f'Error: {response.text}')