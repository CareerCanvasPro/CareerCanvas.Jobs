from pydantic import BaseModel, HttpUrl, Field, validator
from typing import Optional
from datetime import datetime

class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    company: str = Field(..., min_length=1, max_length=255)
    company_url: Optional[HttpUrl]
    job_url: HttpUrl
    location_country: str
    location_city: Optional[str]
    location_state: Optional[str]
    description: str
    job_type: Optional[str]
    salary_interval: Optional[str]
    salary_min: Optional[float] = Field(None, ge=0)
    salary_max: Optional[float] = Field(None, ge=0)
    currency: Optional[str]
    is_remote: bool = False
    source_site: str

    @validator('salary_max')
    def validate_salary_range(cls, v, values):
        if v and values.get('salary_min') and v < values['salary_min']:
            raise ValueError('salary_max must be greater than salary_min')
        return v

class JobCreate(JobBase):
    date_posted: datetime

class JobUpdate(JobBase):
    is_active: Optional[bool]

class JobResponse(JobBase):
    id: int
    date_posted: datetime
    date_scraped: datetime
    is_active: bool

    class Config:
        orm_mode = True