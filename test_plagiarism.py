import unittest
from plagiarism_engine import PlagiarismEngine
from doc_parser import DocumentParser

class TestPlagiarismEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PlagiarismEngine()

    def test_identical_documents(self):
        text = "Artificial intelligence is reshaping software development. Neural networks learn from vast datasets."
        result = self.engine.analyze(text, text)
        self.assertGreaterEqual(result['overall_similarity'], 98.0)
        self.assertEqual(result['risk_classification']['badge'], "High Plagiarism")

    def test_completely_different_documents(self):
        doc1 = "The Parthenon in Athens is a temple of ancient classical Greek architecture."
        doc2 = "Baking fresh sourdough bread requires yeast, flour, water, and salt."
        result = self.engine.analyze(doc1, doc2)
        self.assertLessEqual(result['overall_similarity'], 15.0)

    def test_paraphrased_sentences(self):
        doc1 = "Quantum computing uses qubits to solve complex mathematical problems."
        doc2 = "Quantum hardware leverages qubits to calculate intricate mathematical equations."
        result = self.engine.analyze(doc1, doc2)
        self.assertGreaterEqual(result['overall_similarity'], 40.0)
        
        # Verify sentence match tagging
        doc1_sents = result['sentence_analysis']['doc1_sentences']
        self.assertGreater(len(doc1_sents), 0)
        self.assertIn(doc1_sents[0]['match_type'], ['high', 'exact', 'moderate'])

    def test_top_keywords(self):
        doc1 = "Machine learning algorithms process training data to build neural networks."
        doc2 = "Deep neural networks are machine learning architectures trained on data."
        keywords = self.engine.extract_top_keywords(doc1, doc2)
        self.assertTrue(any(k['term'] in ['machine', 'learning', 'neural', 'networks'] for k in keywords))

    def test_doc_parser_txt(self):
        raw_bytes = b"Hello world! This is a test file for document parsing."
        extracted = DocumentParser.extract_text_from_bytes(raw_bytes, "test.txt")
        self.assertIn("Hello world!", extracted)

if __name__ == '__main__':
    unittest.main()
