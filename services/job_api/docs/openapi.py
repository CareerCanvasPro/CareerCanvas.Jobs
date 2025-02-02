from fastapi.openapi.utils import get_openapi

def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="CareerCanvas Jobs API",
        version="1.0.0",
        description="API for managing and retrieving job listings from various sources",
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://careercanvas.jobs/logo.png"
    }

    openapi_schema["tags"] = [
        {
            "name": "jobs",
            "description": "Operations with job listings"
        },
        {
            "name": "health",
            "description": "API health check endpoints"
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema