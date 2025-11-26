import logging

from fastapi import FastAPI

from .database import create_db_and_tables
from .routers import reviews, watchlist

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Movie Review API",
    description="A comprehensive API for movie reviews and watchlists",
    version="1.0.0"
)

# Include routers
app.include_router(reviews.router)
app.include_router(watchlist.router)

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