# db_utils.py
import sqlalchemy as sa
from sqlalchemy.engine import URL
import psycopg2
from config import *

_engine = None

def get_engine():
    global _engine
    if not _engine:
        url = URL.create(
            drivername=DB_DRIVER,
            username=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        _engine = sa.create_engine(url, pool_size=10, max_overflow=20)
    return _engine

def get_db_connection():
    return psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME
    )