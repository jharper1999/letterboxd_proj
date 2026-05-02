import cloudscraper
from lxml import html
import time


def request_via_cloudscraper(url: str, file: str, test: bool = False) -> html:
    fname = "C:\\Users\\josep\\Documents\\letterboxd_proj\\scraping\\" + file + ".html"
    if test == False:
        scraper = cloudscraper.create_scraper()
        """Route request through cloudscraper to bypass Cloudflare protection."""
        
        response = scraper.get(url, timeout=30)
        if response.status_code == 403:
            time.sleep(3)
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url, timeout=30)
        
        if response.status_code != 200:
            raise LookupError(f"Letterboxd Error: HTTP {response.status_code} for URL: {url}")
        
        response.encoding = response.apparent_encoding
        # for testing without always scraping letterboxd    
        with open(fname, 'wb') as f:
            f.write(response.content)

        return response.content
    elif test == True:
        HtmlFile = open(fname, 'r', encoding='utf-8')
        return HtmlFile