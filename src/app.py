import streamlit as st
from src.utils.environment_setup import EnvironmentSetup
from src.utils.language_model import LanguageModel
from src.utils.prompt_setup import PromptSetup
from src.features.wikipedia_tool import WikipediaTool
from src.features.math_tool import MathTool
from src.features.web_search_tool import WebSearchTool
from src.utils.evaluation_metrics import EvaluationMetrics
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain.chains import LLMMathChain

from src.features.data_analysis_tool import DataAnalysisTool
from src.features.nlp_tool import NLPTool
from src.features.news_tool import NewsTool
from src.features.fact_check_tool import FactCheckTool

class AgentSetup:
    def __init__(self, llm, tools, prompt):
        self.agent = create_openai_functions_agent(llm, tools, prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=tools, verbose=True)

    def run_agent(self, query):
        return self.executor.invoke({"input": query})

class StreamlitApp:
    def __init__(self):
        st.set_page_config(page_title="AI Agent Interface", page_icon="🤖", layout="wide")
        st.title("AI Agent Interface")

        EnvironmentSetup.load_env()
        openai_api_key = EnvironmentSetup.get_env("OPENAI_API_KEY")
        self.language_model = LanguageModel()
        self.prompt = PromptSetup.get_prompt()

        self.wiki_tool = WikipediaTool().tool
        self.math_tool = MathTool(self.language_model.llm).get_tool()
        self.search_tool = WebSearchTool.get_tool()

        self.data_analysis_tool = DataAnalysisTool().get_tool()
        self.nlp_tool = NLPTool().get_tool()
        self.news_tool = NewsTool(api_key=EnvironmentSetup.get_env("NEWS_API_KEY")).get_tool()
        self.fact_check_tool = FactCheckTool().get_tool()

        self.all_tools = {
            "Wikipedia": self.wiki_tool,
            "MathCalculator": self.math_tool,
            "WebSearch": self.search_tool,
            "DataAnalysis": self.data_analysis_tool,
            "NLPProcessing": self.nlp_tool,
            "NewsSearch": self.news_tool,
            "FactChecking": self.fact_check_tool
        }

        self.evaluation_metrics = EvaluationMetrics()

        self.preloaded_questions = {
            "Euro2024": "Who will win the Euro football cup in 2024?",
            "SquareRoot": "What is the square root of 4?",
            "AIDevelopments": "What are the latest developments in AI?",
            "ClimateChange": "What are the main causes of climate change?",
            "SpaceExploration": "What are the current goals of space exploration?",
            "DataAnalysis": "Analyze this data: 1,2,3,4,5,6,7,8,9,10",
            "SentimentAnalysis": "Analyze the sentiment of this text: I love using this AI agent!",
            "RecentNews": "What are the latest news about renewable energy?",
            "FactCheck": "Is it true that vaccines cause autism?"
        }

    def run(self):
        sidebar_col, main_col = st.columns([1, 3])

        with sidebar_col:
            st.header("Tool Selection")
            selected_tools = st.multiselect(
                "Select tools for the agent to use",
                options=list(self.all_tools.keys()),
                default=list(self.all_tools.keys())
            )

            st.header("Preloaded Questions")
            for question_name, question in self.preloaded_questions.items():
                if st.button(question_name):
                    st.session_state.user_input = question

        with main_col:
            tools = [self.all_tools[tool] for tool in selected_tools]
            agent_setup = AgentSetup(self.language_model.llm, tools, self.prompt)

            user_input = st.text_input("Enter your question:", value=st.session_state.get('user_input', ''))

            if st.button("Ask Agent"):
                if user_input:
                    with st.spinner("Agent is thinking..."):
                        response = agent_setup.run_agent(user_input)
                    st.subheader("Agent's Response:")
                    st.write(response['output'])

                    st.subheader("Response Evaluation")
                    evaluation = self.evaluation_metrics.evaluate(response['output'])

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("Readability:")
                        st.json(evaluation['readability'])

                        st.write("Sentiment:")
                        st.json(evaluation['sentiment'])

                    with col2:
                        st.write(f"Coherence Score: {evaluation['coherence']:.2f}")
                        st.write(f"Informativeness Score: {evaluation['informativeness']:.2f}")

                    reference = st.text_area("Enter a reference answer for comparison (optional):")
                    if reference:
                        comparison_eval = self.evaluation_metrics.evaluate(response['output'], reference)
                        st.write("ROUGE Scores (compared to reference):")
                        st.json(comparison_eval['rouge_scores'])
                        st.write(f"BLEU Score (compared to reference): {comparison_eval['bleu_score']:.2f}")
                else:
                    st.warning("Please enter a question.")

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()