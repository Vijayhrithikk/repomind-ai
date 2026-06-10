def extract_trace_patterns(
    observations,
):

    facts = []

    text = " ".join(
        (
            item["fact"]
            if isinstance(item, dict)
            else str(item)
        )
        for item in observations
    ).lower()

    if (
        "comparehashandpassword" in text
        and "signedstring" in text
    ):

        facts.append(
            "JWT authentication flow detected"
        )

    if (
        "queryrow" in text
        or "scan" in text
    ):

        facts.append(
            "Database lookup detected"
        )

    if (
        "saveurl" in text
        and "geturlbyoriginal" in text
    ):

        facts.append(
            "Repository persistence pattern detected"
        )

    return facts


def extract_architecture_patterns(
    architecture,
):

    facts = []

    layers = architecture.get(
        "layers",
        {},
    )

    handlers = layers.get(
        "handlers",
        [],
    )

    services = layers.get(
        "services",
        [],
    )

    repositories = layers.get(
        "repositories",
        [],
    )

    if (
        handlers
        and services
        and repositories
    ):

        facts.append(
            "Layered architecture detected"
        )

    dependencies = architecture.get(
        "dependencies",
        [],
    )

    if "Redis" in dependencies:

        facts.append(
            "Caching infrastructure detected"
        )

    if "JWT" in dependencies:

        facts.append(
            "JWT authentication detected"
        )

    functions = architecture.get(
        "functions",
        [],
    )

    content = " ".join(
        function.get(
            "content",
            "",
        ).lower()
        for function in functions
    )

    if (
        "getcache" in content
        and "setcache" in content
    ):

        facts.append(
            "Cache-aside pattern detected"
        )

    if (
        "pushanalyticsjob"
        in content
    ):

        facts.append(
            "Asynchronous processing detected"
        )

    if (
        "queryrow" in content
        and "scan" in content
    ):

        facts.append(
            "Repository pattern detected"
        )

    if (
        "redirect(" in content
        or "redirecturl" in content
    ):

        facts.append(
            "HTTP redirect workflow detected"
        )

    return facts