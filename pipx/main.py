import newspaper
import sqlite3
from sqlite3 import Error

# Function to create SQLite connection and table
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
def save_article_to_db(conn, article_data):
    sql = ''' INSERT INTO articles(url, title, content, authors, publish_date, top_image)
              VALUES(?,?,?,?,?,?) '''
    cursor = conn.cursor()
    cursor.execute(sql, article_data)
    conn.commit()

# Function to scrape and save an article using newspaper4k
def scrape_article(url, conn):
    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()

        # Extract required information
        title = article.title
        text = article.text
        authors = ', '.join(article.authors) if article.authors else "Unknown"
        publish_date = article.publish_date.strftime('%Y-%m-%d') if article.publish_date else "Unknown"
        top_image = article.top_image if article.top_image else "None"

        # Print article details (for debugging)
        print(f"Title: {title}")
        print(f"Authors: {authors}")
        print(f"Publish Date: {publish_date}")
        print(f"Top Image: {top_image}")
        print(f"Content: {text[:500]}...")  # Limit printed text for preview

        # Save to SQLite
        article_data = (url, title, text, authors, publish_date, top_image)
        save_article_to_db(conn, article_data)
    except Exception as e:
        print(f"Error scraping article: {e}")

if __name__ == "__main__":
    # Set up SQLite connection and table
    database = "news_articles.db"
    conn = create_connection(database)
    if conn:
        create_table(conn)

        # Example URLs of news articles
        article_urls = [
            "https://www.29news.com/2024/09/24/procrastination-not-caused-by-laziness-uva-expert-says/",
            "https://www.ft.com/content/fba9d4ed-83bc-4730-baa7-c9a995021398",
            # Add more URLs here...
        ]

        # Scrape and save each article
        for url in article_urls:
            scrape_article(url, conn)

        # Close the connection
        conn.close()