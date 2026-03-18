import re
from nltk.stem import SnowballStemmer

class NLPService:
    def __init__(self):
        self.stemmer = SnowballStemmer("portuguese")
        self.stopwords = {
            "a", "o", "e", "de", "do", "da", "em", "no", "na",
            "para", "por", "com", "um", "uma", "os", "as", "que",
            "que", "se", "é", "não", "dos", "das", "ao", "à",
        }

    def normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-zà-ú0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text: str) -> list[str]:
        normalized = self.normalize(text)
        tokens = normalized.split()
        return [t for t in tokens if t not in self.stopwords and len(t) > 1]

    def stem_tokens(self, tokens: list[str]) -> list[str]:
        return [self.stemmer.stem(t) for t in tokens]

    def preprocess(self, text: str) -> str:
        tokens = self.tokenize(text)
        stems = self.stem_tokens(tokens)
        return " ".join(stems)
