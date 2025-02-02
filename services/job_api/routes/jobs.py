from fastapi import APIRouter, Depends, HTTPException, Query
from services.shared.utils.serializers import PaginatedResponse, JobListResponse
from services.shared.database.schemas import JobResponse
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from services.shared.database.connection import get_db
from services.shared.database.repository import JobRepository
from services.shared.database.schemas import JobCreate, JobResponse
from services.shared.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

@router.get("/jobs", response_model=PaginatedResponse[JobResponse])
async def get_jobs(
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    is_remote: Optional[bool] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    try:
        repository = JobRepository(db)
        jobs, total = await repository.get_jobs_paginated(
            location=location,
            job_type=job_type,
            is_remote=is_remote,
            skip=(page - 1) * limit,
            limit=limit
        )
        
        return PaginatedResponse(
            items=jobs,
            total=total,
            page=page,
            size=limit,
            pages=((total - 1) // limit) + 1
        )
    except Exception as e:
        logger.error(f"Error fetching jobs: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        repository = JobRepository(db)
        job = await repository.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")