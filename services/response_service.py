from infrastructure.ai_client import AIClient
from services.interfaces import IResponseGenerator

class ResponseGenerator(IResponseGenerator):
    def __init__(self):
        self.ai_client = AIClient()

    def suggest_response(self, email_text: str, category: str) -> str:
        if category == "Produtivo":
            system_tag = "Por favor, responda de forma clara, objetiva e cordial, priorizando ações imediatas."
        else:
            system_tag = "Responda de forma breve e cordial, mostrando agradecimento e sem prometer ações."

        try:
            return self.ai_client.generate_response(email_text, category, system_tag)
        except Exception:
            if category == "Produtivo":
                return "Obrigado pelo contato. Vamos analisar o caso e retornaremos com uma solução detalhada em breve."
            return "Agradecemos a mensagem. Recebemos seu e-mail e estamos à disposição caso precise de algo adicional."
