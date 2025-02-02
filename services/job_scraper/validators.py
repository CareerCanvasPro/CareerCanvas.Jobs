from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl, validator
import re

class ScrapedJobValidator(BaseModel):
    title: str
    company: str
    job_url: HttpUrl
    location: str
    description: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    currency: Optional[str]
    job_type: Optional[str]
    source_site: str
    date_posted: Optional[datetime]

    @validator('title')
    def validate_title(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Title too short')
        return v.strip()

    @validator('company')
    def validate_company(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Company name too short')
        return v.strip()

    @validator('salary_max')
    def validate_salary_range(cls, v, values):
        if v and values.get('salary_min') and v < values['salary_min']:
            raise ValueError('Maximum salary cannot be less than minimum salary')
        return v

    @validator('job_type')
    def validate_job_type(cls, v):
        valid_types = {'FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERNSHIP', 'REMOTE'}
        if v and v not in valid_types:
            raise ValueError(f'Invalid job type. Must be one of {valid_types}')
        return v