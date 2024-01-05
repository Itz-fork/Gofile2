# Original Author: Codec04
# Re-built by Itz-fork
# Project: Gofile2


class InvalidToken(Exception):
    def __init__(self) -> None:
        Exception.__init__(
            self,
            "You need to initialize the Gofile class with a token to perform this action"
        )


class ResponseError(Exception):
    def __init__(self, e) -> None:
        Exception.__init__(
            self,
            f"Gofile server responded with: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues",
        )


class InvalidPath(Exception):
    def __init__(self, e) -> None:
        Exception.__init__(self, e)


class InvalidOption(Exception):
    def __init__(self, opt) -> None:
        Exception.__init__(self, f"{opt} doesn't appear to be a valid option")
