#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

print('=== TESTING SEARCH API ENDPOINT ===')

# Test the actual API endpoint the frontend calls
response = client.post('/api/legal-research/search', json={'query': 'employment'})

print(f'Status Code: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    results = data.get('results', [])
    print(f'Found {len(results)} results for "employment"')
    for i, result in enumerate(results[:3]):
        print(f'  {i+1}. {result.get("document_type", "Unknown")} - {result.get("relevance_score", 0):.2f}')
        print(f'     {result.get("content", "")[:80]}...')
else:
    print(f'Error: {response.text}')

# Test with "law"
print('\n--- Testing "law" ---')
response = client.post('/api/legal-research/search', json={'query': 'law'})
if response.status_code == 200:
    data = response.json()
    results = data.get('results', [])
    print(f'Found {len(results)} results for "law"')
else:
    print(f'Error: {response.text}')