# routers/setup.py
from fastapi import APIRouter, File, UploadFile, FastAPI
from services.sql_runner import run_sql_file
from databases. database import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os
import shutil
import sqlparse

router = APIRouter()

@router.post("/upload-sql/")
async def upload_sql_file(file: UploadFile = File(...)):
    # Save the uploaded SQL file temporarily
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read and execute the SQL file
    with open(temp_path, "r", encoding="utf-8") as f:
        sql_commands = f.read()
    
    with engine.connect() as conn:
        for statement in sql_commands.strip().split(';'):
            stmt = statement.strip()
            if stmt:
                conn.execute(text(stmt))
        conn.commit()

    # Delete the file after execution
    os.remove(temp_path)
    return {"message": "SQL executed successfully"}

@router.post("/upload-sql-crawling/")
async def upload_sql_file_crawling(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(temp_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()

        # Parse and execute statements safely (this handles semicolons inside strings)
        statements = sqlparse.split(sql_content)
        for stmt in statements:
            clean_stmt = stmt.strip()
            if clean_stmt:
                cursor.execute(clean_stmt)

        connection.commit()
    except Exception as e:
        if connection:
            try:
                connection.rollback()
            except Exception:
                pass
        raise e
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass
        os.remove(temp_path)

    return {"message": "SQL executed successfully"}

@router.post("/setup-db/mst_parameter")
def setup_db():
    run_sql_file("seeds/mst_parameter.sql")
    return {"message": "mst_parameter created successfully"}

@router.post("/setup-db/cache")
def setup_db():
    run_sql_file("seeds/cache.sql")
    return {"message": "cache created successfully"}

@router.post("/setup-db/cms_client_reports")
def setup_db():
    run_sql_file("seeds/cms_client_reports (1).sql")
    return {"message": "cms_client_reports created successfully"}

@router.post("/setup-db/crawling_website_products")
def setup_db():
    run_sql_file("seeds/crawling_website_products (20).sql")
    return {"message": "crawling_website_products created successfully"}

@router.post("/setup-db/crawling_website_products_crawl_history")
def setup_db():
    run_sql_file("seeds/crawling_website_products_crawl_history (6).sql")
    return {"message": "crawling_website_products_crawl_history created successfully"}

@router.post("/setup-db/crawling_websites")
def setup_db():
    run_sql_file("seeds/crawling_websites.sql")
    return {"message": "crawling_websites created successfully"}

@router.post("/setup-db/summary_description_split")
def setup_db():
    run_sql_file("seeds/summary_description_split (1) (1).sql")
    return {"message": "summary_description_split created successfully"}

@router.post("/setup-db/summary_description_split_description_link")
def setup_db():
    run_sql_file("seeds/summary_description_split_description_link (2) (1).sql")
    return {"message": "summary_description_split_description_link created successfully"}

