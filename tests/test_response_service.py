import unittest
from services.response_service import ResponseGenerator


class TestResponseGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ResponseGenerator()

    def test_generate_response_fallback_produtivo(self):
        self.generator.ai_client.generate_response = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("fail"))
        text = "O sistema está com erro crítico no pagamento"
        suggestion = self.generator.suggest_response(text, "Produtivo")
        self.assertIn("Obrigado pelo contato", suggestion)

    def test_generate_response_fallback_improdutivo(self):
        self.generator.ai_client.generate_response = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("fail"))
        text = "Obrigado pelo retorno"
        suggestion = self.generator.suggest_response(text, "Improdutivo")
        self.assertIn("Agradecemos a mensagem", suggestion)


if __name__ == "__main__":
    unittest.main()