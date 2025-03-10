"""
Database Service - Layanan untuk berinteraksi dengan database.
"""
import pyodbc
import logging
import time
from contextlib import contextmanager
from typing import Dict, List, Any, Optional
from app.config import Config

logger = logging.getLogger(__name__)


class DatabaseService:
    """
    Service untuk berinteraksi dengan database melalui ODBC.
    """
    @staticmethod
    @contextmanager
    def get_connection():
        """
        Context manager untuk koneksi database.
        
        Yields:
            Connection: Koneksi database pyodbc
            
        Raises:
            ValueError: Jika connection string tidak ditemukan
            Exception: Jika terjadi error saat koneksi database
        """
        if not Config.CONN_STR:
            error_msg = "Connection string tidak ditemukan di environment variable CONN_STR"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        conn = None
        try:
            logger.info("Establishing database connection")
            logger.info(f"Connection string: {Config.CONN_STR}")
            conn = pyodbc.connect(Config.CONN_STR)
            yield conn
            logger.info("Database operation completed successfully")
        except Exception as e:
            error_msg = f"Database connection error: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        finally:
            if conn:
                logger.debug("Closing database connection")
                conn.close()
    
    @classmethod
    def execute_sql_query(cls, query: str) -> Dict[str, Any]:
        """
        Mengeksekusi SQL query dan mengembalikan hasilnya.
        
        Args:
            query: SQL query yang akan dieksekusi
            
        Returns:
            Dict[str, Any]: Hasil eksekusi query
            
        Raises:
            Exception: Jika terjadi error saat eksekusi query
        """
        logger.info("Executing SQL query")
        logger.debug(f"SQL Query: {query}")
        
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            start_time = time.time()
            
            try:
                cursor.execute(query)
                execution_time = time.time() - start_time
                logger.info(f"Query executed in {execution_time:.4f} seconds")
                
                if cursor.description:  # Jika query SELECT, ambil hasilnya
                    rows = cursor.fetchall()
                    columns = [column[0] for column in cursor.description]
                    result = [dict(zip(columns, row)) for row in rows]
                    logger.info(f"Query returned {len(result)} rows")
                else:  # Jika bukan SELECT, kembalikan info rows affected
                    result = {"message": "Query executed successfully", "rows_affected": cursor.rowcount}
                    logger.info(f"Non-SELECT query affected {cursor.rowcount} rows")
                
                return result
            except Exception as e:
                error_msg = f"Error executing SQL query: {str(e)}"
                logger.error(error_msg)
                logger.error(f"Failed query: {query}")
                raise Exception(error_msg)
            finally:
                cursor.close() 