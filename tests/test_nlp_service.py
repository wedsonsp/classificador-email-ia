import unittest
from services.nlp_service import NLPService


class TestNLPService(unittest.TestCase):
    def setUp(self):
        self.nlp = NLPService()

    def test_normalize_removes_special_chars_and_lowercase(self):
        text = "Olá, BOM-dia! 123"
        normalized = self.nlp.normalize(text)
        self.assertEqual(normalized, "olá bom dia 123")

    def test_tokenize_removes_stopwords(self):
        text = "O suporte ao cliente está com problema no sistema"
        tokens = self.nlp.tokenize(text)
        self.assertIn("suporte", tokens)
        self.assertIn("cliente", tokens)
        self.assertNotIn("o", tokens)
        self.assertNotIn("no", tokens)

    def test_preprocess_returns_stemmed_text(self):
        text = "Preciso de ajuda urgente no pagamento"
        proc = self.nlp.preprocess(text)
        self.assertIsInstance(proc, str)
        self.assertIn("prec", proc)
        self.assertIn("ajud", proc)


if __name__ == "__main__":
    unittest.main()