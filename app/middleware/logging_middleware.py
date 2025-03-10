"""
Logging Middleware - Komponen untuk logging request dan responses.
"""
import time
import uuid
import logging
from fastapi import Request, Response

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    """
    Middleware untuk logging request dan response dengan timing info.
    """
    async def __call__(self, request: Request, call_next):
        """
        Process setiap request, catat waktu mulai dan selesai, serta status code.
        
        Args:
            request: FastAPI Request object
            call_next: Function untuk memanggil middleware berikutnya
            
        Returns:
            Response: FastAPI Response object
        """
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Log request info
        logger.info(f"Request {request_id} started - Method: {request.method} Path: {request.url.path}")
        
        try:
            # Process request
            response = await call_next(request)
            
            # Log completion
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id
            
            logger.info(
                f"Request {request_id} completed in {process_time:.4f}s with status code {response.status_code}"
            )
            
            return response
        except Exception as e:
            # Log failure
            process_time = time.time() - start_time
            logger.error(f"Request {request_id} failed in {process_time:.4f}s with error: {str(e)}")
            raise 