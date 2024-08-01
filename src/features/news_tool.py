# src/features/news_tool.py

import requests
from langchain.tools import Tool


class NewsTool:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

    def get_news(self, query: str):
        params = {
            'q': query,
            'apiKey': self.api_key,
            'language': 'en',
            'sortBy': 'publishedAt'
        }
        response = requests.get(self.base_url, params=params)
        news = response.json()

        articles = news.get('articles', [])[:5]
        return [{'title': article['title'], 'description': article['description']} for article in articles]

    def get_tool(self):
        return Tool(
            name="NewsSearch",
            func=self.get_news,
            description="Searches for recent news articles on a given topic. Input should be a search query."
        )