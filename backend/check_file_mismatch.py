#!/usr/bin/env python3

import json
import os

# Load demo documents
with open('app/data/demo_documents.json', 'r') as f:
    data = json.load(f)

documents = data['documents']  # Extract the documents array

print('=== CHECKING FILE PATH MISMATCHES ===')

# Check doc-021 specifically
doc_021 = None
for doc in documents:
    if doc['id'] == 'doc-021':
        doc_021 = doc
        break

if doc_021:
    print(f'Doc-021 Record:')
    print(f'  ID: {doc_021["id"]}')
    print(f'  Name: {doc_021["name"]}')
    print(f'  File Path: {doc_021.get("full_content_path", "NO PATH")}')
    print(f'  Content Preview: {doc_021["content_preview"][:100]}...')
    
    # Check if file exists and read its content
    file_path = doc_021.get('full_content_path')
    if file_path:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                actual_content = f.read()
            print(f'\n  Actual File Content: {actual_content[:100]}...')
            
            # Check if preview matches actual content
            preview_match = doc_021['content_preview'][:50].lower() in actual_content[:200].lower()
            print(f'  Preview Matches File: {preview_match}')
            
            if not preview_match:
                print('  ❌ MISMATCH DETECTED!')
                print(f'  Expected (from preview): {doc_021["content_preview"][:50]}')
                print(f'  Actual (from file): {actual_content[:50]}')
        else:
            print(f'  File NOT FOUND: {file_path}')
else:
    print('Doc-021 not found in demo_documents.json')

# Check a few more documents for mismatches
print('\n=== CHECKING OTHER DOCUMENTS FOR MISMATCHES ===')
mismatch_count = 0

for doc in documents[:5]:  # Check first 5 documents
    file_path = doc.get('full_content_path')
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            actual_content = f.read()
        
        preview_match = doc['content_preview'][:50].lower() in actual_content[:200].lower()
        if not preview_match:
            mismatch_count += 1
            print(f'\n❌ MISMATCH: {doc["id"]} - {doc["name"]}')
            print(f'  Expected: {doc["content_preview"][:50]}')
            print(f'  Actual: {actual_content[:50]}')

print(f'\nTotal mismatches found: {mismatch_count}')