import logging
from fastapi import FastAPI, Depends, Request, status
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .routers import stations

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="3호선 도착 정보 확인",
        version="1.0.0",
        openapi_version="3.0.0",
        description="OpenAPI for Subway ornage line (3호선)",
        servers=[
            {
                "url": "<your-url or ip>"
            }
        ],
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    # dependencies=[Depends(get_token_header)]
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    logging.error(f"Query params: {request.query_params}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

app.include_router(stations.router)
app.openapi = custom_openapi


@app.get("/")
async def root():
    return {
        "SUBWAY_API_KEY": "Hello"
    }