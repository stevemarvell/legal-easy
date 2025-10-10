# API Examples

This document provides practical examples of using the AI Legal Platform API.

## Authentication

Currently, no authentication is required. In production, include the JWT token in the Authorization header:

```bash
Authorization: Bearer <your-jwt-token>
```

## Cases API Examples

### Get All Cases

```bash
curl -X GET "http://localhost:8000/cases" \
  -H "accept: application/json"
```

**Response:**
```json
[
  {
    "id": "case-001",
    "title": "Wrongful Dismissal - Sarah Chen vs TechCorp Solutions",
    "case_type": "Employment Dispute",
    "client_name": "Sarah Chen",
    "status": "Active",
    "created_date": "2024-01-15T09:00:00Z",
    "summary": "Employee alleges wrongful dismissal after reporting safety violations...",
    "key_parties": [
      "Sarah Chen (Claimant)",
      "TechCorp Solutions Ltd. (Respondent)"
    ],
    "documents": ["doc-001", "doc-002", "doc-003"],
    "playbook_id": "employment-dispute"
  }
]
```

### Get Specific Case

```bash
curl -X GET "http://localhost:8000/cases/case-001" \
  -H "accept: application/json"
```

### Get Case Statistics

```bash
curl -X GET "http://localhost:8000/cases/statistics" \
  -H "accept: application/json"
```

**Response:**
```json
{
  "total_cases": 6,
  "active_cases": 3,
  "resolved_cases": 1,
  "under_review_cases": 2,
  "recent_activity_count": 4
}
```

## Documents API Examples

### Get Documents for a Case

```bash
curl -X GET "http://localhost:8000/documents/cases/case-001/documents" \
  -H "accept: application/json"
```

**Response:**
```json
[
  {
    "id": "doc-001",
    "case_id": "case-001",
    "name": "Employment Contract - Sarah Chen",
    "type": "Contract",
    "size": 245760,
    "upload_date": "2024-01-15T09:30:00Z",
    "content_preview": "EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen...",
    "analysis_completed": true
  }
]
```

### Get Specific Document

```bash
curl -X GET "http://localhost:8000/documents/doc-001" \
  -H "accept: application/json"
```

### Get Document Analysis

```bash
curl -X GET "http://localhost:8000/documents/doc-001/analysis" \
  -H "accept: application/json"
```

**Response:**
```json
{
  "document_id": "doc-001",
  "key_dates": ["2022-03-15", "2024-01-12"],
  "parties_involved": [
    "Sarah Chen",
    "TechCorp Solutions Inc.",
    "Marcus Rodriguez"
  ],
  "document_type": "Employment Contract",
  "summary": "At-will employment agreement for Senior Safety Engineer position with 30-day notice provision and standard benefits package.",
  "key_clauses": [
    "At-will employment clause with 30-day notice requirement",
    "Safety reporting obligations and whistleblower protections",
    "Annual salary of $95,000 with performance review eligibility"
  ],
  "confidence_scores": {
    "parties": 0.95,
    "dates": 0.98,
    "contract_terms": 0.92,
    "key_clauses": 0.89
  }
}
```

## JavaScript/TypeScript Examples

### Using Fetch API

```javascript
// Get all cases
const getCases = async () => {
  try {
    const response = await fetch('http://localhost:8000/cases');
    const cases = await response.json();
    console.log('Cases:', cases);
  } catch (error) {
    console.error('Error fetching cases:', error);
  }
};

// Get case statistics
const getStatistics = async () => {
  try {
    const response = await fetch('http://localhost:8000/cases/statistics');
    const stats = await response.json();
    console.log('Statistics:', stats);
  } catch (error) {
    console.error('Error fetching statistics:', error);
  }
};

// Get document analysis
const getDocumentAnalysis = async (documentId) => {
  try {
    const response = await fetch(`http://localhost:8000/documents/${documentId}/analysis`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const analysis = await response.json();
    console.log('Analysis:', analysis);
  } catch (error) {
    console.error('Error fetching analysis:', error);
  }
};
```

### Using Axios

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  }
});

// Get all cases
const cases = await api.get('/cases');

// Get specific case
const case = await api.get('/cases/case-001');

// Get case documents
const documents = await api.get('/documents/cases/case-001/documents');

// Get document analysis
const analysis = await api.get('/documents/doc-001/analysis');
```

