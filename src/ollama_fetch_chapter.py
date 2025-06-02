from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright._impl._errors import Error as PlaywrightRuntimeError
from bs4 import BeautifulSoup, Comment
import time
import random
from src.ollama_scraper import *

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags
    paragraphs = soup.find_all('p')
    print(paragraphs)


    return str(paragraphs)

def fetch_chapter():
    url = 'https://novelbin.com/b/library-of-heavens-path/chapter-1'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=False helps solve captchas
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        ]
        user_agent = random.choice(user_agents)
        context = browser.new_context(
            user_agent=user_agent,
            java_script_enabled=False  
        )
        
        page = context.new_page()
        page.goto(url)

        try:
            # Smart wait first
            time.sleep(random.randint(2, 5))
            html = page.content()
        except (PlaywrightTimeoutError, PlaywrightRuntimeError) as e:
            # Fallback: wait manually if selector didn't show
            print(f"Error loading or rendering: {url} — {e}")
            browser.close()
            return {"title": None, "content": None}

        browser.close()
        
        cleaned_html = clean_html(html)
        
        
        results = extract_with_ai(cleaned_html)
        
        
        return results