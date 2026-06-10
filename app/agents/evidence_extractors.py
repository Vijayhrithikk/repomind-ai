def extract_trace_patterns(
    observations
):

    semantic = []

    text = " ".join(observation["fact"] for observation in observations)

    if "CompareHashAndPassword" in text:
        semantic.append(
            "Password verification detected"
        )

    if (
        "NewWithClaims" in text
        and "SignedString" in text
    ):
        semantic.append(
            "JWT generation detected"
        )

    if (
        "QueryRow" in text
        or "Scan" in text
    ):
        semantic.append(
            "Database lookup detected"
        )

    return semantic