# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from metric_calc import MetricCalculator

app = FastAPI()
calculator = MetricCalculator()

class MetricRequest(BaseModel):
    metrics: List[str]
    ground_truth: str
    answer: str
    question: str
    context: str

@app.post("/calculate_metrics")
async def calculate_metrics(request: MetricRequest):
    try:
        results = calculator.calculate_metrics(
            request.metrics,
            ground_truth=request.ground_truth,
            answer=request.answer,
            question=request.question,
            context=request.context
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
