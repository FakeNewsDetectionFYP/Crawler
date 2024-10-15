import re
import os
import csv
import sqlite3

# Function to fetch unprocessed URLs from the database
def fetch_urls_from_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        # Fetch URLs where isExtracted = 0 (unprocessed)
        cursor.execute('SELECT url FROM urls WHERE isExtracted = 0')
        urls = [row[0] for row in cursor.fetchall()]
        return urls
    except sqlite3.Error as e:
        print(f"Error fetching URLs from database: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Function to insert a URL into the database
def save_url_to_db(db_file, url):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        # Insert URL into the table with isExtracted = 0 (unprocessed)
        cursor.execute('''
            INSERT OR IGNORE INTO urls (url, isExtracted)
            VALUES (?, 0)
        ''', (url,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving URL to database: {e}")
    finally:
        if conn:
            conn.close()

# Function to extract links from a CSV file and store them in the database
def extract_links_from_csv(file_path, db_directory):
    try:
        # Define the database file path for urls_gdelt.db
        db_file = os.path.join(db_directory, "urls_gdelt.db")

        # Use the csv module to read the CSV file
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')

            # Regex to identify valid URLs
            url_pattern = re.compile(r'(https?://\S+)')

            extracted_urls = set()  # Use a set to store unique URLs

            # Process each row in the CSV
            for row in csvreader:
                # Search for URLs in each cell of the row
                for cell in row:
                    urls = re.findall(url_pattern, cell)
                    for url in urls:
                        clean_url = url.rstrip('",')  # Clean any trailing commas/quotes
                        extracted_urls.add(clean_url)

        # Log how many URLs were found initially
        print(f"Found {len(extracted_urls)} unique URLs in the CSV.")

        # Save each unique URL to the database
        for url in extracted_urls:
            print(f"Saving URL to database: {url}")  # Log each URL being saved
            save_url_to_db(db_file, url)

        print(f"Extracted and saved {len(extracted_urls)} unique URLs to the database.")
    except Exception as e:
        print(f"Error extracting links: {e}")