from domain.entities.email_message import EmailMessage

class EmailClassificationService:
    def __init__(self, classifier, responder):
        self.classifier = classifier
        self.responder = responder

    def execute(self, email_message: EmailMessage):
        category, confidence = self.classifier.classify(email_message.text)
        suggestion = self.responder.suggest_response(email_message.text, category)
        return {
            "category": category,
            "confidence": confidence,
            "suggestion": suggestion,
        }
