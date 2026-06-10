def summarize_result(
    tool: str,
    result,
) -> str:

    if tool == "trace":

        root = list(result.keys())

        return f"""
TOOL: Trace

Root Functions:
{root}
"""

    if tool == "architecture":

        layers = result.get(
            "layers",
            {},
        )

        return f"""
TOOL: Architecture

Layers:
{layers}
"""

    if tool == "security_review":

        return f"""
TOOL: Security Review

Findings:
{result}
"""

    if tool == "explain":

        calls = result.get(
            "calls",
            [],
        )

        return f"""
TOOL: Explain

Function:
{result.get("function")}

Calls:
{calls}
"""

    if tool == "rag":

        return f"""
TOOL: RAG

Answer:
{str(result)[:1000]}
"""

    return f"""
TOOL:
{tool}

RESULT:
{str(result)[:1000]}
"""