from fastapi import FastAPI,HTTPException
from routes import router as incidents_router
from exceptions import http_exception_handler
from models import Base
from database import engine

app=FastAPI(title="Incident Intake Service",version="1.0",debug=True)

app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(incidents_router)

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
@app.get("/health")
def health():
    return {"status": "ok"}