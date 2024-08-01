from langchain_openai import ChatOpenAI

class LanguageModel:
    def __init__(self, temperature=0.9, model_name="gpt-4"):
        self.llm = ChatOpenAI(temperature=temperature, model_name=model_name)