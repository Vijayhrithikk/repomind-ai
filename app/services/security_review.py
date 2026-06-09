from app.core.gemini import GeminiClient
from app.services.repository_explorer import (
    RepositoryExplorer,
)


class SecurityReviewService:

    def __init__(self):
        self.gemini = GeminiClient()
        self.explorer = RepositoryExplorer()

    def review(self,target:str="authentication"):

        investigation = self.explorer.investigate(target)

        context = ""

        for function in investigation["functions"]:

            context += f"""
Function:
{function['function_name']}

Code:
{function['content']}

--------------------
"""

        prompt = f"""
You are a senior security engineer.

Review this code.

Look for:

1. Authentication issues
2. JWT issues
3. Password issues
4. Missing rate limiting
5. Input validation problems
6. Authorization problems

Give:

- Finding
- Severity
- Explanation
- Recommendation

Code:

{context}
"""

        return self.gemini.generate(prompt)