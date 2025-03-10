"""
Application entry point for the SQL Translator API.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,  # Auto-reload on file changes (development only)
        log_level="info"
    ) 