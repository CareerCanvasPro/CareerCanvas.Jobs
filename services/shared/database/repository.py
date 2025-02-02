from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .models import Job

class JobRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_job(self, job_data: dict) -> Job:
        job = Job(**job_data)
        self.session.add(job)
        await self.session.commit()
        return job

    async def get_job_by_url(self, job_url: str) -> Optional[Job]:
        result = await self.session.execute(
            select(Job).where(Job.job_url == job_url)
        )
        return result.scalar_one_or_none()

    async def get_recent_jobs(self, hours: int = 24) -> List[Job]:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        result = await self.session.execute(
            select(Job)
            .where(Job.date_posted >= cutoff)
            .where(Job.is_active == True)
            .order_by(Job.date_posted.desc())
        )
        return result.scalars().all()