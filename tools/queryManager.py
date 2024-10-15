import os
import sqlite3
from crawler.crawler import run_crawler
from tools.link_extractor import extract_links_from_csv
from crawler.crawler import run_ocr_for_incomplete_articles

# Function to check and update incomplete entries in articles.db
def check_and_update_articles(db_directory):
    articles_db = os.path.join(db_directory, "articles.db")
    conn = sqlite3.connect(articles_db)
    cursor = conn.cursor()

    # Query to find entries with empty title or content
    cursor.execute('SELECT id, url, title, content FROM articles WHERE title IS NULL OR title = "" OR content IS NULL OR content = ""')
    incomplete_entries = cursor.fetchall()

    if not incomplete_entries:
        print("No incomplete entries found in the database.")
        return

    print(f"Found {len(incomplete_entries)} incomplete entries. Processing them...")

    # Process each incomplete entry
    for entry in incomplete_entries:
        entry_id, url, title, content = entry
        print(f"Processing entry ID: {entry_id} with URL: {url}")

        # Extract content via OCR and GPT
        ocr_content = extract_content_with_ocr(url)
        if ocr_content:
            # Do not update publish_date or top_image
            updated_title = ocr_content['title'] if ocr_content['title'] != "Unknown" else title
            updated_content = ocr_content['content'] if ocr_content['content'] != "Unknown" else content

            # Update the database with the newly partitioned title and content
            cursor.execute('UPDATE articles SET title = ?, content = ? WHERE id = ?', (updated_title, updated_content, entry_id))
            conn.commit()
            print(f"Updated entry ID: {entry_id} with new content.")

    conn.close()

# Function to handle user queries (menu options)
def handle_user_queries(db_directory, csv_file_path):
    while True:
        print("\nPlease choose an option:")
        print("1. Extract URLs from CSV and run crawler")
        print("2. Check and update incomplete entries in articles.db (OCR + GPT)")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            # Extract links from the CSV and run the crawler
            print("Extracting URLs from CSV...")
            extract_links_from_csv(csv_file_path, db_directory)
            print("Starting the crawling process...")
            run_crawler(db_directory)

        elif choice == "2":
            # Check and update incomplete entries in the database
            print("Checking for incomplete entries in articles.db...")
            run_ocr_for_incomplete_articles(db_directory)

        elif choice == "3":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")