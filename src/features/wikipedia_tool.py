from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class WikipediaTool:
    def __init__(self, top_k_results=5, search_query="UEFA_Euro_2024", doc_content_chars_max=1000):
        api_wrapper = WikipediaAPIWrapper(
            top_k_results=top_k_results,
            search_query=search_query,
            doc_content_chars_max=doc_content_chars_max,
        )
        self.tool = WikipediaQueryRun(api_wrapper=api_wrapper)