from mysql.connector import pooling, Error
from app.log_utils import get_daily_logger
import os

logger = get_daily_logger()

pool = pooling.MySQLConnectionPool(
    pool_name="main_pool",
    pool_size=10,
    host=os.getenv("DBHOST"),
    database=os.getenv("DBNAME"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASSWORD"),
    autocommit=True
)

def get_conn():
    try:
        return pool.get_connection()
    except Error as e:
        print(f"Error obteniendo conexión del pool: {e}")
        logger.info(f"Error obteniendo conexión del pool: {e}")
        return None
    