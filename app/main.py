from fastapi import FastAPI
from app.routes import router
from app.gemma_engine import get_gemma_response

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

@app.on_event("startup")
def warm_model():
    print("Warming up Gemma model...")
    get_gemma_response("hello")
    print("Model ready.")