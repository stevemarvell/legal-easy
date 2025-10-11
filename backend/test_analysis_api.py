#!/usr/bin/env python3
import requests
import json

def test_analysis_api():
    try:
        # Test the analysis endpoint
        response = requests.get('http://localhost:8000/api/documents/doc-001/analysis')
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            print('Analysis found!')
            data = response.json()
            print(f'Document ID: {data.get("document_id")}')
            print(f'Overall confidence: {data.get("overall_confidence")}')
            print(f'Summary: {data.get("summary", "No summary")[:100]}...')
            print(f'Key dates: {data.get("key_dates", [])}')
            print(f'Parties: {data.get("parties_involved", [])}')
        elif response.status_code == 404:
            print('Analysis not found - this is the issue!')
            print(f'Error: {response.text}')
        else:
            print(f'Error: {response.text}')
            
    except Exception as e:
        print(f'Connection error: {e}')
        print('Make sure the backend server is running on localhost:8000')

if __name__ == "__main__":
    test_analysis_api()