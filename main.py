from src.batch_scraper import fetch_multi_chapters
from src.epub_builder import build_epub
from src.chapter_table_scraper import table_of_content_extractor
from src.book_manager import book_manager
from src.ollama_fetch_chapter import fetch_chapter #delete after testing AI

def main():
   
    #book_manager()
    url = 'https://novelbin.com/b/library-of-heavens-path/chapter-1'
    fetch_chapter(url)
    
if __name__ == "__main__":
    main()