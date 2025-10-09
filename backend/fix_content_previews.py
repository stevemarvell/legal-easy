#!/usr/bin/env python3

import json
import os

# Load demo documents
with open('app/data/demo_documents.json', 'r') as f:
    data = json.load(f)

documents = data['documents']

print('=== FIXING CONTENT PREVIEW MISMATCHES ===')

fixed_count = 0

for doc in documents:
    file_path = doc.get('full_content_path')
    if file_path and os.path.exists(file_path):
        # Read actual file content
        with open(file_path, 'r', encoding='utf-8') as f:
            actual_content = f.read()
        
        # Create new preview from actual content (first 150 chars)
        new_preview = actual_content.replace('\n', ' ').replace('\r', '').strip()[:150] + '...'
        
        # Update if different
        if doc['content_preview'] != new_preview:
            print(f'Fixing {doc["id"]}: {doc["name"]}')
            print(f'  Old: {doc["content_preview"][:50]}...')
            print(f'  New: {new_preview[:50]}...')
            doc['content_preview'] = new_preview
            fixed_count += 1

# Save updated file
with open('app/data/demo_documents.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f'\n✅ Fixed {fixed_count} content preview mismatches!')
print('📄 All document previews now match actual file contents')
print('🔄 Analysis should now work with correct content and show proper confidence scores')