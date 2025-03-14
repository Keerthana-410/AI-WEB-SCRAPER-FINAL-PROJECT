from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the AUTH variable from the .env file
AUTH = os.getenv("AUTH")

# Construct the SBR_WEBDRIVER URL using the AUTH variable
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape_website(website):
    print("Connecting to Scraping Browser...")
    if not SBR_WEBDRIVER:
        raise ValueError("SBR_WEBDRIVER environment variable not set.")
    try:
        # Establishing connection to the WebDriver
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            driver.get(website)
            print("Waiting for captcha to solve...")
            
            # Wait for captcha solution
            solve_res = driver.execute(
                "executeCdpCommand",
                {
                    "cmd": "Captcha.waitForSolve",
                    "params": {"detectTimeout": 10000},
                },
            )
            print("Captcha solve status:", solve_res["value"]["status"])
            print("Navigated! Scraping page content...")
            
            # Get the HTML content of the page
            html = driver.page_source
            return html
    except Exception as e:
        print(f"Error scraping the website: {e}")
        return None

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove all <script> and <style> elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    """Split the content into chunks of `max_length` characters."""
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]
