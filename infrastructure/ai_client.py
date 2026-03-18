import random

class AIClient:
    def classify_email(self, text: str):
        lower = text.lower()
        productive = ["suporte", "erro", "bug", "problema", "ajuda", "ocorreu", "urgente", "prioridade", "revisão", "reclamação"]
        unproductive = ["obrigado", "feliz", "parabéns", "boa sorte", "saudações", "agradecimento"]
        p = sum(1 for k in productive if k in lower)
        u = sum(1 for k in unproductive if k in lower)
        if p >= u and p > 0:
            return "Produtivo", min(0.95, 0.5 + p * 0.08)
        if u > p and u > 0:
            return "Improdutivo", min(0.95, 0.5 + u * 0.08)
        return ("Produtivo", 0.58) if random.random() > 0.4 else ("Improdutivo", 0.52)

    def generate_response(self, text: str, category: str, guidance: str):
        if category == "Produtivo":
            return "Obrigado pelo contato. Identificamos o ponto e vamos priorizar a correção imediatamente."
        return "Agradecemos sua mensagem. Encaminharemos seu feedback ao time responsável e retornaremos quando necessário."
