
from typing import Dict, Any, List
from metric_adapter import (
    NoiseSensitivityAdapter, FaithfulnessAdapter
) #ADD YOUR ADAPTERS HERE
from metric_learner import MetricLearner
import os
from dotenv import load_dotenv

load_dotenv()

class MetricCalculator:
    def __init__(self):
        self.adapters: Dict[str, Any] = {
            "noise_sensitivity": NoiseSensitivityAdapter(),
            "faithfulness": FaithfulnessAdapter(),
            # "answer_relevancy": AnswerRelevancyAdapter(),
            # "context_recall": ContextRecallAdapter(),
            # "context_precision": ContextPrecisionAdapter(),
            # "context_utilization": ContextUtilizationAdapter(),
            # "context_entity_recall": ContextEntityRecallAdapter(),
            # "summarization_score": SummarizationScoreAdapter(),
        }
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
        max_tokens = int(os.getenv("MAX_TOKENS", "100"))
        self.learner = MetricLearner(api_key, model, max_tokens)

    def calculate_metrics(self, metrics: List[str], **kwargs) -> Dict[str, Any]:
        results = {}
        unknown_metrics = []

        for metric in metrics:
            metric_key = metric.lower().replace(" ", "_")
            adapter = self.adapters.get(metric_key)
            if adapter:
                results[metric] = adapter.calculate(**kwargs)
            else:
                unknown_metrics.append(metric)

        if unknown_metrics:
            learned_results = self.learner.calculate_metrics(unknown_metrics, **kwargs)
            results.update(learned_results)

        return results
