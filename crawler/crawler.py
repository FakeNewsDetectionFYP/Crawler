import os
import sqlite3
import newspaper
from sqlite3 import Error
from tools.link_extractor import fetch_urls_from_db
from crawler.crawler_ocr import extract_content_with_ocr

# Function to create connection to SQLite
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

# Function to scrape articles and save to database
def scrape_article(url):
    try:
        article = newspaper.Article(url, request_timeout=10)
        article.download()
        article.parse()

        # Check if content or title is invalid
        if not article.text or len(article.text) < 50 or len(article.title) < 15:
            print(f"Content extraction failed or is restricted for {url}.")
            return None
        else:
            publish_date = article.publish_date.strftime('%Y-%m-%d') if article.publish_date else "Unknown"
            return {
                'url': url,
                'title': article.title,
                'content': article.text,
                'authors': ', '.join(article.authors) if article.authors else "Unknown",
                'publish_date': publish_date,
                'top_image': article.top_image or "None"
            }
    except Exception as e:
        print(f"Error scraping article: {e}")
        return None

# Function to save the article to the articles.db
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

# Function to mark a URL as extracted, even if extraction failed
def mark_url_as_extracted(db_file, url, is_extracted):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE urls SET isExtracted = ? WHERE url = ?', (is_extracted, url))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error marking URL as extracted: {e}")
    finally:
        if conn:
            conn.close()

# Function to log failed URLs
def log_failed_url(url):
    with open("failed_urls.log", "a") as log_file:
        log_file.write(f"{url}\n")

# Function to run the crawler
def run_crawler(db_directory):
    urls_db = os.path.join(db_directory, "urls_gdelt.db")
    articles_db = os.path.join(db_directory, "articles.db")

    # Fetch unprocessed URLs from the database
    article_urls = fetch_urls_from_db(urls_db)

    # Create a database connection for articles
    conn = create_connection(articles_db)
    if conn is not None:
        for url in article_urls:
            print(f"Processing URL: {url}")
            article = scrape_article(url)
            if article:
                save_article(conn, article)
                # Mark the URL as extracted (successful extraction)
                mark_url_as_extracted(urls_db, url, 1)
            else:
                print(f"Skipping URL due to failed extraction: {url}")
                # Mark the URL as extracted to prevent retries, but log it for review
                mark_url_as_extracted(urls_db, url, 1)
                log_failed_url(url)  # Log the failed URL for further investigation
        conn.close()
    else:
        print("Error! Cannot create the articles database connection.")

# Function to process OCR for specific articles
def run_ocr_for_incomplete_articles(db_directory):
    articles_db = os.path.join(db_directory, "articles.db")
    conn = sqlite3.connect(articles_db)
    cursor = conn.cursor()

    # Query to find entries with missing title or content
    cursor.execute('SELECT id, url, title, content, top_image FROM articles WHERE title IS NULL OR title = "" OR content IS NULL OR content = ""')
    incomplete_entries = cursor.fetchall()

    if not incomplete_entries:
        print("No incomplete entries found in the database.")
        return

    print(f"Found {len(incomplete_entries)} incomplete entries. Processing them...")

    for entry in incomplete_entries:
        entry_id, url, title, content, top_image = entry
        print(f"Processing entry ID: {entry_id} with URL: {url}")

        # Extract content via OCR and GPT
        ocr_content = extract_content_with_ocr(url)
        if ocr_content:
            # Ensure url and top_image remain unchanged
            updated_title = ocr_content['title'] if ocr_content['title'] != "Unknown" else title
            updated_content = ocr_content['content'] if ocr_content['content'] != "Unknown" else content

            # Update the database with the newly partitioned title and content (but not url or top_image)
            cursor.execute('UPDATE articles SET title = ?, content = ? WHERE id = ?', (updated_title, updated_content, entry_id))
            conn.commit()
            print(f"Updated entry ID: {entry_id} with new content.")

    conn.close()