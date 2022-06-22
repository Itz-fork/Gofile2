# Original Author: Codec04
# Re-built by Itz-fork
# Project: Gofile2
from requests import get


class InvalidToken(Exception):
    def __init__(self) -> None:
        Exception.__init__(
            self, "Token is required for this action but it's None")


class JobFailed(Exception):
    def __init__(self, e) -> None:
        Exception.__init__(
            self, f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")


class ResponseError(Exception):
    pass


class InvalidPath(Exception):
    pass


class InvalidOption(Exception):
    def __init__(self, opt) -> None:
        Exception.__init__(self, f"{opt} doesn't appear to be a valid option")



# Function to check if token is valid or not (using request lib as this is just a sync function)
def is_valid_token(url, token):
    get_account_resp = get(
        url=f"{url}getAccountDetails?token={token}&allDetails=true").json()
    if get_account_resp["status"] == "error-wrongToken":
        raise InvalidToken(
            "Invalid Gofile Token, Get your Gofile token from --> https://gofile.io/myProfile")
    else:
        pass
