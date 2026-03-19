import os
from openai import AzureOpenAI

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-mini")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-07-01-preview")

if not endpoint or not api_key:
    raise RuntimeError("Configure AZURE_OPENAI_ENDPOINT e AZURE_OPENAI_API_KEY no ambiente")

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint,
)


def chamar_modelo(prompt: str) -> str:
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
