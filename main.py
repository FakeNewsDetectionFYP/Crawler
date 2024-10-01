import newspaper
import sqlite3
import nltk
from sqlite3 import Error

nltk.download('punkt_tab')

# Function to create SQLite connection and table
# @param db_file: SQLite database file
# @return: SQLite connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite {db_file}")
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                authors TEXT,
                publish_date TEXT,
                top_image TEXT
            )
        ''')
        conn.commit()
    except Error as e:
        print(e)

# Function to save article to SQLite database
# @param conn: SQLite connection
# @param article: Dictionary containing the article information
def save_article(conn, article):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (url, title, content, authors, publish_date, top_image)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (article['url'], article['title'], article['content'], article['authors'], article['publish_date'], article['top_image']))
        conn.commit()
    except Error as e:
        print(f"Error saving article: {e}")

# Function to scrape a single article using newspaper4k
# @param url: URL of the article to scrape
# @return: Dictionary containing the article information
def scrape_article(url):
    try:
        article = newspaper.Article(url, request_timeout=10)  # Set request timeout to 10 seconds
        article.download()
        article.parse()

        publish_date = article.publish_date.strftime('%Y-%m-%d') if article.publish_date else "Unknown"
        return {
            'url': article.url,
            'title': article.title,
            'content': article.text,
            'authors': ', '.join(article.authors) if article.authors else "Unknown",
            'publish_date': publish_date,
            'top_image': article.top_image or "None"
        }
    except Exception as e:
        print(f"Error scraping article: {e}")
        return None

# Main function
def main():
    database = "articles.db"
    news_url = "https://www.usatoday.com/story/news/nation/2024/09/29/hurricane-helene-climate-change-florida-storms-intensify/75429855007/"

    # Create a database connection
    conn = create_connection(database)
    if conn is not None:
        # Create articles table
        create_table(conn)

        # Scrape the article
        article = scrape_article(news_url)

        # Save article to database
        if article:
            save_article(conn, article)

        # Close the connection
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()


# 