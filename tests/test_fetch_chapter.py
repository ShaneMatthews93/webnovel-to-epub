import unittest
from unittest.mock import patch
import src.fetch_chapter 
class TestFetchChapter(unittest.TestCase):
    
    @patch('src.fetch_chapter.fetch_chapter')
    def test_valid_chapter_success(self, mock_fetch):
        mock_fetch.return_value = {
            'title': "Chapter 1: test",
            'content': "<p> testing </p>"
        }
        url = 'https://novelbin.com/b/shadow-slave#tab-chapters-title'
        result = src.fetch_chapter.fetch_chapter(url)
        self.assertIsNotNone(result)
        self.assertIn('title', result)
        self.assertIn('content', result)
        
    @patch('src.fetch_chapter.fetch_chapter')
    def test_invalid_url(self, mock_fetch):
        mock_fetch.return_value = None
        url = 'https://invalid.url'
        result = src.fetch_chapter.fetch_chapter(url)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
