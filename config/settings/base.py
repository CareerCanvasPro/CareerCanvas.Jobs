from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Service Configuration
    SERVICE_NAME: str = "careercanvas-jobs"
    ENVIRONMENT: str = Field(default="development", env="ENV")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # AWS Configuration
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")
    
    # Database Configuration
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    class Config:
        env_file = ".env"

settings = Settings()