from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright._impl._errors import Error as PlaywrightRuntimeError
from bs4 import BeautifulSoup
import time
import random

def fetch_chapter(url):
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
        soup = BeautifulSoup(html, "html.parser")

        title_tag = soup.select_one("h2 .chr-text")
        title_text = title_tag.get_text(strip=True) if title_tag else None

        content_div = soup.select_one("#chr-content")
        paragraphs = content_div.find_all("p") if content_div else []
        chapter_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
        results = {
            "title": title_text,
            "content": chapter_text
        }
        
        return results