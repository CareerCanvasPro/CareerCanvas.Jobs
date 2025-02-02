from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    company_url = Column(String(500))
    job_url = Column(String(500), unique=True, index=True)
    location_country = Column(String(100))
    location_city = Column(String(100))
    location_state = Column(String(100))
    description = Column(Text)
    job_type = Column(String(50))
    salary_interval = Column(String(20))
    salary_min = Column(Float)
    salary_max = Column(Float)
    currency = Column(String(10))
    date_posted = Column(DateTime, index=True)
    date_scraped = Column(DateTime, default=datetime.utcnow)
    is_remote = Column(Boolean, default=False)
    source_site = Column(String(50))
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        Index('idx_job_search', 'title', 'company', 'location_country', 'is_active'),
    )