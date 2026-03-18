from infrastructure.ai_client import AIClient
from services.interfaces import IEmailClassifier

class EmailClassifier(IEmailClassifier):
    PRODUCTIVE = "Produtivo"
    UNPRODUCTIVE = "Improdutivo"

    def __init__(self, nlp_service):
        self.nlp = nlp_service
        self.ai_client = AIClient()

    def _rule_based(self, text: str):
        productive_keywords = ["suporte", "erro", "bug", "atualiza", "ajuda", "problema", "imediato", "prioridade", "detalhes", "solicita", "resposta"]
        unproductive_keywords = ["fica", "obrigado", "parabens", "feliz", "sauda", "ótimo", "agradecimento", "obrigada", "celebra"]
        text_lower = text.lower()

        p = sum(1 for k in productive_keywords if k in text_lower)
        u = sum(1 for k in unproductive_keywords if k in text_lower)

        if p >= u and p > 0:
            return self.PRODUCTIVE, min(0.95, 0.5 + p * 0.08)
        if u > p and u > 0:
            return self.UNPRODUCTIVE, min(0.95, 0.5 + u * 0.08)
        return self.PRODUCTIVE, 0.55

    def classify(self, text: str):
        cleaned = self.nlp.preprocess(text)
        if len(cleaned.strip()) < 10:
            return self.UNPRODUCTIVE, 0.35

        # Tentar classificação com AI se disponível; caso falhe, usar regra simples
        try:
            label, confidence = self.ai_client.classify_email(text)
            return label, confidence
        except Exception:
            return self._rule_based(text)
