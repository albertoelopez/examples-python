from restack_ai.function import function, log
import requests
from bs4 import BeautifulSoup

@function.defn(name="crawl_website")
async def crawl_website(url_and_headers: tuple) -> str:
    url, headers = url_and_headers
    try:
        # Create a session to handle cookies
        session = requests.Session()
        
        # First make a GET request to the main page to get any necessary cookies
        main_page = "https://www.lacourt.org/"
        session.get(main_page, headers=headers)
        
        # Now make the actual request with the same session
        response = session.get(url, headers=headers, allow_redirects=True)
        
        if response.status_code != 200:
            log.error(f"Request failed with status code: {response.status_code}")
            log.error(f"Response content: {response.text}")
            return f"Error accessing case information. Status code: {response.status_code}"

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the text content from the page
        content = soup.get_text(separator=' ', strip=True)
        
        log.info("crawl_website success", extra={"status": response.status_code})
        
        return content

    except Exception as e:
        log.error("crawl_website function failed", extra={"error": str(e)})
        return f"Error accessing case information: {str(e)}"
