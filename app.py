from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from domain.entities.email_message import EmailMessage
from domain.services.email_classification_service import EmailClassificationService
from services.classification_service import EmailClassifier
from services.response_service import ResponseGenerator
from services.nlp_service import NLPService

app = Flask(__name__)
app.secret_key = "chave-secreta-super"  # em produção, use variável de ambiente

# Serviços de domínio e caso de uso (aplicação)
nlp = NLPService()
classifier = EmailClassifier(nlp)
responder = ResponseGenerator()
email_service = EmailClassificationService(classifier, responder)


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    suggestion = None
    email_text = ""

    if request.method == "POST":
        # Entrada de fallback: arquivo ou texto
        email_text = request.form.get("email_text", "").strip()
        upload = request.files.get("email_file")

        if upload and upload.filename != "":
            filename = upload.filename.lower()
            if filename.endswith(".txt"):
                email_text = upload.stream.read().decode("utf-8", errors="ignore")
            elif filename.endswith(".pdf"):
                try:
                    from PyPDF2 import PdfReader
                    reader = PdfReader(upload.stream)
                    email_text = "\n".join([p.extract_text() or "" for p in reader.pages])
                except Exception:
                    flash("Erro lendo PDF. Envie um arquivo .txt ou insira texto diretamente.", "danger")
                    return redirect(url_for("index"))
            else:
                flash("Formato não suportado. Use .txt ou .pdf", "danger")
                return redirect(url_for("index"))

        if not email_text:
            flash("Por favor, insira o texto do email ou faça upload de arquivo.", "warning")
            return redirect(url_for("index"))

        result = email_service.execute(EmailMessage(email_text))
        suggestion = result["suggestion"]
        prediction = {
            "category": result["category"],
            "score": result["confidence"],
        }

    return render_template(
        "index.html",
        prediction=prediction,
        suggestion=suggestion,
        email_text=email_text,
    )

@app.route("/api/classify", methods=["POST"])
def api_classify():
    data = request.get_json(silent=True)
    if data is None:
        data = request.form

    email_text = (data.get("email_text") or "").strip()
    if not email_text:
        return jsonify({"error": "email_text is required"}), 400

    result = email_service.execute(EmailMessage(email_text))
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)