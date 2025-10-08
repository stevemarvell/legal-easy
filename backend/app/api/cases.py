from fastapi import APIRouter
from typing import List
from app.models.case import Case, CaseStatistics
from app.services.case_service import CaseService

router = APIRouter(prefix="/cases", tags=["cases"])
case_service = CaseService()


@router.get("/", response_model=List[Case])
async def get_cases():
    """Get all cases"""
    # Implementation will be added in later tasks
    pass


@router.get("/{case_id}", response_model=Case)
async def get_case(case_id: str):
    """Get a specific case by ID"""
    # Implementation will be added in later tasks
    pass


@router.get("/statistics", response_model=CaseStatistics)
async def get_case_statistics():
    """Get case statistics for dashboard"""
    # Implementation will be added in later tasks
    pass