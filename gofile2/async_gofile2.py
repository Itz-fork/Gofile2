# Original Author: Codec04
# Re-built by Itz-fork
# Project: Gofile2
import os
import aiohttp

from .errors import is_valid_token, InvalidToken, JobFailed, ResponseError, InvalidPath


class Async_Gofile:
    """
    ## Gofile Class:

        Base class of Asynchronous Gofile2

    ### Arguments:

        - `token` (optional for some functions)- The access token of an account. Can be retrieved from the profile page
    """

    def __init__(self, token=None):
        self.api_url = "https://api.gofile.io/"
        self.r_session = aiohttp.ClientSession()
        self.token = token
        if self.token is not None:
            is_valid_token(url=self.api_url, token=self.token)

    async def _api_resp_handler(self, response):
        api_status = response["status"]
        if api_status == "ok":
            return response["data"]
        else:
            if "error-" in response["status"]:
                error = response["status"].split("-")[1]
            else:
                error = "Response Status is not ok and reason is unknown"
            raise ResponseError(error)

    async def get_Server(self, pre_session=None):
        """
        ### Get Server Function:
            Get server of Gofile

        ### Arguments:
            `None`
        """
        if pre_session:
            server_resp = await pre_session.get(f"{self.api_url}getServer")
            server_resp = await server_resp.json()
            return await self._api_resp_handler(server_resp)
        else:
            async with self.r_session as session:
                try:
                    server_resp = await session.get(f"{self.api_url}getServer")
                    server_resp = await server_resp.json()
                    return await self._api_resp_handler(server_resp)
                except Exception as e:
                    raise JobFailed(
                        f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    async def get_Account(self, check_account=False):
        """
        ### Get Account Function:

            Get information about the account

        ### Arguments:

            - `check_account` (optional) - Boolean. Pass True to check if account exists or not. else it'll return all data of account
        """
        if self.token is None:
            raise InvalidToken(
                "Token is required for this action but it's None")
        async with self.r_session as session:
            try:
                get_account_resp = await session.get(url=f"{self.api_url}getAccountDetails?token={self.token}&allDetails=true")
                get_account_resp = await get_account_resp.json()
                if check_account is True:
                    if get_account_resp["status"] == "ok":
                        return True
                    elif get_account_resp["status"] == "error-wrongToken":
                        return False
                    else:
                        return await self._api_resp_handler(get_account_resp)
                else:
                    return await self._api_resp_handler(get_account_resp)
            except Exception as e:
                raise JobFailed(
                    f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    async def upload(self, file: str, folderId: str = "", description: str = "", password: str = "", tags: str = "", expire: str = ""):
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
        async with self.r_session as session:
            # Check time
            if not os.path.isfile(file):
                raise InvalidPath(f"No such file - {file}")
            if password and len(password) < 4:
                raise ValueError("Password Length must be greater than 4")

            server = await self.get_Server(pre_session=session)
            server = server["server"]
            token = self.token if self.token else ""

            # Making dict
            req_dict = {}
            if token:
                req_dict["token"] = token
            if folderId:
                req_dict["folderId"] = folderId
            if description:
                req_dict["description"] = description
            if password:
                req_dict["password"] = password
            if tags:
                req_dict["tags"] = tags
            if expire:
                req_dict["expire"] = expire

            with open(file, "rb") as go_file_d:
                req_dict["file"] = go_file_d
                try:
                    upload_file = await session.post(
                        url=f"https://{server}.gofile.io/uploadFile",
                        data=req_dict
                    )
                    upload_file = await upload_file.json()
                    return await self._api_resp_handler(upload_file)
                except Exception as e:
                    raise JobFailed(
                        f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    async def create_folder(self, parentFolderId, folderName):
        """
        ### Create Folder Function:

            Create a new folder account

        ### Arguments:

            - `parentFolderId` - The parent folder ID
            - `folderName` - The name of the folder that wanted to create
        """
        if self.token is None:
            raise InvalidToken(
                "Token is required for this action but it's None")
        async with self.r_session as session:
            try:
                folder_resp = await session.put(
                    url=f"{self.api_url}createFolder",
                    data={
                        "parentFolderId": parentFolderId,
                        "folderName": folderName,
                        "token": self.token
                    }
                )
                folder_resp = await folder_resp.json()
                return await self._api_resp_handler(folder_resp)
            except Exception as e:
                raise JobFailed(
                    f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    async def set_folder_options(self, folderId, option, value):
        """
        ### Set Folder Options Function:

            Set an option on a folder

        ### Arguments:

            - `folderId` - The ID of the folder
            - `option` - Option that you want to set. Can be "private", "password", "description", "expire" or "tags"
            - `value` - The value of the option to be defined.
                     - For "private", can be "true" or "false".
                     - For "password", must be the password.
                     - For "description", must be the description.
                     - For "expire", must be the expiration date in the form of unix timestamp.
                     - For "tags", must be a comma seperated list of tags.
        """
        if self.token is None:
            raise InvalidToken(
                "Token is required for this action but it's None")
        async with self.r_session as session:
            try:
                set_folder_resp = await session.put(
                    url=f"{self.api_url}setFolderOptions",
                    data={
                        "token": self.token,
                        "folderId": folderId,
                        "option": option,
                        "value": value
                    }
                )
                set_folder_resp = await set_folder_resp.json()
                return await self._api_resp_handler(set_folder_resp)
            except Exception as e:
                raise JobFailed(
                    f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    async def get_content(self, contentId):
        """
        ### Get Content Function:

            Get a specific content details

        ### Arguments:

            - `contentId` - The ID of the file or folder
        """
        if self.token is None:
            raise InvalidToken(
                "Token is required for this action but it's None")
        async with self.r_session as session:
            try:
                get_content_resp = await session.get(url=f"{self.api_url}getContent?contentId={contentId}&token={self.token}")
                get_content_resp = await get_content_resp.json()
                return await self._api_resp_handler(get_content_resp)
            except Exception as e:
                raise JobFailed(
                    f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    async def copy_content(self, contentsId, folderIdDest):
        """
        ### Copy Content Function:

            Copy one or multiple contents to another folder

        ### Arguments:

            - `contentsId` - The ID(s) of the file or folder (Separate each one by comma if there are multiple IDs)
            - `folderIdDest` - Destinatination folder ID
        """
        if self.token is None:
            raise InvalidToken(
                "Token is required for this action but it's None")
        async with self.r_session as session:
            try:
                copy_content_resp = await session.put(
                    url=f"{self.api_url}copyContent",
                    data={
                        "token": self.token,
                        "contentsId": contentsId,
                        "folderIdDest": folderIdDest
                    }
                )
                copy_content_resp = await copy_content_resp.json()
                return await self._api_resp_handler(copy_content_resp)
            except Exception as e:
                raise JobFailed(
                    f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")

    async def delete_content(self, contentId):
        """
        ### Delete Content Function:

            Delete a file or folder

        ### Arguments:

            - `contentId` - The ID of the file or folder
        """
        if self.token is None:
            raise InvalidToken(
                "Token is required for this action but it's None")
        async with self.r_session as session:
            try:
                del_content_resp = await session.delete(
                    url=f"{self.api_url}deleteContent",
                    data={
                        "contentId": contentId,
                        "token": self.token
                    }
                )
                del_content_resp = await del_content_resp.json()
                return await self._api_resp_handler(del_content_resp)
            except Exception as e:
                raise JobFailed(
                    f"Error Happend: {e} \n\nReport this at ----> https://github.com/Itz-fork/Gofile2/issues")
