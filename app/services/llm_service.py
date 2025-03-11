"""
LLM Service - Layanan untuk berinteraksi dengan model bahasa (Language Model).
"""
import openai
import logging
from app.config import Config

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service untuk berinteraksi dengan model bahasa seperti OpenAI atau Azure OpenAI.
    """
    @staticmethod
    def translate_to_sql(context: str, ddl: str, db: str, db_specific: str) -> str:
        """
        Menggunakan LLM untuk menerjemahkan konteks natural language menjadi SQL query.
        
        Args:
            context: Konteks atau pertanyaan dalam bahasa natural
            ddl: DDL database yang berisi struktur tabel dan kolom
            
        Returns:
            str: SQL query yang dihasilkan
            
        Raises:
            Exception: Jika terjadi error saat memanggil API OpenAI
        """
        logger.info("Translating natural language to SQL query")
        
        system_message = """Kamu adalah SQL expert yang mengubah permintaan bahasa natural menjadi query SQL yang valid dan efisien. 
Pikirkan terlebih dahulu permintaan user baik-baik, kemudian gunakan DDL database yang diberikan sebagai referensi untuk membuat 
query yang benar dan buat query dengan merujuk pada master data yang dirujuk sehingga informasi yang ditampilkan bukan hanya id, 
tapi code, nama atau deskripsi di tabel rujukan. Gunakan pencarian menggunakan operator LIKE dengan % agar lebih fleksibel. 
JANGAN pernah gunakan reserved keyword seperti AND, OR sebagai alias dari tabel atau field.
Hanya berikan SQL query sebagai output, tanpa penjelasan atau komentar tambahan atau ```. 

"""
        
        user_message = f"""# DDL Database:
{ddl}

# Permintaan: 
{context}

# Aturan database:
{db_specific}

# Database: 
{db}

# Transformasikan permintaan di atas menjadi SQL query yang valid.
# Hanya berikan SQL query sebagai output, tanpa penjelasan atau komentar atau tag ```, HANYA SQL query.
"""
        
        try:
            request_params = {
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.1,  # Output yang lebih deterministik
                "max_tokens": 1000   # Token yang cukup untuk query kompleks
            }
            
            if Config.LLM_PROVIDER == 'azure':
                request_params["engine"] = Config.AZURE_OPENAI_DEPLOYMENT
                logger.info(f"Calling Azure OpenAI with deployment: {Config.AZURE_OPENAI_DEPLOYMENT}")
            else:
                request_params["model"] = Config.OPENAI_MODEL_NAME
                logger.info(f"Calling OpenAI with model: {Config.OPENAI_MODEL_NAME}")
            
            response = openai.ChatCompletion.create(**request_params)
            sql_query = response.choices[0].message.content.strip()
            
            logger.info(f"Generated SQL query: {sql_query}")
            
            return sql_query
        except Exception as e:
            error_msg = f"Error saat memanggil OpenAI API: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) 