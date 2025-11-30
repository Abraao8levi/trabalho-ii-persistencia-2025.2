import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database import create_db_and_tables
from app.crud.exceptions import (
    DuplicateEntryException,
    NotFoundException,
    ValidationException,
)
from routers import actors, genre, movies, reviews, users, watchlist

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Movie Review API",
    description="A comprehensive API for movie reviews and watchlists",
    version="1.0.0"
)

# Exception Handlers
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )

@app.exception_handler(DuplicateEntryException)
async def duplicate_entry_exception_handler(request: Request, exc: DuplicateEntryException):
    return JSONResponse(
        status_code=409,  # Conflict
        content={"message": exc.message},
    )

@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=422,  # Unprocessable Entity
        content={"message": exc.message},
    )

# Include routers
app.include_router(reviews.router)
app.include_router(watchlist.router)
app.include_router(actors.router)
app.include_router(genre.router)
app.include_router(users.router)
app.include_router(movies.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Movie Review API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)