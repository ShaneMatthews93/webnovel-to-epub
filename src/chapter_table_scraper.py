import json
from playwright.sync_api import sync_playwright
import time, os, re, random
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

def table_of_content_extractor(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False helps solve captchas
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        ]
        user_agent = random.choice(user_agents)
        context = browser.new_context(
            user_agent=user_agent,
            java_script_enabled=True  
        )
        
        page = context.new_page()
        page.goto(url)
        
        # Click the "Chapter List" tab
        page.click('#tab-chapters-title')
        page.wait_for_load_state('networkidle')  # Wait for all requests to finish
        page.wait_for_selector('ul.list-chapter', timeout=15000)
        time.sleep(5)  # Slight buffer to allow rendering
        
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        links = soup.select('ul.list-chapter li a')
        
        book_title = soup.select_one('h3.title')
        book_title_text = book_title.get_text(strip=True)
        
        author_tag = soup.select_one('li h3:-soup-contains("Author:") + a')
        if not author_tag:
            # fallback if the structure is simpler
            author_tag = soup.select_one('a[href*="/a/"]')
        author_name = author_tag.get_text(strip=True) if author_tag else "Unknown Author"
        
        genre_li = None
        for li in soup.select("li"):
            if "Genre:" in li.get_text():
                genre_li = li
                break

        # Extract all <a> tags inside that <li>
        if genre_li:
            genre_tags = genre_li.find_all("a")
            genres = [a.get_text(strip=True) for a in genre_tags]
        else:
            genres = []
        book_dir = f'./Books/{book_title_text}'
        metadata_path = os.path.join(book_dir, 'metadata.json')
        toc_file = os.path.join(book_dir, 'table_of_contents_url.txt')

        # Extract the cover art
        cover_img = soup.find("img", class_="lazy")
        cover_url = cover_img["src"] if cover_img else None

        # Ensure Book folder exists
        os.makedirs(book_dir, exist_ok=True)
        
        # Load Existing URLs
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
        else:
            metadata = {
                "title": book_title_text,
                "author": author_name,
                "genres": genres,
                "cover_url": cover_url,
                "source_url": url,
                "chapter_urls": [],
                "downloaded_chapters": {}
            }
        
        existing_urls = set(metadata.get("chapter_urls", []))
        
        new_urls = []
        for link in links:
            href = link['href'].strip()
            if href not in existing_urls:
                print(f'New chapter found: {href}')
                new_urls.append(href)
            
        if new_urls:
            with open(toc_file, 'a') as f:
                for href in new_urls:
                    f.write(href + '\n')
            all_urls = list(existing_urls.union(new_urls))
            
            metadata["title"] = book_title_text
            metadata["author"] = author_name
            metadata["genres"] = genres
            metadata["cover_url"] = cover_url
            metadata["source_url"] = url
            def extract_chapter_number(url):
                match = re.search(r'chapter-(\d+)', url)
                return int(match.group(1)) if match else float('inf')

            all_urls = list(existing_urls.union(new_urls))
            all_urls.sort(key=extract_chapter_number)
            metadata["chapter_urls"] = all_urls
            if "downloaded_chapters" not in metadata:
                metadata["downloaded_chapters"] = {}
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        browser.close()
        return book_title_text
    