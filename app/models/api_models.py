"""
API Models - Berisi model-model Pydantic untuk validasi request dan response.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional


class QueryInput(BaseModel):
    """Model input untuk API SQL Translator"""
    question: str = Field(..., 
                         description="Konteks atau pertanyaan dalam bahasa natural yang ingin diterjemahkan ke SQL")


class QueryResult(BaseModel):
    """Model output dari API SQL Translator"""
    request_id: str = Field(..., description="ID unik untuk request")
    sql_query: str = Field(..., description="SQL query yang dihasilkan")
    result: Any = Field(..., description="Hasil eksekusi SQL query")


class ErrorResponse(BaseModel):
    """Model untuk response error"""
    detail: str = Field(..., description="Detail pesan error") 