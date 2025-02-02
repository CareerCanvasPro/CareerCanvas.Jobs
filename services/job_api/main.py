from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from services.shared.database.connection import get_db
from services.shared.utils.logger import setup_logger
from .routes import jobs, health

app = FastAPI(
    title="CareerCanvas Jobs API",
    description="API for managing and retrieving job listings",
    version="1.0.0"
)

# Middleware
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rate_limiter = RateLimiter()

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    await rate_limiter.check_rate_limit(request)
    response = await call_next(request)
    return response

# Include routers with auth
app.include_router(
    jobs.router,
    prefix="/api/v1",
    tags=["jobs"],
    dependencies=[Depends(verify_api_key)]
)
app.include_router(health.router, tags=["health"])

logger = setup_logger("job_api")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Job API service")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Job API service")