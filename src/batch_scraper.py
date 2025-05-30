from src.fetch_chapter import fetch_chapter
from src.epub_builder import build_epub
import random, json
import time
import sys


def fetch_multi_chapters(book_metadata_path):
    with open(book_metadata_path, 'r') as f:
        metadata = json.load(f)
        
    downloaded_chapters = metadata.get("downloaded_chapters", {})
    all_urls = metadata.get("chapter_urls", [])
    total = len(all_urls)

    def fetch_and_store(i, url):
        result = fetch_chapter(url)
        if result['title'] and result['content']:
            print(f"✅ Success fetching Chapter {i}: {result['title']}")
            downloaded_chapters[url] = result

            # Save to file immediately
            metadata['downloaded_chapters'] = downloaded_chapters
            with open(book_metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            time.sleep(random.uniform(0, 2.9))
            return result
        else:
            print(f"❌ Failed to fetch Chapter {i}")
            return None
        
    
    chapters = [downloaded_chapters.get(url) for url in all_urls]
    failed = []
        
    for i, url in enumerate(all_urls, start=1):
        if url in downloaded_chapters:
            print(f"✅ Cached Chapter {i}/{total}: {url}")
            continue
        result = fetch_and_store(i, url)        
        chapters[i - 1] = result
        if result is None:
            failed.append((i, url))
             
        sys.stdout.flush()
    
    while failed:
        print(f"\n🔁 Retrying {len(failed)}")
        next_failed = []    

        for i, url in failed:
            result = fetch_and_store(i, url)
            print(i, url)
            print(result)
            
            if result is not None:
                chapters[i - 1] = (i, result)
            else:
                next_failed.append((i, url))
                
            time.sleep(random.uniform(0.0, 4.1))
            sys.stdout.flush()
        failed = next_failed

        
    metadata['downloaded_chapters'] = downloaded_chapters
    
    with open(book_metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    build_epub(book_metadata_path)
    
    return [ch for ch in chapters if ch]
