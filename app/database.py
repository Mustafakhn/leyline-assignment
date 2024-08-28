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
            database=os.getenv("MYSQL_DB", "leyline_db"),
            cursorclass=pymysql.cursors.DictCursor
        )
        initialize_database()
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def initialize_database():
    # Create a connection to MySQL without specifying the database to create it
    try:
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('MYSQL_DB', 'leyline_db')}")  # noqa: E501
            # Select the database
            cursor.execute(f"USE {os.getenv('MYSQL_DB', 'leyline_db')}")
            # Create the table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS queries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    domain VARCHAR(255) NOT NULL,
                    ipv4_addresses TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        connection.commit()
        print("Database and table initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        connection.close()


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
        except Exception as e:
            print(f"Error saving query: {e}")
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
        except Exception as e:
            print(f"Error fetching recent queries: {e}")
        finally:
            conn.close()
    return []
