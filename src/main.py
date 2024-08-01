from langchain.agents import create_openai_functions_agent, AgentExecutor
from src.utils.environment_setup import EnvironmentSetup
from src.utils.language_model import LanguageModel
from src.utils.prompt_setup import PromptSetup
from src.features.wikipedia_tool import WikipediaTool
from src.features.math_tool import MathTool
from src.features.web_search_tool import WebSearchTool

class AgentSetup:
    def __init__(self, llm, tools, prompt):
        self.agent = create_openai_functions_agent(llm, tools, prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=tools, verbose=True)

    def run_agent(self, query):
        result = self.executor.invoke({"input": query})
        print(result)

class MainApplication:
    def __init__(self):
        openai_api_key = EnvironmentSetup.load_env()
        language_model = LanguageModel()
        prompt = PromptSetup.get_prompt()

        wiki_tool = WikipediaTool().tool
        math_tool = MathTool(language_model.llm).get_tool()
        search_tool = WebSearchTool.get_tool()

        tools = [wiki_tool, math_tool, search_tool]

        self.agent_setup = AgentSetup(language_model.llm, tools, prompt)

    def run_examples(self):
        print("Ejemplo 1: Predicción de la Eurocopa 2024")
        self.agent_setup.run_agent("Who will win the Euro football cup in 2024?")

        print("\nEjemplo 2: Cálculo matemático")
        self.agent_setup.run_agent("What is the square root of 4?")

        print("\nEjemplo 3: Búsqueda web")
        self.agent_setup.run_agent("What are the latest developments in AI?")

if __name__ == "__main__":
    app = MainApplication()
    app.run_examples()