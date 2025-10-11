#!/usr/bin/env python3
from app.services.data_service import DataService

print('Regenerating document analysis...')
success = DataService.regenerate_document_analysis()
print(f'Success: {success}')

if success:
    stats = DataService.get_document_analysis_stats()
    print(f"Total documents: {stats.get('total_documents')}")
    print(f"Analyzed documents: {stats.get('analyzed_documents')}")
    print(f"Failed documents: {stats.get('failed_documents')}")
    print(f"Average confidence: {stats.get('average_confidence')}")