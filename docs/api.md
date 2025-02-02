# CareerCanvas.Jobs API Documentation

## Overview

CareerCanvas.Jobs is a component of the CareerCanvas.Pro platform, providing a RESTful API for managing and retrieving job listings from multiple sources. This service aggregates job postings from various job boards and company career pages, offering a unified interface for job search and management.

## Base URL

https://jobs.careercanvas.pro/api/v1

## Authentication

All API endpoints require an API key passed in the header:

X-API-Key: your_api_key_here

## Endpoints

### Get Jobs

```http
GET /jobs
```

### Query Parameters:

- keyword (optional): Search term
- location (optional): Location filter
- job_type (optional): FULL_TIME, PART_TIME, CONTRACT, REMOTE
- page (default: 1): Page number
- limit (default: 10, max: 100): Items per page

Response:

```
{
    "items": [
        {
            "id": "string",
            "title": "string",
            "company": "string",
            "location": "string",
            "job_type": "string",
            "salary_range": {
                "min": "number",
                "max": "number",
                "currency": "string"
            },
            "description": "string",
            "requirements": "string",
            "posted_date": "string",
            "source": "string",
            "url": "string"
        }
    ],
    "total": "number",
    "page": "number",
    "pages": "number"
}
```

### Get Job by ID

```http
GET /jobs/{id}
```

```
{
    "id": "string",
    "title": "string",
    "company": "string",
    "company_url": "string",
    "location_country": "string",
    "location_city": "string",
    "location_state": "string",
    "job_type": "string",
    "salary_interval": "string",
    "salary_min": "number",
    "salary_max": "number",
    "currency": "string",
    "description": "string",
    "is_remote": "boolean",
    "date_posted": "string",
    "source_site": "string",
    "job_url": "string"
}

```

## Search Jobs

GET /jobs/search

Query Parameters:

- q (required): Search query string
- location : Filter by location
- remote_only : Boolean to filter remote jobs only
- posted_after : ISO date string to filter by posting date
- salary_min : Minimum salary filter
- salary_currency : Currency code for salary filter
- page : Page number (default: 1)
- limit : Results per page (default: 10, max: 100)

Response:

{
"items": [...],
"total": "number",
"page": "number",
"pages": "number",
"filters": {
"locations": ["string"],
"job_types": ["string"],
"salary_ranges": [{
"min": "number",
"max": "number",
"currency": "string"
}]
}
}

Get Job Statistics

GET /jobs/stats
Response:
{
"total_jobs": "number",
"active_jobs": "number",
"jobs_by_source": {
"LinkedIn": "number",
"Indeed": "number",
"BdJobs": "number"
},
"jobs_by_type": {
"FULL_TIME": "number",
"PART_TIME": "number",
"CONTRACT": "number",
"REMOTE": "number"
},
"top_locations": [
{
"country": "string",
"count": "number"
}
]
}

Error Responses

All endpoints may return the following error responses:

### 400 Bad Request

{
"error": "VALIDATION_ERROR",
"message": "Error description",
"details": {
"field": ["error detail"]
}
}

### 401 Unauthorized

{
"error": "UNAUTHORIZED",
"message": "Invalid or missing API key"
}

### 429 Too Many Requests

{
"error": "RATE_LIMIT_EXCEEDED",
"message": "Too many requests",
"retry_after": "number"
}
