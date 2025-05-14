from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.dashboard import router as dashboard
from routes.add_report import router as add_report
from routes.db_setup import router as db_setup
from fastapi.middleware.cors import CORSMiddleware
from databases.database import Base, engine
import models
from services.sql_runner import run_sql_file

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

# Add CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Authentication Router
app.include_router(auth_router, prefix="/auth")
app.include_router(dashboard, prefix="/api", tags=["Dashboard"])
app.include_router(add_report, prefix="/api", tags=["Report"])
app.include_router(db_setup, prefix="/api", tags=["DB Setup"])

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Authentication"}

@app.get("/test")
def test():
    return {"message": "Swagger should work"}

@app.get("/create-tables")
def create_tables():
    Base.metadata.create_all(bind=engine)
    return {"message": "Tables created successfully"}

