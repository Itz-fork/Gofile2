# Original Author: Codec04
# Re-built by Itz-fork
# Project: Gofile2


class InvalidToken(Exception):
    def __init__(self, message=None) -> None:
        super().__init__(
            message
            or "A valid token is required to perform this action"
        )


class ResponseError(Exception):
    def __init__(self, status) -> None:
        super().__init__(
            f"Gofile server responded with: {status} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues",
        )


class RateLimitError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Rate limit exceeded. Try again later"
        )


class InvalidPath(Exception):
    def __init__(self, e) -> None:
        super().__init__(e)


class InvalidOption(Exception):
    def __init__(self, opt) -> None:
        super().__init__(f"{opt} doesn't appear to be a valid option")
