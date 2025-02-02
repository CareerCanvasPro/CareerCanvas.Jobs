from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime

class JobSearchParams(BaseModel):
    keyword: Optional[str] = Field(None, min_length=2, max_length=100)
    location: Optional[str] = Field(None, min_length=2, max_length=100)
    job_type: Optional[str] = Field(None, regex="^(FULL_TIME|PART_TIME|CONTRACT|INTERNSHIP)$")
    is_remote: Optional[bool] = None
    min_salary: Optional[float] = Field(None, ge=0)
    max_salary: Optional[float] = Field(None, ge=0)
    posted_after: Optional[datetime] = None

    @validator('max_salary')
    def validate_salary_range(cls, v, values):
        if v and values.get('min_salary') and v < values['min_salary']:
            raise ValueError('max_salary must be greater than min_salary')
        return v