from langchain import hub

class PromptSetup:
    @staticmethod
    def get_prompt():
        return hub.pull("hwchase17/openai-functions-agent")