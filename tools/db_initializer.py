import os
import sqlite3
from sqlite3 import Error

# Function to create SQLite connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite {db_file}")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

# Function to create articles table in articles.db
def create_articles_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                authors TEXT,
                publish_date TEXT,
                top_image TEXT
            )
        ''')
        conn.commit()
        print("Articles table created.")
    except Error as e:
        print(f"Error creating articles table: {e}")

# Function to create URLs table in urls_gdelt.db
def create_urls_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                isExtracted INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        print("URLs table created.")
    except Error as e:
        print(f"Error creating URLs table: {e}")

# Function to initialize both databases
def initialize_databases(db_directory):
    articles_db = os.path.join(db_directory, "articles.db")
    urls_db = os.path.join(db_directory, "urls_gdelt.db")

    # Ensure the databases directory exists
    os.makedirs(db_directory, exist_ok=True)

    # Initialize articles.db
    articles_conn = create_connection(articles_db)
    if articles_conn:
        create_articles_table(articles_conn)
        articles_conn.close()

    # Initialize urls_gdelt.db
    urls_conn = create_connection(urls_db)
    if urls_conn:
        create_urls_table(urls_conn)
        urls_conn.close()