from pydantic import BaseModel, Field

class MathInput(BaseModel):
    expression: str = Field(description="The mathematical expression to calculate")

class WebSearchInput(BaseModel):
    query: str = Field(description="The search query to look up")