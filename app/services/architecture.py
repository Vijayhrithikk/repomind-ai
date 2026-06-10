from app.core.gemini import GeminiClient
from app.services.repository_explorer import (
    RepositoryExplorer,
)


class ArchitectureService:

    def __init__(self):

        self.gemini = GeminiClient()
        self.explorer = RepositoryExplorer()

    def review(
        self,
        topic: str,
    ):

        investigation = (self.explorer.investigate(topic))

        context = ""

        for function in investigation["functions"]:

            context += f"""
Function:
{function['function_name']}

File:
{function['file_path']}

Code:
{function['content']}

--------------------
"""

        prompt = f"""
You are a senior software architect.

Analyze this repository area.

Topic:
{topic}

Relationships:
{investigation['relationships']}

Code:

{context}

Explain:

1. Components involved
2. Request flow
3. Data flow
4. Dependencies
5. Architectural strengths
6. Architectural weaknesses
7. Scaling concerns

Be specific to the code.
"""

        architecture = (self.gemini.generate(prompt))

        return {
            "topic": topic,
            "architecture": architecture,
            "relationships": investigation[
                "relationships"
            ],
        }