# Create a fastapi project
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from api.routers.mask_pdf import router as mask_pdf_router

server = FastAPI(
    title="FastAPI",
    description="FastAPI",
    version="0.0.1",
)


# Handle CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]


# Give an Id to every request and response set
@server.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id", "")
    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    return response


@server.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global handler for all exceptions.
    Returns a structured JSON error response.
    """
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unexpected error occurred",
            "error": str(exc),
            "path": str(request.url),
        },
    )


@server.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handles HTTPException with custom message sent from router.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "path": str(request.url)},
    )


# Add cors middleware
server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

server.include_router(mask_pdf_router)


@server.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error", "detail": str(e)},
        )


@server.get("/")
async def root():
    return {"message": "Hello, FastAPI"}


# Start the server
if __name__ == "__main__":
    uvicorn.run(server, host="0.0.0.0", port=8000)
