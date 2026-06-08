import psycopg 
from app.core.config import DATABASE_URL

conn = psycopg.connect(DATABASE_URL)