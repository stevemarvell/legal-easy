#!/usr/bin/env python3

import json

# Load the cached analysis results
with open('app/data/analysis_results/live_analysis_results.json', 'r') as f:
    data = json.load(f)

# Check doc-021 specifically
if 'doc-021' in data['analyses']:
    doc_021 = data['analyses']['doc-021']
    print('=== CACHED ANALYSIS FOR DOC-021 ===')
    print(f'Document Type: {doc_021.get("document_type")}')
    print('Confidence Scores:')
    for category, score in doc_021.get('confidence_scores', {}).items():
        print(f'  {category}: {score:.3f} ({score:.1%})')
        if abs(score - 0.5) < 0.01:
            print('    ↑ This is exactly 50%!')
    print(f'\nParties: {doc_021.get("parties_involved")}')
    print(f'Summary: {doc_021.get("summary", "")[:100]}...')
else:
    print('doc-021 not found in cached results')