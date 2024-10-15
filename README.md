Crawler Program

This program extracts URLs from a GDELT CSV export, crawls the associated webpages, and saves the extracted content (including title, authors, content, etc.) into a local SQLite database (articles.db). It can also process incomplete entries using OCR and GPT-based text partitioning if needed.

Prerequisites

Before running this program, ensure that you have the following tools and dependencies installed:

	1.	Python 3.x installed on your machine.
	2.	pip (Python package manager) to install the required Python packages.
	3.	Required Python packages: You can install the necessary packages by running the following command:

```bash
pip install -r requirements.txt
```

	4.	Additional system dependencies:
	•	Tesseract (for OCR functionality)
	•	Selenium and ChromeDriver (for web page interaction in case of OCR)
Refer to the instructions in install.sh (for macOS/Linux) or install.bat (for Windows) to set up these dependencies.

Steps to Use the Program

1. Download the CSV Export File from GDELT

	1.	Go to the GDELT Export Interface and download an export CSV file that contains a list of URLs you want to process.
	2.	Place the CSV file in the main directory of this project (the same directory as main.py).

2. Update the CSV File Name in main.py

After placing the CSV file in the main directory, follow these steps:

	1.	Open main.py in your preferred text editor.
	2.	Locate the line that sets the path to the CSV file:

```python
csv_file = "your_csv_file_name.csv"
```

	3.	Update your_csv_file.csv to the name of your downloaded CSV file.

3. Run the Program

After updating the CSV file name, you can run the program from your terminal:

	1.	Open a terminal or command prompt.
	2.	Navigate to the directory where main.py is located.
	3.	Run the following command:

```bash
python main.py
```

4. Select an Option from the Menu

Once you run the program, you will be prompted with a menu offering the following options:

	•	Option 1: Extract URLs from the CSV and run the crawler. This will scrape the articles from the URLs in the CSV and save them to the articles.db database.
	•	Option 2: Check and update incomplete entries in articles.db using OCR and GPT. This will allow you to process entries with missing titles or content using OCR and GPT.
	•	Option 3: Exit the program.

Simply type 1, 2, or 3 based on your choice, and press Enter to execute the corresponding action.

5. Viewing Results

The results of the crawler, including extracted article data, are stored in the databases/articles.db SQLite database. You can inspect this database using an SQLite viewer or any SQL database tool of your choice.

6. Reviewing Failed URLs

If the program fails to extract content from certain URLs, those URLs are logged in a file named failed_urls.log in the main directory. You can review these URLs later and decide if you’d like to handle them manually or rerun the program.

Additional Notes

	•	Error Handling: If extraction fails for any URL (e.g., due to restrictions on the website), the program will log the URL in failed_urls.log and move on to the next one.
	•	OCR and GPT Processing: OCR processing is only triggered when explicitly requested by the user in the menu, and it will only attempt to fill in missing titles and content (leaving url and top_image unchanged).

