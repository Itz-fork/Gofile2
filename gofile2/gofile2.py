# Original Author: Codec04
# Re-built by Itz-fork
# Project: Gofile2
import os
from typing import Any, Dict, List

from aiofiles import open as aiopen
from asyncio import sleep as asleep
from aiohttp import ClientSession, FormData

from .errors import InvalidOption, InvalidPath, InvalidToken, ResponseError


class Gofile:
    """
    ## Gofile Class:

        Base class of Asynchronous Gofile2

    ### Arguments:

        - `token` (optional for some functions)- The access token of an account. Can be retrieved from the profile page

    ### Functions:

        - `validate_token` - Validate gofile token
        - `get_server` - Get the best server available to receive files
        - `get_account` - Get information about the account
        - `get_content` - Get information about the content
        - `upload` - Upload a file to Gofile server
        - `upload_folder` - Upload a folder to Gofile server
        - `create_folder` - Create a new folder
        - `set_option` - Set an option on a content
        - `copy_content` - Copy one or multiple contents to another folder
        - `delete_content` - Delete one or multiple files/folders

    ### Notes:

        - Functions marked as "Premium function" can only be executed by gofile premium members
    """

    def __init__(self, token=None):
        self.api_url = "https://api.gofile.io/"
        self.token = token
        self.session = ClientSession()

    @classmethod
    async def initialize(cls, token=None):
        """
        ## Create:

            Create a Gofile2 object

        ### Arguments:

            - `token` (optional for some functions)- The access token of an account. Can be retrieved from the profile page
        """
        gofile_cls = cls(token)
        if token is not None:
            await gofile_cls.validate_token(token)
        return gofile_cls

    async def _api_request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        data: FormData = None,
        need_token: bool = True,
    ) -> Dict[str, Any]:
        """
        ## Request function:

            Make an API request to Gofile server
        """
        # check if token is required
        if need_token and self.token is None:
            raise InvalidToken()

        # prepare data
        url = None
        if endpoint == "uploadFile":
            server = await self.get_server()
            url = f"https://{server}.gofile.io/uploadFile"
        else:
            url = f"{self.api_url}{endpoint}"
        if data and self.token:
            data.add_field("token", self.token)

        # make request
        resp = None
        if method == "GET":
            resp = await self.session.get(url, params=params, data=data)

        elif method == "POST":
             resp = await self.session.post(url, data=data)

        elif method == "PUT":
            resp = await self.session.put(url, data=data)

        elif method == "DELETE":
             resp = await self.session.delete(url, data=data)

        # convert to json
        resp = await resp.json()

        # error handling
        status = resp["status"]
        if status == "ok":
            return resp["data"]
        else:
            if "error-" in resp["status"]:
                error = resp["status"].split("-")[1]
            else:
                error = "Response Status is not ok and the reason is unknown"
            raise ResponseError(error)

    async def validate_token(self, token):
        """
        ## Validate function:

           Validate gofile token

        ### Arguments:

            - `token` - The token to validate
        """
        async with ClientSession() as session:
            async with session.get(
                f"{self.api_url}getAccountDetails?token={token}"
            ) as resp:
                resp = await resp.json()
                if resp["status"] == "error-wrongToken":
                    raise InvalidToken(
                        "Invalid Gofile Token, Get your Gofile token from --> https://gofile.io/myProfile"
                    )

    async def get_server(self) -> str:
        """
        ## Get Server:

            Get the best server available to receive files
        """
        resp = await self._api_request("GET", "getServer", need_token=False)
        return resp["server"]

    async def get_account(self) -> Dict[str, Any]:
        """
        ## Premium function
            This function can only be executed by gofile premium members

        ### Get Account:

            Get information about the account
        """
        return await self._api_request("GET", "getAccountDetails")

    async def get_content(self, contentId) -> Dict[str, Any]:
        """
        ## Premium function
            This function can only be executed by gofile premium members

        ## Get Content:

            Get information about the content

        ### Arguments:

            - `contentId` - The ID of the file or folder
        """
        return await self._api_request(
            "GET", "getContent", params={"contentId": contentId}
        )

    async def upload(self, file: str, folderId: str = None) -> Dict[str, Any]:
        """
        ## Upload:

            Upload a file to Gofile server

        ### Arguments:

            - `file` - Path to file that want to be uploaded
            - `folderId` (optional) - The ID of a folder. If you're using the folderId, make sure that you initialize the Gofile class with a token
        """
        if not os.path.isfile(file):
            raise InvalidPath(f"{file} is not a valid file path")

        data = FormData()
        async with aiopen(file, "rb") as toup:
            data.add_field("file", await toup.read(), filename=file)
        if folderId:
            # without a token, user can't upload multiple files to the same folder
            if not self.token:
                raise InvalidToken()
            data.add_field("folderId", folderId)
        
        return await self._api_request(
            "POST", "uploadFile", data=data, need_token=False
        )

    async def upload_folder(
        self, path: str, folderId: str = None, delay: int = 3
    ) -> List[Dict[str, Any]]:
        """
        ## Upload Folder:

            Upload a folder to Gofile server

        ### Arguments:

            - `path` - Path to folder that you want to be uploaded
            - `folderId` (optional) - The ID of a folder. If you're using the folderId, make sure that you initialize the Gofile class with a token
            - `delay` (optional) - Time interval between file uploads (in seconds)
        """
        if not os.path.isdir(path):
            raise InvalidPath(f"{path} is not a valid directory")

        files = [
            val
            for sublist in [
                [os.path.join(i[0], j) for j in i[2]] for i in os.walk(path)
            ]
            for val in sublist
        ]

        uploaded = []
        # do first request to collect folder id if folderId is None
        if folderId is None:
            file = files.pop(0)
            upres = await self.upload(file)
            folderId = upres["parentFolder"]
            uploaded.append(upres)

        for file in files:
            upres = await self.upload(file, folderId)
            uploaded.append(upres)
            # sleep for x amount of time to avoid potential rate limits / ip bans
            await asleep(delay)

        return uploaded

    async def create_folder(self, parentFolderId: str, folderName: str)  -> None:
        """
        ## Premium function
            This function can only be executed by gofile premium members

        ### Create Folder Function:

            Create a new folder

        ### Arguments:

            - `parentFolderId` - The parent folder ID
            - `folderName` - The name of the folder that wanted to create
        """
        data = FormData()
        data.add_fields(
            ("parentFolderId", parentFolderId),
            ("folderName", folderName),
        )
        return await self._api_request("PUT", "createFolder", data=data)

    async def set_option(self, contentId: str, option: str, value: str)  -> None:
        """
        ## Premium function
            This function can only be executed by gofile premium members

        ### Set Folder Option Function:

            Set an option on a content

        ### Arguments:

            - `contentId` - The content ID
            - `option` - Option that you want to set. Can be "public", "password", "description", "expire" or "tags"
            - `value` - The value of the option to be defined.
                     - For "public", can be "true" or "false".
                     - For "password", must be the password.
                     - For "description", must be the description.
                     - For "expire", must be the expiration date in the form of unix timestamp.
                     - For "tags", must be a comma seperated list of tags.
                     - For "directLink", can be "true" or "false". The contentId must be a file.
        """
        if option not in [
            "public",
            "password",
            "description",
            "expire",
            "tags",
            "directLink",
        ]:
            raise InvalidOption(option)

        data = FormData()
        data.add_fields(
            ("contentId", contentId),
            ("option", option),
            ("value", value),
        )
        return await self._api_request("PUT", "setOption", data=data)

    async def copy_content(self, contentsId: str, folderIdDest: str) -> None:
        """
        ## Premium function
            This function can only be executed by gofile premium members

        ### Copy Content Function:

            Copy one or multiple contents to another folder

        ### Arguments:

            - `contentsId` - The ID(s) of the file or folder (Separate each one by comma if there are multiple IDs)
            - `folderIdDest` - Destinatination folder ID
        """
        data = FormData()
        data.add_fields(
            ("contentsId", contentsId),
            ("folderIdDest", folderIdDest),
        )
        return await self._api_request("PUT", "copyContent", data=data)

    async def delete_content(self, contentsId: str) -> None:
        """
        ## Premium function
            This function can only be executed by gofile premium members

        ### Delete Content Function:

            Delete one or multiple files/folders

        ### Arguments:

            - `contentsId` - The ID(s) of the file or folder (Separate each one by comma if there are multiple IDs)
        """
        data = FormData()
        data.add_field("contentsId", contentsId)
        return await self._api_request("DELETE", "deleteContent", data=data)
    

    async def done(self):
        """
        ## Done function

            Close the session
        """
        await self.session.close()