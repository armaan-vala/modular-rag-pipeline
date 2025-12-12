import unittest
from src.ingestion import TextCleaner

class TestTextCleaner(unittest.TestCase):
    
    def test_normalize_spaces(self):
        raw = "This    has   too\nmany\tspaces."
        expected = "This has too many spaces."
        self.assertEqual(TextCleaner.clean(raw), expected)

    def test_remove_headers(self):
        # Testing the specific logic defined in cleaner
        raw = "Content here. Page 1 of 10 More content."
        # Note: The simple regex replaces it with empty string, double spaces cleaned by first rule
        expected = "Content here. More content." 
        self.assertEqual(TextCleaner.clean(raw), expected)

    def test_empty_string(self):
        self.assertEqual(TextCleaner.clean(""), "")

    def test_special_characters(self):
        raw = "Hello \x00 World" # Null byte
        expected = "Hello  World"
        self.assertEqual(TextCleaner.clean(raw), expected)

if __name__ == '__main__':
    unittest.main()