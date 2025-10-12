# Services for the AI Legal Platform

from .cases_service import CasesService
from .documents_service import DocumentsService
from .corpus_service import CorpusService
from .playbooks_service import PlaybooksService


__all__ = ['CasesService', 'DocumentsService', 'CorpusService', 'PlaybooksService']