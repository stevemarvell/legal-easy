#!/usr/bin/env python3

from app.main import app
from fastapi.testclient import TestClient

# Test the actual API endpoint
client = TestClient(app)

print('=== TESTING API ENDPOINT DIRECTLY ===')

# Test with doc-001 (Sarah Chen's contract)
response = client.get('/api/documents/doc-001/analyze')

print(f'Status Code: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Document Type: {data.get("document_type")}')
    print('Confidence Scores:')
    for category, score in data.get('confidence_scores', {}).items():
        print(f'  {category}: {score}')
    
    print('\nFull response structure:')
    print(f'Keys: {list(data.keys())}')
else:
    print(f'Error: {response.text}')