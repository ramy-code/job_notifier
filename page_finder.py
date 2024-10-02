from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def get_page(page_url):
    """Fetches the HTML content of the specified page URL using Selenium."""
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (optional)
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Automatically download and install the ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(page_url)  # Navigate to the page
        time.sleep(5)  # Wait for the JavaScript to load (increase if necessary)
        
        # Get the page source after the JavaScript has executed
        html = driver.page_source
        return html
    finally:
        driver.quit()  # Close the browser

def find_all_links(html):
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    anchor_tags = soup.find_all('a')

    # Extract the href attributes from the <a> tags
    filtered_links = [
        a['href'] for a in anchor_tags 
        if 'href' in a.attrs and '/companies/' in a['href'] and '/jobs/' in a['href']
    ]

    return filtered_links

if __name__ == "__main__":
    base_url = "https://www.welcometothejungle.com/fr/jobs?refinementList%5Boffices.country_code%5D%5B%5D=FR&refinementList%5Bcontract_type%5D%5B%5D=internship&aroundLatLng=48.85717%2C2.3414&page=1&aroundRadius=20&aroundQuery=Paris%2C%20France&query=computer%20vision"  # Replace with the actual job board URL
    page = get_page(base_url)
    all_links = find_all_links(page)
    all_links = ["https://www.welcometothejungle.com" + link for link in all_links]
    
    print(f"Found {len(all_links)} links:")
    for link in all_links:
        print(link)  # Print each found link
