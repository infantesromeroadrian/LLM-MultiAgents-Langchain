# src/features/nlp_tool.py
from transformers import pipeline
from langchain.tools import Tool

class NLPTool:
    def __init__(self):
        self.summarizer = pipeline("summarization")
        self.sentiment_analyzer = pipeline("sentiment-analysis")

    def process_text(self, text: str):
        summary = self.summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
        sentiment = self.sentiment_analyzer(text)[0]

        return {
            'summary': summary,
            'sentiment': sentiment
        }

    def get_tool(self):
        return Tool(
            name="NLPProcessing",  # Cambiado de "NLP Processor" a "NLPProcessing"
            func=self.process_text,
            description="Summarizes text and analyzes sentiment."
        )