
from abc import ABC, abstractmethod
from typing import Dict, Any
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class MetricAdapter(ABC):
    @abstractmethod
    def calculate(self, **kwargs) -> Dict[str, Any]:
        pass

class NoiseSensitivityAdapter(MetricAdapter):
    def calculate(self, question: str, ground_truth: str, answer: str, context: str, **kwargs) -> Dict[str, Any]:
        """
        Noise sensitivity measures how often a system makes errors by providing incorrect responses.
        """
        # Tokenize and remove stopwords
        stop_words = set(stopwords.words('english'))
        ground_truth_tokens = [word.lower() for word in word_tokenize(ground_truth) if word.lower() not in stop_words]
        answer_tokens = [word.lower() for word in word_tokenize(answer) if word.lower() not in stop_words]
        context_tokens = [word.lower() for word in word_tokenize(context) if word.lower() not in stop_words]

        # Identify claims from the generated answer
        claims = []
        for token in answer_tokens:
            if token in ground_truth_tokens:
                claims.append(token)

        # Cross-check each claim with the relevant retrieved context
        noise_sensitivity = 0
        for claim in claims:
            if claim in context_tokens:
                noise_sensitivity += 1

        # Calculate noise sensitivity
        noise_sensitivity /= len(claims)
        return {"noise_sensitivity": noise_sensitivity}

class FaithfulnessAdapter(MetricAdapter):
    def calculate(self, answer: str, context: str, **kwargs) -> Dict[str, Any]:
        """
        Faithfulness measures how well the generated answer aligns with the given context.
        """
        # Tokenize and remove stopwords
        stop_words = set(stopwords.words('english'))
        answer_tokens = [word.lower() for word in word_tokenize(answer) if word.lower() not in stop_words]
        context_tokens = [word.lower() for word in word_tokenize(context) if word.lower() not in stop_words]

        # Identify claims from the generated answer
        claims = []
        for token in answer_tokens:
            if token in context_tokens:
                claims.append(token)

        # Cross-check each claim with the given context
        faithfulness = len(claims) / len(answer_tokens)
        return {"faithfulness": faithfulness}


# ... (implement other metric adapters similarly)
