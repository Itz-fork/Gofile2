# Original Author: Codec04
# Re-built by Itz-fork
# Project: Gofile2
import requests


class InvalidToken(Exception):
    pass

class JobFailed(Exception):
    pass

class ResponseError(Exception):
    pass

# Function to check if token is valid or not (using request lib as this is just a sync function)
def is_valid_token(url, token):
    get_account_resp = requests.get(url=f"{url}getAccountDetails?token={token}&allDetails=true").json()
    if get_account_resp["status"] == "error-wrongToken":
        raise InvalidToken("Invalid Gofile Token, Get your Gofile token from --> https://gofile.io/myProfile")
    else:
        pass