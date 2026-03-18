from abc import ABC, abstractmethod

class IEmailClassifier(ABC):
    @abstractmethod
    def classify(self, text: str):
        pass

class IResponseGenerator(ABC):
    @abstractmethod
    def suggest_response(self, text: str, category: str) -> str:
        pass
