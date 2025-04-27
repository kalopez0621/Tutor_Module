from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Tutor Module API",
    description="AI-Powered Tutor Module for MDC Skyy using Gemma",
    version="1.0.0"
)

# Include all routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Tutor Module API is running!"}
