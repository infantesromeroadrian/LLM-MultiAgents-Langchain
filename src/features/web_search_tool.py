from langchain.tools import DuckDuckGoSearchRun, StructuredTool
from src.models.input_models import WebSearchInput
from langchain_community.tools import DuckDuckGoSearchRun

class WebSearchTool:
    @staticmethod
    def web_search(query: str) -> str:
        return DuckDuckGoSearchRun().run(query)

    @classmethod
    def get_tool(cls):
        return StructuredTool.from_function(
            func=cls.web_search,
            name="web_search",
            description="A tool to search the web using DuckDuckGo",
            args_schema=WebSearchInput,
        )