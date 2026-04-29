import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling

load_dotenv()

def dbConnect():
    try:
        db = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=os.getenv('DB_POOL'),
            pool_size=5,
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_DATABASE')
        )
    except ConnectionError as ex:
        print(ex)
        return None
    
    return db.get_connection()