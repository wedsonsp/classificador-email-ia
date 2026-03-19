import json
import os
import re

from openai import AzureOpenAI, OpenAI


class AIClient:
    """
    Cliente responsável por conversar com o modelo da OpenAI.

    Espera as variáveis de ambiente:
    - OPENAI_API_KEY: chave da API
    - OPENAI_MODEL (opcional): nome do modelo, padrão gpt-4o-mini
    """

    def __init__(self) -> None:
        # Suporta 2 modos:
        # - OpenAI direto (OPENAI_API_KEY)
        # - Azure OpenAI (AZURE_OPENAI_ENDPOINT / AZURE_OPENAI_API_KEY / AZURE_OPENAI_DEPLOYMENT)
        self.client = None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

        if azure_endpoint and azure_api_key and azure_deployment:
            self.client = AzureOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=azure_api_key,
                api_version=azure_api_version,
            )
            # No Azure, "model" costuma ser o nome do deployment
            self.model = azure_deployment
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = OpenAI(api_key=api_key)

    @staticmethod
    def _parse_json(payload: str) -> dict:
        """
        Tenta extrair um JSON válido de uma resposta que pode vir com texto extra.
        """
        text = (payload or "").strip()
        if not text:
            return {}

        # Primeiro tenta parse direto
        try:
            return json.loads(text)
        except Exception:
            pass

        # Depois tenta extrair a primeira ocorrência de {...}
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return {}

        return {}

    def classify_email(self, text: str):
        """
        Usa o modelo da OpenAI para classificar o e-mail como
        'Produtivo' ou 'Improdutivo' e retorna também a confiança (0–1).
        """
        system_msg = (
            "Você é um classificador de e-mails em português. "
            "Sua tarefa é analisar o texto e decidir se o e-mail é "
            "Produtivo (trata de trabalho, suporte, problema, solicitação) "
            "ou Improdutivo (mensagens de agradecimento, felicitações, "
            "mensagens sociais sem pedido de ação). "
            "Responda APENAS um JSON com os campos: "
            "{\"category\": \"Produtivo|Improdutivo\", \"confidence\": 0.xx}."
        )

        if not self.client:
            raise RuntimeError("OpenAI/Azure OpenAI não configurado (ver variáveis de ambiente).")

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": text},
            ],
            temperature=0.2,
        )

        content = completion.choices[0].message.content or "{}"
        data = self._parse_json(content)

        category = data.get("category", "Produtivo")
        confidence = float(data.get("confidence", 0.7))
        return category, confidence

    def generate_response(self, text: str, category: str, guidance: str) -> str:
        """
        Usa o modelo da OpenAI para sugerir uma resposta curta ao e-mail,
        levando em conta a categoria e uma orientação de estilo (guidance).
        """
        system_msg = (
            "Você é um assistente de atendimento ao cliente em português. "
            "Com base no e-mail abaixo, gere uma resposta educada, clara e "
            "profissional. "
            f"Categoria do e-mail: {category}. "
            f"Orientação: {guidance}. "
            "Responda apenas com o corpo do e-mail (sem saudações como 'Olá' "
            "na primeira linha e sem assinatura)."
        )

        if not self.client:
            raise RuntimeError("OpenAI/Azure OpenAI não configurado (ver variáveis de ambiente).")

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": text},
            ],
            temperature=0.5,
        )

        return completion.choices[0].message.content.strip()
