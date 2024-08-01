# src/features/data_analysis_tool.py

import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class DataAnalysisInput(BaseModel):
    data: List[str] = Field(..., description="List of numbers to analyze")
    config: Dict[str, Any] = Field(default_factory=dict, description="Configuration for the analysis")

class DataAnalysisTool:
    def analyze_data(self, input_data: DataAnalysisInput):
        data = ','.join(input_data.data)
        df = pd.read_csv(BytesIO(data.encode()), header=None)

        summary = df.describe().to_string()

        plt.figure(figsize=(10, 6))
        df.plot(kind='bar')
        plt.title('Data Visualization')

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return {
            'summary': summary,
            'plot': plot_url
        }

    def get_tool(self):
        return StructuredTool.from_function(
            func=self.analyze_data,
            name="DataAnalysis",
            description="Analyzes numerical data and creates visualizations. Input should be a list of numbers.",
            args_schema=DataAnalysisInput
        )