# CareerCanvas.Jobs

Job aggregation and search service for the CareerCanvas.Pro platform. This service collects job listings from multiple sources and provides a unified API for job search and management.

## Features

- Real-time job aggregation from multiple sources
- Advanced job search with filters
- Automated job data collection
- RESTful API with documentation
- Scalable and containerized deployment

## Tech Stack

- Python 3.10+
- FastAPI
- PostgreSQL
- Redis
- Docker
- Kubernetes
- AWS Cloud

## Quick Start

1. Clone the repository:

```bash
git clone git@github.com:CareerCanvas/CareerCanvas.Jobs.git
cd CareerCanvas.Jobs

```

2. Set up environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your configurations
```

4. Run development server:

```bash
uvicorn services.job_api.main:app --reload
```

## API Documentation

The API documentation is available at /docs when running the server:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

- GET /api/v1/jobs - List and search jobs
- GET /api/v1/jobs/{id} - Get job details
- GET /api/v1/jobs/stats - Get job statistics

## Development

### Prerequisites

- Python 3.10+
- Docker
- PostgreSQL 14+
- Redis 6+

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=services tests/
```

### Local Development with Docker

```bash
docker-compose up -d
```

## Deployment

### MVP Setup (Single EC2)

```bash
./scripts/setup_mvp.sh
```

### Production Setup

See Deployment Guide for detailed instructions.

```plaintext
CareerCanvas.Jobs/
├── services/           # Main service modules
│   ├── job_api/       # REST API service
│   └── job_scraper/   # Job scraping service
├── tests/             # Test suites
├── deployment/        # Deployment configurations
└── docs/             # Documentation
```

## Contributing

Please read our Contributing Guide before submitting a Pull Request.

## ## Monitoring

- Health Check: /health
- Metrics: /metrics
- Logs: CloudWatch Logs
- Dashboards: Grafana

## Support

For support:

1. Check Troubleshooting Guide
2. Open an issue
3. Contact: support@careercanvas.pro

## License

This project is licensed under the MIT License - see the LICENSE file for details.
