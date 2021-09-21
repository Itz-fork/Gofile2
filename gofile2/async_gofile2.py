# Original Author: Codec04
# Re-built by Itz-fork
# Project: Gofile2
import aiohttp
from .errors import is_valid_token, InvalidToken,JobFailed, ResponseError


class Async_Gofile:
    """
    Gofile Class:
        Base class of Asynchronous Gofile2
    
    Arguments:
        token (optional for some functions)- The access token of an account. Can be retrieved from the profile page
    """

    def __init__(self, token=None):
        self.api_url = "https://api.gofile.io/"
        self.r_session = aiohttp.ClientSession()
        self.token = token
        if self.token is not None:
            is_valid_token(url=self.api_url, token=self.token)

    async def __close_session(self, session):
        await session.close()

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

    async def get_Server(self):
        """
        Get Server Function:
            Get server of Gofile

        Arguments:
            None
        """
        async with self.r_session as session:
            try:
                server_resp = await session.get(f"{self.api_url}getServer")
                server_resp = await server_resp.json()
                await self.__close_session(session)
                return await self._api_resp_handler(server_resp)
            except Exception as e:
                await self.__close_session(session)
                raise JobFailed(f"Cannot Continue due to: {e}")
    
    async def get_Account(self, check_account=False):
        """
        Get Account Function:
            Get information about the account
        
        Arguments:
            check_account (optional) - Boolean. Pass True to check if account exists or not. else it'll return all data of account
        """
        if self.token is None:
            raise InvalidToken("Token is required for this action but it's None")
        async with self.r_session as session:
            try:
                get_account_resp = await session.get(url=f"{self.api_url}getAccountDetails?token={self.token}&allDetails=true")
                get_account_resp = await get_account_resp.json()
                await self.__close_session(session)
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
                await self.__close_session(session)
                raise JobFailed(f"Cannot Continue due to: {e}")
        
    async def upload(self,file: str, folderId: str = None, description: str = None, password: str = None, tags: str = None, expire: int = None):
        """
        Upload Function:
            Upload a file to Gofile
        
        Arguments:
            file - Path to file that want to be uploaded
            folderId (optional) - The ID of a folder. When using the folderId, you must pass the token
            description (optional) - Description for the uploaded file. Not applicable if you specify a folderId
            password (optional) - Password for the folder. Not applicable if you specify a folderId
            tags (optional) - Tags for the folder. If multiple tags, seperate them with comma. Not applicable if you specify a folderId
            expire (optional) - Expiration date of the folder. Must be in the form of unix timestamp. Not applicable if you specify a folderId
        """
        server = self.get_Server()["server"]
        if password != None and len(password) < 4:
            raise ValueError("Password Length must be greater than 4")
        
        async with self.r_session as session:
            try:
                upload_file = await session.post(
                    url=f"https://{server}.gofile.io/uploadFile",
                    data={
                        "token": self.token,
                        "folderId": folderId,
                        "description": description,
                        "password": password,
                        "tags": tags,
                        "expire": expire
                    },
                    files={"upload_file": open(file, "rb")}
                )
                upload_file = await upload_file.json()
                await self.__close_session(session)
                return await self._api_resp_handler(upload_file)
            except Exception as e:
                await self.__close_session(session)
                raise JobFailed(f"Cannot Continue due to: {e}")

    async def create_folder(self, parentFolderId, folderName):
        """
        Create Folder Function:
            Create a new folder account
        
        Arguments:
            parentFolderId - The parent folder ID
            folderName - The name of the folder that wanted to create
        """
        if self.token is None:
            raise InvalidToken("Token is required for this action but it's None")
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
                await self.__close_session(session)
                return await self._api_resp_handler(folder_resp)
            except Exception as e:
                await self.__close_session(session)
                raise JobFailed(f"Cannot Continue due to: {e}")
    
    async def set_folder_options(self, folderId, option, value):
        """
        Set Folder Options Function:
            Set an option on a folder
        
        Arguments:
            folderId - The ID of the folder
            option - Option that you want to set. Can be "private", "password", "description", "expire" or "tags"
            value - The value of the option to be defined.
                     For "private", can be "true" or "false".
                     For "password", must be the password.
                     For "description", must be the description.
                     For "expire", must be the expiration date in the form of unix timestamp.
                     For "tags", must be a comma seperated list of tags.
        """
        if self.token is None:
            raise InvalidToken("Token is required for this action but it's None")
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
                await self.__close_session(session)
                return await self._api_resp_handler(set_folder_resp)
            except Exception as e:
                await self.__close_session(session)
                raise JobFailed(f"Cannot Continue due to: {e}")

    async def delete_content(self, contentId):
        """
        Delete Content Function:
            Delete a file or folder
        
        Arguments:
            contentId - The ID of the file or folder
        """
        if self.token is None:
            raise InvalidToken("Token is required for this action but it's None")
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
                await self.__close_session(session)
                return await self._api_resp_handler(del_content_resp)
            except Exception as e:
                await self.__close_session(session)
                raise JobFailed(f"Cannot Continue due to: {e}")