#!/usr/bin/env python3

from main import app
from fastapi.testclient import TestClient

# Test all case documents endpoints
client = TestClient(app)

print('=== TESTING ALL CASE DOCUMENTS ===')

# Test cases 1-6
for case_num in range(1, 7):
    case_id = f'case-{case_num:03d}'
    print(f'\n--- Testing {case_id} ---')
    
    response = client.get(f'/api/documents/cases/{case_id}/documents')
    
    if response.status_code == 200:
        data = response.json()
        print(f'✅ {case_id}: {len(data)} documents found')
        for doc in data:
            print(f'   - {doc.get("id")}: {doc.get("name")} (Analysis: {doc.get("analysis_completed")})')
    else:
        print(f'❌ {case_id}: Error {response.status_code} - {response.text}')