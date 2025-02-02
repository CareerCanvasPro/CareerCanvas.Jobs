import pytest
from datetime import datetime
from services.shared.database.repository import JobRepository

@pytest.mark.asyncio
async def test_create_job(test_db):
    async with test_db() as session:
        repository = JobRepository(session)
        job_data = {
            'title': 'Python Developer',
            'company': 'Test Company',
            'job_url': 'https://example.com/job/123',
            'location': 'Remote',
            'description': 'Test job description',
            'source_site': 'Test'
        }
        
        job = await repository.create_job(job_data)
        assert job.id is not None
        assert job.title == job_data['title']
        assert job.company == job_data['company']

@pytest.mark.asyncio
async def test_get_job_by_url(test_db):
    async with test_db() as session:
        repository = JobRepository(session)
        job_url = 'https://example.com/job/456'
        job_data = {
            'title': 'Senior Developer',
            'company': 'Another Company',
            'job_url': job_url,
            'location': 'Dhaka',
            'source_site': 'Test'
        }
        
        await repository.create_job(job_data)
        job = await repository.get_job_by_url(job_url)
        assert job is not None
        assert job.job_url == job_url