import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """
    Crea y devuelve una conexión a la base de datos PostgreSQL.
    """
    connection = psycopg2.connect(
        dbname=os.getenv("PG_DATABASE"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT", 5432)
    )
    return connection
