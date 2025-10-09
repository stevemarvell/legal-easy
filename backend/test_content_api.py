#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app
from fastapi.testclient import TestClient

# Test the new document content endpoint
client = TestClient(app)

print('=== TESTING DOCUMENT CONTENT API ENDPOINT ===')

# Test with doc-001 (Sarah Chen's contract)
response = client.get('/api/documents/doc-001/content')

print(f'Status Code: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Document ID: {data.get("document_id")}')
    print(f'Content Length: {data.get("content_length")} characters')
    print(f'Content Preview: {data.get("content", "")[:100]}...')
    print('✅ Document content API endpoint works!')
else:
    print(f'❌ Error: {response.text}')

# Test with doc-021 (Insurance Policy)
print('\n=== TESTING DOC-021 ===')
response = client.get('/api/documents/doc-021/content')

print(f'Status Code: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Document ID: {data.get("document_id")}')
    print(f'Content Length: {data.get("content_length")} characters')
    print(f'Content Preview: {data.get("content", "")[:100]}...')
    print('✅ Doc-021 content API works!')
else:
    print(f'❌ Error: {response.text}')