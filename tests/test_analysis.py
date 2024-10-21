# tests/test_analysis.py

import unittest
from src.analysis import (
    extract_entities,
    extract_pos_tags,
    dependency_parsing,
    keyword_extraction,
    extract_relationships,
    lda_topic_modeling,
    sentiment_analysis,
    analyze_connectors,
    spelling_correction,
    readability_scores,
    extract_dates,
    extract_actions_and_responsibles,
    check_verb_agreement,
    detect_person_changes
)

class TestAnalysis(unittest.TestCase):

    def test_extract_entities_en(self):
        text = "Apple is looking at buying U.K. startup for $1 billion."
        language = 'en'
        expected_entities = [('Apple', 'ORG'), ('U.K.', 'GPE'), ('$1 billion', 'MONEY')]
        entities = extract_entities(text, language)
        self.assertEqual(entities, expected_entities)

    def test_extract_entities_pt(self):
        text = "A empresa Vibracorp está considerando a aquisição da startup brasileira por R$1 bilhão."
        language = 'pt'
        expected_entities = [('Vibracorp', 'ORG'), ('startup brasileira', 'ORG'), ('R$1 bilhão', 'MONEY')]
        entities = extract_entities(text, language)
        self.assertEqual(entities, expected_entities)

    def test_keyword_extraction_en(self):
        text = "Natural language processing enables computers to understand human language."
        language = 'en'
        keywords = keyword_extraction(text, language)
        self.assertTrue(len(keywords) > 0)
        # Verifica se 'language' está nas palavras-chave
        self.assertIn(('language', keywords[0][1]), keywords)

    def test_sentiment_analysis_en(self):
        text = "I love sunny days but hate the rain."
        language = 'en'
        sentiment = sentiment_analysis(text, language)
        self.assertIn(sentiment['label'], ['POSITIVE', 'NEGATIVE'])

    def test_spelling_correction_en(self):
        text = "Ths is a smple English txt."
        language = 'en'
        corrections = spelling_correction(text, language)
        expected_corrections = {
            'ths': ['this', 'thus'],
            'smple': ['sample', 'simple'],
            'txt': ['text']
        }
        for word, suggestions in expected_corrections.items():
            self.assertIn(word, corrections)
            self.assertTrue(len(corrections[word]) > 0)

    def test_readability_scores_en(self):
        text = "This is a simple English text. It has two sentences."
        language = 'en'
        scores = readability_scores(text, language)
        self.assertGreater(scores['flesch_reading_ease'], 0)
        self.assertGreater(scores['flesch_kincaid_grade'], 0)

    def test_analyze_connectors_pt(self):
        text = "Também queria ler um livro. Além disso, planejei exercitar."
        language = 'pt'
        connectives = analyze_connectors(text, language)
        expected_connectives = {'aditivos': 2, 'adversativos': 0, 'conclusivos': 0}
        self.assertEqual(connectives, expected_connectives)

    def test_detect_person_changes_en(self):
        text = "I am going to the store. He is coming with me."
        language = 'en'
        person_changes = detect_person_changes(text, language)
        self.assertTrue(person_changes['inconsistent_person'])

    def test_check_verb_agreement_pt(self):
        text = "Ele vão ao mercado."
        language = 'pt'
        errors = check_verb_agreement(text, language)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(errors[0]['error'], 'Concordância incorreta para sujeito singular.')

if __name__ == '__main__':
    unittest.main()
