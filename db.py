# db.py
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="park_key",
        user="postgres",      
        password="8894"  
    )
