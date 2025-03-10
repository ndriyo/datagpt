"""
Config - Modul untuk konfigurasi aplikasi.
"""
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Config:
    """
    Konfigurasi aplikasi yang dibaca dari environment variables.
    """
    # LLM Provider
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai').lower()
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'API_KEY')
    OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL', 'o3-mini')
    
    # Azure OpenAI Settings
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://xxx.openai.azure.com")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-26")
    AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "AZURE_OPENAI_KEY")
    AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'your-deployment-name')
    
    # Database connection
    CONN_STR = os.getenv('CONN_STR')
    
    # Application settings
    DDL_GLOB_PATTERN = "ddl*.sql"

# Setup OpenAI berdasarkan provider
def setup_openai():
    """
    Setup konfigurasi OpenAI berdasarkan provider yang dipilih.
    """
    import openai
    
    if Config.LLM_PROVIDER == 'azure':
        logger.info("Using Azure OpenAI as LLM provider")
        openai.api_type = "azure"
        openai.api_base = Config.AZURE_OPENAI_ENDPOINT
        openai.api_version = Config.AZURE_OPENAI_API_VERSION
        openai.api_key = Config.AZURE_OPENAI_KEY
    else:
        logger.info("Using OpenAI as LLM provider")
        openai.api_key = Config.OPENAI_API_KEY
        openai.api_type = "openai" 