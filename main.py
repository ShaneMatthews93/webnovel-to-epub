from src.batch_scraper import fetch_multi_chapters
from src.epub_builder import build_epub
from src.chapter_table_scraper import table_of_content_extractor
from src.book_manager import book_manager

def main():
   
    book_manager()
    
if __name__ == "__main__":
    main()