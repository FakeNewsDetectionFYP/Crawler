from openai import OpenAI
from selenium import webdriver
from PIL import Image
import pytesseract
import os

# Initialize OpenAI API key
# client

# Function to take a screenshot of a webpage and return text via OCR
def extract_content_with_ocr(url):
    try:
        # Set up Selenium with a headless browser
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Scroll to the bottom of the page to capture the full content
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, scroll_height)

        # Take a screenshot of the entire page
        screenshot_path = 'full_page_screenshot.png'
        driver.save_screenshot(screenshot_path)
        driver.quit()

        # Use OCR to extract text from the screenshot
        screenshot = Image.open(screenshot_path)
        ocr_text = pytesseract.image_to_string(screenshot)

        # Clean up the screenshot file after use
        os.remove(screenshot_path)

        # Send the extracted text to GPT for partitioning
        partitioned_content = send_text_to_gpt(ocr_text)

        return partitioned_content
    except Exception as e:
        print(f"Error during OCR extraction: {e}")
        return None

# Function to send extracted text to GPT and get structured output
def send_text_to_gpt(ocr_text):
    try:
        prompt = f"""
        You are a helpful assistant. The following is raw extracted text from a web page. Please partition it into the following sections:
        - Title
        - Content
        - Authors (if available)
        - Publish Date (if available)

        Raw Text: {ocr_text}
        """

        # Use the new ChatCompletion method
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that partitions text into structured sections."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the structured message from the response
        structured_output = completion.choices[0].message['content'].strip()
        print(f"GPT structured output: {structured_output}")

        # Return the structured content as a dictionary (or another structured format)
        return parse_gpt_output(structured_output)

    except Exception as e:
        print(f"Error during GPT processing: {e}")
        return None

# Function to parse GPT's output into a dictionary format
def parse_gpt_output(gpt_output):
    # Basic parsing logic to extract title, content, authors, etc. from the GPT output
    # This assumes GPT returns output in a format like "Title: XYZ\nContent: ABC\nAuthors: DEF"
    sections = ["Title", "Content", "Authors", "Publish Date", "Top Image"]
    partitioned = {section: "Unknown" for section in sections}

    for section in sections:
        start = gpt_output.find(f"{section}:")
        if start != -1:
            end = gpt_output.find("\n", start)
            partitioned[section] = gpt_output[start + len(f"{section}:"):end].strip()

    return partitioned