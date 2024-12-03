import requests
from bs4 import BeautifulSoup
import csv
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fetch webpage content using requests
def fetch_page_content(url):
    """
    Fetch HTML content of a webpage using the requests library.
    """
    logging.info(f"Fetching content from {url}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info("Content fetched successfully.")
            return response.text
        else:
            logging.error(f"Failed to fetch content. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching content: {e}")
        return None

# Parse HTML content using BeautifulSoup
def parse_html(content):
    """
    Parse the HTML content and extract required information.
    """
    logging.info("Parsing HTML content...")
    soup = BeautifulSoup(content, "html.parser")
    data = []

    # Example: Extract all headings (h2 tags)
    headings = soup.find_all('h2')
    for heading in headings:
        data.append(heading.get_text(strip=True))

    logging.info(f"Extracted {len(data)} items.")
    return data

# Save the extracted data to a CSV file
def save_to_csv(data, output_file):
    """
    Save the extracted data to a CSV file.
    """
    logging.info(f"Saving extracted data to {output_file}...")
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Heading'])
            for row in data:
                writer.writerow([row])
        logging.info("Data saved successfully.")
    except Exception as e:
        logging.error(f"Error saving data: {e}")

# Main function to execute the entire scraping process
def main():
    url = "https://example.com"  # Replace with the URL of the website to scrape
    output_file = "data/extracted_data.csv"

    # Fetch page content
    content = fetch_page_content(url)
    if content is None:
        return

    # Parse the content and extract data
    data = parse_html(content)

    # Save the data to a CSV file
    save_to_csv(data, output_file)

if __name__ == "__main__":
    main()
