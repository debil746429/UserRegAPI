from app.core.config import settings
import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name
    )
    try:
        yield connection # FastAPI handles the 'self' and injection
    finally:
        connection.close() # Safely closes after the API request is done

