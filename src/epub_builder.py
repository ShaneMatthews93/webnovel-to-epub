from ebooklib import epub
from bs4 import BeautifulSoup
import os, json, requests, re

def extract_chapter_number(url, chapter_data):
   # First, try to get it from the URL
    url_patterns = [
        r'chapter[-_](\d+)',
        r'chatper[-_](\d+)',
        r'chap[-_](\d+)',
        r'(\d+)',
    ]
    for pattern in url_patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return int(match.group(1))

    # Fallback: Try extracting number from title by splitting
    title = chapter_data.get("title", "")
    if title.lower().startswith("chapter"):
        parts = title.split()
        if len(parts) > 1 and parts[1].isdigit():
            return int(parts[1])

    return float('inf')

def build_epub(book_metadata_path):
    with open(book_metadata_path, 'r') as f:
        metadata =  json.load(f)
    
    book_title = metadata['title']
    author = metadata.get('author', 'Unknown Author')
    genres = metadata.get('genres', [])
    cover_url = metadata.get('cover_url')
    source_url = metadata.get('source_url')
    downloaded_chapters = metadata.get("downloaded_chapters", {})

    book = epub.EpubBook()
    book.set_title(book_title)
    book.set_language('en')
    book.add_author(author)
    book.add_metadata('DC', 'source', source_url)
    book.add_metadata('DC', 'subject', ', '.join(genres))
    
    if cover_url:
        cover_filename = os.path.basename(cover_url)
        cover_path = os.path.join(os.path.dirname(book_metadata_path), cover_filename)
        
        try:
            if not os.path.exists(cover_path):
                response = requests.get(cover_url)
                with open(cover_path, 'wb') as img:
                    img.write(response.content)
            with open(cover_path, 'rb') as img:
                book.set_cover(cover_filename, img.read())
        except Exception as e:
            print(f"Warning: Could not downlaod or embed cover image. {e}")

    epub_chapters = []
    
    sorted_chapters = sorted(
    downloaded_chapters.items(),
    key=lambda item: extract_chapter_number(item[0], item[1])
)

    for i, (url, chapter) in enumerate(sorted_chapters, start=1):
        if not chapter.get("title") or not chapter.get("content"):
            continue

        paragraphs = chapter["content"].split('\n')
        formatted_content = "".join(f"<p>{p.strip()}</p>" for p in paragraphs if p.strip())

        c = epub.EpubHtml(
            title=chapter["title"],
            file_name=f"chap_{i}.xhtml",
            lang="en"
        )
        c.content = f"<h1>{chapter['title']}</h1>{formatted_content}"
        book.add_item(c)
        epub_chapters.append(c)
    
    book.toc = epub_chapters
    book.spine = ['nav'] + epub_chapters
    book.add_item(epub.EpubNav())
    book.add_item(epub.EpubNcx())

    output_dir = os.path.join("Books", book_title)
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, f"{book_title}.epub")
    epub.write_epub(output_path, book)
    print(f"✅ EPUB saved to: {output_path}")
