# metric_learner.py
import openai
import json
from typing import List, Dict, Any

class MetricLearner:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", max_tokens: int = 30):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        openai.api_key = self.api_key

    def generate_prompt(self, metrics: List[str], **kwargs) -> str:
        prompt = f"""
        Calculate the following RAGA metrics:
        {', '.join(metrics)}

        For each metric, provide:
        1. A brief explanation of how you calculated it
        2. The calculated value (between 0 and 1)

        Use the following information:
        """
        for key, value in kwargs.items():
            prompt += f"{key}: {value}\n"
        
        prompt += "\nRespond in JSON format. Be concise."
        return prompt

    def calculate_metrics(self, metrics: List[str], **kwargs) -> Dict[str, Any]:
        prompt = self.generate_prompt(metrics, **kwargs)
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a precise RAGA metric calculator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                n=1,
                temperature=0.2
            )
            
            result = response.choices[0].message.content.strip()
            return json.loads(result)
        except Exception as e:
            print(f"Error calculating metrics: {e}")
            return {}
