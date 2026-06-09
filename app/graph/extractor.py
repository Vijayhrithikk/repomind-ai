import re


CALL_PATTERN = re.compile(
    r'([A-Z][A-Za-z0-9_]*)\s*\('
)

IGNORE_CALLS = {
    "New",
    "JSON",
    "Abort",
    "Set",
    "Next",
    "Now",
    "Add",
    "Unix",
}

def extract_calls(
    function_name: str,
    content: str,
):

    matches = CALL_PATTERN.findall(
        content
    )

    calls = []

    for match in matches:

        if match == function_name:
            continue
        if match in IGNORE_CALLS:
            continue

        calls.append(
            (
                function_name,
                match,
            )
        )

    return calls