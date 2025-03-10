"""
Main application - Entry point untuk SQL Translator API.
"""
import uuid
import time
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import Config, setup_openai
from app.models.api_models import QueryInput, QueryResult
from app.middleware.logging_middleware import LoggingMiddleware
from app.services.ddl_manager import DDLManager
from app.services.llm_service import LLMService
from app.services.database_service import DatabaseService

# Get logger instance
logger = logging.getLogger(__name__)

# Setup OpenAI configuration
setup_openai()

# Initialize FastAPI application
app = FastAPI(
    title="SQL Translator API",
    description="API untuk menerjemahkan konteks natural language menjadi SQL query",
    version="1.0.0"
)

# Add middlewares
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)
app.middleware("http")(LoggingMiddleware())


@app.get("/health")
async def health_check():
    """
    Endpoint sederhana untuk health check.
    
    Returns:
        dict: Status kesehatan API
    """
    return {"status": "healthy", "timestamp": time.time()}


@app.post("/translate_sql", response_model=QueryResult)
async def translate_sql(query_input: QueryInput, request: Request):
    """
    Endpoint untuk menerjemahkan konteks natural language menjadi SQL query
    dan mengeksekusi query tersebut ke database.
    
    Args:
        query_input: Input berisi konteks yang akan diterjemahkan
        request: FastAPI Request object
        
    Returns:
        QueryResult: SQL query dan hasil eksekusinya
        
    Raises:
        HTTPException: Jika terjadi error selama proses
    """
    request_id = str(uuid.uuid4())
    logger.info(f"Processing translate_sql request {request_id}")
    
    try:
        # Validasi input
        if not query_input.question.strip():
            error_msg = "Question tidak boleh kosong"
            logger.warning(f"Request {request_id}: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Load DDL
        try:
            ddl = DDLManager.load_ddl()
        except (FileNotFoundError, IOError) as e:
            logger.error(f"Request {request_id}: DDL loading error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        
        # Terjemahkan ke SQL
        try:
            sql_query = LLMService.translate_to_sql(query_input.question, ddl, "SQL Server", 
                    "Khusus untuk parameter hari dalam bahasa inggris, selain itu SEMUA parameter lain HARUS dalam bahasa Indonesia. \
                    Selalu gunakan hospital_id = 1 dan location_id = 2. Untuk spesialisasi, JANGAN masukkan kata dokter. ")
        except Exception as e:
            logger.error(f"Request {request_id}: Translation error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        
        # Eksekusi SQL query
        try:
            result = DatabaseService.execute_sql_query(sql_query)
        except Exception as e:
            logger.error(f"Request {request_id}: Database error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        
        # Kembalikan hasil
        logger.info(f"Request {request_id} completed successfully")
        return QueryResult(
            request_id=request_id,
            sql_query=sql_query,
            result=result
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log unexpected errors
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"Request {request_id}: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Handler yang dijalankan saat aplikasi start."""
    logger.info("==== SQL Translator API starting up ====")
    logger.info(f"LLM Provider: {Config.LLM_PROVIDER}")
    
    # Verify environment is set up correctly
    if Config.LLM_PROVIDER == 'azure' and (not Config.AZURE_OPENAI_KEY or not Config.AZURE_OPENAI_ENDPOINT):
        logger.warning("Azure OpenAI credentials not properly configured")
    elif Config.LLM_PROVIDER == 'openai' and not Config.OPENAI_API_KEY:
        logger.warning("OpenAI API key not properly configured")
    
    if not Config.CONN_STR:
        logger.warning("Database connection string not configured")
    
    # Try to validate DDL file exists
    try:
        import glob
        ddl_files = glob.glob(Config.DDL_GLOB_PATTERN)
        if not ddl_files:
            logger.warning(f"No DDL files found matching pattern: {Config.DDL_GLOB_PATTERN}")
        else:
            logger.info(f"Found DDL file: {ddl_files[0]}")
    except Exception as e:
        logger.warning(f"Error checking for DDL files: {str(e)}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Handler yang dijalankan saat aplikasi shutdown."""
    logger.info("==== SQL Translator API shutting down ====") 