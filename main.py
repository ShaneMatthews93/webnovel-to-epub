from src.batch_scraper import fetch_multi_chapters
from src.epub_builder import build_epub
from src.chapter_table_scraper import table_of_content_extractor
from src.book_manager import book_manager

def main():
    
    
    
    #table_url = 'https://novelbin.com/b/shadow-slave#tab-chapters-title'
    #table_of_content_extractor(table_url)
    
    book_manager()
    
    # Call workers to pull chapters 
    #fetch_multi_chapters("./Books/Shadow Slave/metadata.json")
    
    #build_epub("Shadow Slave", chapters, output_file="shadow slave.epub")
    
if __name__ == "__main__":
    main()