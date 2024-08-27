import pymysql.cursors
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DB", "rest_api_db"),
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def save_query(domain, ipv4_addresses):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO queries (domain, ipv4_addresses) VALUES (%s, %s)",  # noqa: E501
                    (domain, ','.join(ipv4_addresses))
                )
            conn.commit()
        finally:
            conn.close()


def get_recent_queries():
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM queries ORDER BY created_at DESC LIMIT 20")  # noqa: E501
                results = cursor.fetchall()
            return results
        finally:
            conn.close()
    return []
