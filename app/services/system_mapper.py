class SystemMapper:

    def map_systems(
        self,
        functions,
    ):

        systems = {
            "authentication": [],
            "url_shortening": [],
            "analytics": [],
            "infrastructure": [],
        }

        for function in functions:

            name = (function["function_name"].lower())

            path = (
                function["file_path"]
                .replace("\\", "/")
                .lower()
            )

            if (
                "auth" in name
                or "auth" in path
                or "login" in name
                or "signup" in name
            ):

                systems["authentication"].append(function["function_name"])

            elif (
                "url" in name
                or "short" in name
            ):

                systems[
                    "url_shortening"
                ].append(
                    function["function_name"]
                )

            elif (
                "analytics" in name
            ):

                systems[
                    "analytics"
                ].append(
                    function["function_name"]
                )

            elif (
                "redis" in name
                or "db" in name
                or "config" in name
                or "connect" in name
            ):

                systems["infrastructure"].append(function["function_name"])

        return systems