## Python Examples

### Using Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Get all cases
response = requests.get(f"{BASE_URL}/cases")
cases = response.json()
print(f"Found {len(cases)} cases")

# Get case statistics
response = requests.get(f"{BASE_URL}/cases/statistics")
stats = response.json()
print(f"Statistics: {stats}")

# Get document analysis
response = requests.get(f"{BASE_URL}/documents/doc-001/analysis")
if response.status_code == 200:
    analysis = response.json()
    print(f"Document type: {analysis['document_type']}")
    print(f"Summary: {analysis['summary']}")
else:
    print(f"Error: {response.status_code}")
```

### Using httpx (async)

```python
import httpx
import asyncio

async def get_cases_index():
    async with httpx.AsyncClient() as client:
        # Get cases
        cases_response = await client.get("http://localhost:8000/cases")
        cases = cases_response.json()
        
        # Get statistics
        stats_response = await client.get("http://localhost:8000/cases/statistics")
        stats = stats_response.json()
        
        return cases, stats

# Run async function
cases, stats = asyncio.run(get_cases_index())
```

## Error Handling Examples

### JavaScript Error Handling

```javascript
const getCaseWithErrorHandling = async (caseId) => {
  try {
    const response = await fetch(`http://localhost:8000/cases/${caseId}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Case not found');
      } else if (response.status === 500) {
        throw new Error('Server error');
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching case:', error.message);
    throw error;
  }
};
```

### Python Error Handling

```python
import requests
from requests.exceptions import RequestException

def get_case_with_error_handling(case_id):
    try:
        response = requests.get(f"http://localhost:8000/cases/{case_id}")
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"Case {case_id} not found")
        elif response.status_code == 500:
            print("Server error occurred")
        else:
            print(f"HTTP error: {e}")
    except RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None
```

## Integration Examples

### React Component Example

```jsx
import React, { useState, useEffect } from 'react';

const CasesList = () => {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCases = async () => {
      try {
        const response = await fetch('http://localhost:8000/cases');
        if (!response.ok) {
          throw new Error('Failed to fetch cases');
        }
        const casesData = await response.json();
        setCases(casesData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCases();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Legal Cases</h2>
      {cases.map(case => (
        <div key={case.id} className="case-item">
          <h3>{case.title}</h3>
          <p>Status: {case.status}</p>
          <p>Client: {case.client_name}</p>
          <p>Type: {case.case_type}</p>
        </div>
      ))}
    </div>
  );
};

export default CasesList;
```

## Testing Examples

### Jest Test Example

```javascript
// api.test.js
const fetch = require('node-fetch');

describe('AI Legal Platform API', () => {
  const BASE_URL = 'http://localhost:8000';

  test('should get all cases', async () => {
    const response = await fetch(`${BASE_URL}/cases`);
    expect(response.status).toBe(200);
    
    const cases = await response.json();
    expect(Array.isArray(cases)).toBe(true);
    expect(cases.length).toBeGreaterThan(0);
  });

  test('should get case statistics', async () => {
    const response = await fetch(`${BASE_URL}/cases/statistics`);
    expect(response.status).toBe(200);
    
    const stats = await response.json();
    expect(stats).toHaveProperty('total_cases');
    expect(stats).toHaveProperty('active_cases');
    expect(typeof stats.total_cases).toBe('number');
  });

  test('should handle 404 for non-existent case', async () => {
    const response = await fetch(`${BASE_URL}/cases/non-existent`);
    expect(response.status).toBe(404);
  });
});
```