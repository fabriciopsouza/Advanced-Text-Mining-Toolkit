# tests/test_preprocessing.py

import unittest
from src.preprocessing import preprocess_text, text_statistics, count_syllables_pt

class TestPreprocessing(unittest.TestCase):

    def test_preprocess_text_en(self):
        text = "This is a sample English text."
        language = 'en'
        expected_tokens = ['sample', 'english', 'text']
        tokens = preprocess_text(text, language)
        self.assertEqual(tokens, expected_tokens)

    def test_preprocess_text_pt(self):
        text = "Este é um texto de exemplo em português."
        language = 'pt'
        expected_tokens = ['texto', 'exemplo', 'português']
        tokens = preprocess_text(text, language)
        self.assertEqual(tokens, expected_tokens)

    def test_preprocess_text_empty(self):
        text = ""
        language = 'en'
        expected_tokens = []
        tokens = preprocess_text(text, language)
        self.assertEqual(tokens, expected_tokens)

    def test_text_statistics(self):
        text = "This is a sentence. This is another sentence."
        stats = text_statistics(text)
        self.assertEqual(stats['total_characters'], 45)
        self.assertEqual(stats['total_words'], 8)
        self.assertEqual(stats['total_sentences'], 2)
        self.assertEqual(stats['min_sentences_paragraph'], 2)
        self.assertEqual(stats['max_sentences_paragraph'], 2)
        self.assertEqual(stats['avg_sentences_paragraph'], 2.0)
        self.assertEqual(stats['avg_words_sentence'], 4.0)

    def test_count_syllables_pt(self):
        text = "Este é um texto de exemplo em português."
        syllables = count_syllables_pt(text)
        self.assertEqual(syllables, 16)

if __name__ == '__main__':
    unittest.main()
