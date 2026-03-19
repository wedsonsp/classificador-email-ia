import unittest
from services.classification_service import EmailClassifier
from services.nlp_service import NLPService


class DummyNLP:
    def preprocess(self, text):
        return text


class TestEmailClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = EmailClassifier(DummyNLP())

    def test_short_text_returns_improductive(self):
        label, confidence = self.classifier.classify("hi")
        self.assertEqual(label, EmailClassifier.UNPRODUCTIVE)
        self.assertLess(confidence, 0.5)

    def test_ai_client_classification_is_used_when_available(self):
        self.classifier.ai_client.classify_email = lambda text: ("Produtivo", 0.88)
        label, confidence = self.classifier.classify("Temos erro no pagamento e precisamos de correção")
        self.assertEqual(label, "Produtivo")
        self.assertEqual(confidence, 0.88)

    def test_ai_client_failure_falls_back_to_rule_based(self):
        def raise_error(text):
            raise RuntimeError("serviço indisponível")

        self.classifier.ai_client.classify_email = raise_error
        label, confidence = self.classifier.classify("Há um erro crítico no sistema de pagamento")
        self.assertEqual(label, "Produtivo")
        self.assertGreater(confidence, 0.5)

    def test_rule_based_improductive(self):
        self.classifier.ai_client.classify_email = lambda text: (_ for _ in ()).throw(RuntimeError("boom"))
        label, confidence = self.classifier.classify("Obrigado pelo suporte, está ótimo")
        self.assertEqual(label, "Improdutivo")
        self.assertGreater(confidence, 0.5)


if __name__ == "__main__":
    unittest.main()