#!/usr/bin/env python3

from main import app
from fastapi.testclient import TestClient

# Comprehensive API test
client = TestClient(app)

def test_endpoint(method, url, expected_status=200):
    """Test an endpoint and return result"""
    if method.upper() == 'GET':
        response = client.get(url)
    elif method.upper() == 'POST':
        response = client.post(url)
    else:
        return f"❌ {method} {url}: Unsupported method"
    
    if response.status_code == expected_status:
        return f"✅ {method} {url}: {response.status_code}"
    else:
        return f"❌ {method} {url}: {response.status_code} (expected {expected_status})"

print('=== COMPREHENSIVE API TEST ===')

# Core endpoints
results = []
results.append(test_endpoint('GET', '/'))
results.append(test_endpoint('GET', '/health'))

# Documents API
results.append(test_endpoint('GET', '/api/documents/cases/case-001/documents'))
results.append(test_endpoint('GET', '/api/documents/doc-001'))
results.append(test_endpoint('GET', '/api/documents/doc-001/analysis', 404))  # No analysis stored
results.append(test_endpoint('POST', '/api/documents/doc-001/analyze'))
results.append(test_endpoint('GET', '/api/documents/doc-001/content'))

# Cases API
results.append(test_endpoint('GET', '/api/cases/'))
results.append(test_endpoint('GET', '/api/cases/case-001'))
results.append(test_endpoint('GET', '/api/cases/statistics'))

# Playbooks API
results.append(test_endpoint('GET', '/api/playbooks/'))

# Legal Research API
results.append(test_endpoint('GET', '/api/legal-research/categories'))

# Admin API
results.append(test_endpoint('GET', '/api/admin/stats', 404))  # May not be implemented

# Print results
for result in results:
    print(result)

# Count successes
successes = len([r for r in results if r.startswith('✅')])
total = len(results)
print(f'\n=== SUMMARY ===')
print(f'Passed: {successes}/{total} ({successes/total*100:.1f}%)')

if successes >= total * 0.8:  # 80% success rate
    print('🎉 API is working well!')
else:
    print('⚠️  Some API issues detected')