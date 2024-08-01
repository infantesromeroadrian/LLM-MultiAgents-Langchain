# src/features/fact_check_tool.py

import requests
from langchain.tools import Tool


class FactCheckTool:
    def __init__(self):
        self.base_url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        self.api_key = "YOUR_GOOGLE_FACT_CHECK_API_KEY"  # Replace with actual API key

    def check_fact(self, claim: str):
        params = {
            'query': claim,
            'key': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        results = response.json()

        if 'claims' in results:
            return [{'text': claim['text'], 'claimReview': claim['claimReview'][0]['textualRating']}
                    for claim in results['claims'][:3]]
        else:
            return "No fact check information found."

    def get_tool(self):
        return Tool(
            name="FactChecking",
            func=self.check_fact,
            description="Checks the factual accuracy of a given claim. Input should be a statement to fact-check."
        )