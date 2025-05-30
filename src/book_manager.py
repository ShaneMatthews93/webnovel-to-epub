import os
from src.chapter_table_scraper import table_of_content_extractor
from src.batch_scraper import fetch_multi_chapters

def book_manager():
    # Check for directory to store books
    check_book_dir()
    
    program_running = True
    while program_running:
        user_input = input("What would you like to do? --help for options. ")
        if user_input in ('--help', '-h'):
            print("\nUser Commands:"
                  "\n--Update     Check for novel updates"
                  "\n--NewNovel   Add a new novel via its Table of Contents link"
                  "\n--Exit       Exit the program\n")

        elif user_input == '--Update':
            print("Feature not implemented yet: update logic goes here.")
        
        elif user_input == '--NewNovel':
            table_of_contents_url = input("Paste the NovelBin.com URl to the New Novel Table of Contents: ")
            title = table_of_content_extractor(table_of_contents_url)
            fetch_multi_chapters(f"./Books/{title}/metadata.json")
            
        
        elif user_input == '--Exit':
            program_running = False
            print("Exiting book manager. Goodbye!")
        
        else:
            print("Unrecognized command. Type '--help' to see options.")

def check_book_dir():
    if not os.path.exists("Books"):
        os.makedirs("Books")