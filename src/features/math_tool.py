from langchain import LLMMathChain
from langchain.tools import StructuredTool
from src.models.input_models import MathInput
from langchain.chains import LLMMathChain

class MathTool:
    def __init__(self, llm):
        self.llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

    def math_calculator(self, expression: str) -> str:
        return self.llm_math_chain.run(expression)

    def get_tool(self):
        return StructuredTool.from_function(
            func=self.math_calculator,
            name="math_calculator",
            description="A tool that calculates math expressions. The input should be a mathematical expression as a string.",
            args_schema=MathInput,
        )