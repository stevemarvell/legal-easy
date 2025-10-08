from fastapi import APIRouter
from app.models.playbook import Playbook, CaseAssessment
from app.services.playbook_engine import PlaybookEngine

router = APIRouter(prefix="/playbooks", tags=["playbooks"])
playbook_engine = PlaybookEngine()


@router.get("/{case_type}", response_model=Playbook)
async def get_playbook(case_type: str):
    """Get playbook for a specific case type"""
    # Implementation will be added in later tasks
    pass


@router.get("/cases/{case_id}/assessment", response_model=CaseAssessment)
async def get_case_assessment(case_id: str):
    """Get AI assessment for a case using its playbook"""
    # Implementation will be added in later tasks
    pass