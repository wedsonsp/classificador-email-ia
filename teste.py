from modelo import chamar_modelo

while True:
    prompt = input("Digite sua pergunta (ou 'sair'): ")
    if prompt.lower() == "sair":
        break
    resposta = chamar_modelo(prompt)
    print("Resposta:", resposta)