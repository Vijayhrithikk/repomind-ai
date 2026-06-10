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

    services = layers.get(
        "services",
        [],
    )

    repositories = layers.get(
        "repositories",
        [],
    )

    handlers = layers.get(
        "handlers",
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

    deps = architecture.get(
        "dependencies",
        [],
    )

    if "Redis" in deps:

        facts.append(
            "Caching infrastructure detected"
        )

    if "JWT" in deps:

        facts.append("JWT authentication detected")

    flows = architecture.get(
        "flows",
        [],
    )

    flow_text = str(flows).lower()

    if (
        "getcache" in flow_text
        and "setcache" in flow_text
    ):

        facts.append("Cache-aside pattern detected")

    if ("pushanalyticsjob"
        in flow_text
    ):

        facts.append("Asynchronous processing detected")

    return facts