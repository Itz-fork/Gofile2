# Original Author: Codec04
# Re-built by Itz-fork
# Project: Gofile2
import os

from time import time, strftime
from requests import delete, get, post, put
from .errors import (InvalidOption, InvalidPath, InvalidToken, JobFailed,
                     ResponseError, is_valid_token)


class Gofile:
    """
    ## Gofile Class:

        Base class of Asynchronous Gofile2

    ### Arguments:

        - `token` (optional for some functions)- The access token of an account. Can be retrieved from the profile page
    """

    def __init__(self, token=None):
        self.api_url = "https://api.gofile.io/"
        self.token = token
        if self.token is not None:
            is_valid_token(url=self.api_url, token=self.token)

    def _api_resp_handler(self, response):
        api_status = response["status"]
        if api_status == "ok":
            return response["data"]
        else:
            if "error-" in response["status"]:
                error = response["status"].split("-")[1]
            else:
                error = "Response Status is not ok and reason is unknown"
            raise ResponseError(error)

    def get_Server(self):
        """
        ### Get Server Function:
            Get server of Gofile

        ### Arguments:
            `None`
        """
        try:
            server_resp = get(f"{self.api_url}getServer").json()
            return self._api_resp_handler(server_resp)
        except Exception as e:
            raise JobFailed(
                f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    def get_Account(self, check_account=False):
        """
        ### Get Account Function:

            Get information about the account

        ### Arguments:

            - `check_account` (optional) - Boolean. Pass True to check if account exists or not. else it'll return all data of account
        """
        token = self.token
        if token is None:
            raise InvalidToken(
                "Token is required for this action but it's None")
        try:
            get_account_resp = get(
                url=f"{self.api_url}getAccountDetails?token={token}&allDetails=true").json()
            if check_account is True:
                if get_account_resp["status"] == "ok":
                    return True
                elif get_account_resp["status"] == "error-wrongToken":
                    return False
                else:
                    return self._api_resp_handler(get_account_resp)
            else:
                return self._api_resp_handler(get_account_resp)
        except Exception as e:
            raise JobFailed(
                f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    def upload_folder(self, path: str, folderId: str = "", delay: int = 2):
        """
        NOTE: To use this function, you must have a gofile token

        ### Upload folder Function

            Upload files in the given path to Gofile

        ### Arguments

            - `path` - Path to the folder
            - `folderId` (optional) - The ID of a folder. When using the folderId, you must pass the token
            - `delay` - Time interval between file uploads (in seconds)
        """
        if not os.path.isdir(path):
            raise InvalidPath(f"{path} is not a valid directory")
        uploaded = []
        files = [val for sublist in [[os.path.join(
            i[0], j) for j in i[2]] for i in os.walk(path)] for val in sublist]
        # Get folder id if not passed
        if not folderId:
            rtfid = self.get_Account()["rootFolder"]
            folderId = self.create_folder(rtfid, "Gofile2 - Created in {}".format(strftime("%b %d, %Y %l:%M%p")))["id"]
        for file in files:
            udt = self.upload(file, folderId)
            uploaded.append(udt)
            time.sleep(2)
        return uploaded

    def upload(self, file: str, folderId: str = None, description: str = None, password: str = None, tags: str = None, expire: int = None):
        """
        ### Upload Function:

            Upload a file to Gofile

        ### Arguments:

            - `file` - Path to file that want to be uploaded
            - `folderId` (optional) - The ID of a folder. When using the folderId, you must pass the token

            [Deprecated options as of 2022-03-25]
            - `description` (optional) - Description for the uploaded file. Not applicable if you specify a folderId
            - `password` (optional) - Password for the folder. Not applicable if you specify a folderId
            - `tags` (optional) - Tags for the folder. If multiple tags, seperate them with comma. Not applicable if you specify a folderId
            - `expire` (optional) - Expiration date of the folder. Must be in the form of unix timestamp. Not applicable if you specify a folderId
        """
        if not os.path.isfile(file):
            raise InvalidPath(f"No such file - {file}")

        token = self.token if self.token else ""
        if password != None and len(password) < 4:
            raise ValueError("Password Length must be greater than 4")

        try:
            server = self.get_Server()["server"]
            upload_file = post(
                url=f"https://{server}.gofile.io/uploadFile",
                data={
                    "token": token,
                    "folderId": folderId,
                    "description": description,
                    "password": password,
                    "tags": tags,
                    "expire": expire
                },
                files={"upload_file": open(file, "rb")},
                stream=True
            ).json()
            return self._api_resp_handler(upload_file)
        except Exception as e:
            raise JobFailed(
                f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    def create_folder(self, parentFolderId, folderName):
        """
        ### Create Folder Function:

            Create a new folder account

        ### Arguments:

            - `parentFolderId` - The parent folder ID
            - `folderName` - The name of the folder that wanted to create
        """
        token = self.token
        if token is None:
            raise InvalidToken(
                "Token is required for this action but it's None")
        try:
            folder_resp = put(
                url=f"{self.api_url}createFolder",
                data={
                    "parentFolderId": parentFolderId,
                    "folderName": folderName,
                    "token": token
                }
            ).json()
            return self._api_resp_handler(folder_resp)
        except Exception as e:
            raise JobFailed(
                f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    def set_folder_option(self, folderId, option, value):
        """
        ### Set Folder Option Function:

            Set an option on a folder

        ### Arguments:

            - `folderId` - The ID of the folder
            - `option` - Option that you want to set. Can be "public", "password", "description", "expire" or "tags"
            - `value` - The value of the option to be defined.
                     - For "public", can be "true" or "false".
                     - For "password", must be the password.
                     - For "description", must be the description.
                     - For "expire", must be the expiration date in the form of unix timestamp.
                     - For "tags", must be a comma seperated list of tags.
        """
        token = self.token
        if token is None:
            raise InvalidToken()
        if not option in ["public", "password", "description", "expire", "tags"]:
            raise InvalidOption(option)
        try:
            set_folder_resp = put(
                url=f"{self.api_url}setFolderOption",
                data={
                    "token": token,
                    "folderId": folderId,
                    "option": option,
                    "value": value
                }
            ).json()
            return self._api_resp_handler(set_folder_resp)
        except Exception as e:
            raise JobFailed(
                f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    def get_content(self, contentId):
        """
        ### Get Content Function:

            Get a specific content details

        ### Arguments:

            - `contentId` - The ID of the file or folder
        """
        token = self.token
        if token is None:
            raise InvalidToken(
                "Token is required for this action but it's None")
        try:
            get_content_resp = get(
                url=f"{self.api_url}getContent?contentId={contentId}&token={token}").json()
            return self._api_resp_handler(get_content_resp)
        except Exception as e:
            raise JobFailed(
                f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    def copy_content(self, contentsId, folderIdDest):
        """
        ### Copy Content Function:

            Copy one or multiple contents to another folder

        ### Arguments:

            - `contentsId` - The ID(s) of the file or folder (Separate each one by comma if there are multiple IDs)
            - `folderIdDest` - Destinatination folder ID
        """
        token = self.token
        if token is None:
            raise InvalidToken(
                "Token is required for this action but it's None")
        try:
            copy_content_resp = put(
                url=f"{self.api_url}copyContent",
                data={
                    "token": token,
                    "contentsId": contentsId,
                    "folderIdDest": folderIdDest
                }
            ).json()
            return self._api_resp_handler(copy_content_resp)
        except Exception as e:
            raise JobFailed(
                f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    def delete_content(self, contentId):
        """
        ### Delete Content Function:

            Delete a file or folder

        ### Arguments:

            - `contentId` - The ID of the file or folder
        """
        token = self.token
        if token is None:
            raise InvalidToken(
                "Token is required for this action but it's None")
        try:
            del_content_resp = delete(
                url=f"{self.api_url}deleteContent",
                data={
                    "contentId": contentId,
                    "token": token
                }
            ).json()
            return self._api_resp_handler(del_content_resp)
        except Exception as e:
            raise JobFailed(
                f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")
