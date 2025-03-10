"""
DDL Manager - Modul untuk mengelola DDL (Data Definition Language) database.
"""
import glob
import logging
from app.config import Config

logger = logging.getLogger(__name__)


class DDLManager:
    """
    Class untuk mengelola operasi terkait DDL database.
    """
    @staticmethod
    def load_ddl() -> str:
        """
        Memuat file DDL dengan pattern dari Config.DDL_GLOB_PATTERN.
        
        Returns:
            str: Konten file DDL
            
        Raises:
            FileNotFoundError: Jika file tidak ditemukan
            IOError: Jika terjadi error saat membaca file
        """
        logger.info(f"Looking for DDL files with pattern: {Config.DDL_GLOB_PATTERN}")
        ddl_files = glob.glob(Config.DDL_GLOB_PATTERN)
        
        if not ddl_files:
            error_msg = f"DDL file tidak ditemukan dengan pattern '{Config.DDL_GLOB_PATTERN}'"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        ddl_file = ddl_files[0]
        logger.info(f"Loading DDL from file: {ddl_file}")
        
        try:
            with open(ddl_file, 'r') as f:
                ddl = f.read()
            logger.debug(f"DDL loaded successfully, size: {len(ddl)} characters")
            return ddl
        except Exception as e:
            error_msg = f"Failed to read DDL file: {str(e)}"
            logger.error(error_msg)
            raise IOError(error_msg) 