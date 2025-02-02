from pydantic import BaseModel
from typing import List, Optional, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: datetime = datetime.utcnow()
    details: Optional[dict] = None

class JobListResponse(BaseModel):
    jobs: List[dict]
    metadata: dict = {
        "source": "CareerCanvas.Jobs",
        "version": "1.0.0"
    }