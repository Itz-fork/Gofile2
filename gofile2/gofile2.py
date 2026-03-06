# Original Author: Codec04
# Re-built by Itz-fork
# Project: Gofile2
import os
from typing import Any, Dict, List, Optional, Union
from asyncio import sleep as asleep

from aiohttp import ClientSession, FormData

from .errors import (
    InvalidOption,
    InvalidPath,
    InvalidToken,
    RateLimitError,
    ResponseError,
)


class Gofile:
    """
    Asynchronous API wrapper for the Gofile REST API.

    Args:
        token: API token for authentication. Can be retrieved from the profile page.
               Required for all operations except guest uploads.

    Supports use as an async context manager:

        async with Gofile(token="...") as g:
            await g.upload("file.txt")
    """

    def __init__(self, token: Optional[str] = None):
        self.api_url = "https://api.gofile.io"
        self.token = token
        self._session: Optional[ClientSession] = None

    async def _get_session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = ClientSession()
        return self._session

    async def _api_request(
        self,
        method: str,
        url: str,
        json: Optional[dict] = None,
        data: Optional[FormData] = None,
        need_token: bool = True,
    ) -> Dict[str, Any]:
        """
        Make an API request to the Gofile server.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            url: Full URL for the request.
            json: JSON body for the request.
            data: Form data for the request (used for file uploads).
            need_token: Whether a token is required for this request.

        Returns:
            The 'data' field from the API response.
        """
        if need_token and self.token is None:
            raise InvalidToken()

        session = await self._get_session()
        headers: Dict[str, str] = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        async with session.request(
            method, url, json=json, data=data, headers=headers
        ) as resp:
            if resp.status == 429:
                raise RateLimitError()
            result = await resp.json(content_type=None)

        status = result.get("status")
        if status == "ok":
            return result.get("data", {})

        raise ResponseError(status or "unknown error")

    async def upload(
        self,
        file: str,
        folderId: Optional[str] = None,
        server: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload a file to Gofile storage.

        Args:
            file: Path to the file to upload.
            folderId: Destination folder ID. If omitted, a new folder is created.
            server: Regional upload server (e.g. 'upload-eu-par' for Paris).
                    Defaults to automatic server selection via 'upload'.

        Returns:
            Upload result containing file info, parentFolder, and (for guest
            uploads) guestToken.
        """
        if not os.path.isfile(file):
            raise InvalidPath(f"{file} is not a valid file path")

        if server:
            url = f"https://{server}.gofile.io/uploadfile"
        else:
            url = "https://upload.gofile.io/uploadfile"

        data = FormData()
        fh = open(file, "rb")
        data.add_field(
            "file", fh, filename=os.path.basename(file)
        )
        if folderId:
            data.add_field("folderId", folderId)

        try:
            return await self._api_request(
                "POST", url, data=data, need_token=False
            )
        finally:
            fh.close()

    async def upload_folder(
        self,
        path: str,
        folderId: Optional[str] = None,
        delay: int = 3,
        server: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Upload all files in a folder to Gofile storage.

        Args:
            path: Path to the folder to upload.
            folderId: Destination folder ID. If omitted, a new folder is created
                      from the first upload's response.
            delay: Time interval between file uploads in seconds (to avoid rate limits).
            server: Regional upload server.

        Returns:
            List of upload results for each file.
        """
        if not os.path.isdir(path):
            raise InvalidPath(f"{path} is not a valid directory")

        files = [
            os.path.join(root, name)
            for root, _, names in os.walk(path)
            for name in names
        ]

        if not files:
            return []

        uploaded: List[Dict[str, Any]] = []
        for i, file_path in enumerate(files):
            result = await self.upload(
                file_path, folderId=folderId, server=server
            )
            uploaded.append(result)
            if folderId is None:
                folderId = result.get("parentFolder")
            if i < len(files) - 1:
                await asleep(delay)

        return uploaded

    async def create_folder(
        self,
        parentFolderId: str,
        folderName: Optional[str] = None,
        public: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Create a new folder.

        Args:
            parentFolderId: The parent folder ID.
            folderName: Custom folder name. If omitted, a unique name is generated.
            public: Whether the folder should be publicly accessible.

        Returns:
            Folder creation result.
        """
        url = f"{self.api_url}/contents/createFolder"
        payload: Dict[str, Union[str, bool]] = {
            "parentFolderId": parentFolderId
        }
        if folderName is not None:
            payload["folderName"] = folderName
        if public is not None:
            payload["public"] = public
        return await self._api_request("POST", url, json=payload)

    async def update_content(
        self,
        contentId: str,
        attribute: str,
        attributeValue: Any,
    ) -> Dict[str, Any]:
        """
        Update an attribute of a file or folder.

        Args:
            contentId: The content ID.
            attribute: Attribute to update. One of: 'name', 'description',
                       'tags', 'public', 'expiry', 'password'.
            attributeValue: New value for the attribute.

        Returns:
            Update result.
        """
        valid_attributes = {
            "name",
            "description",
            "tags",
            "public",
            "expiry",
            "password",
        }
        if attribute not in valid_attributes:
            raise InvalidOption(attribute)

        url = f"{self.api_url}/contents/{contentId}/update"
        payload = {
            "attribute": attribute,
            "attributeValue": attributeValue,
        }
        return await self._api_request("PUT", url, json=payload)

    async def delete_content(self, contentId: str) -> Dict[str, Any]:
        """
        Delete a file or folder.

        Args:
            contentId: The ID of the file or folder to delete.

        Returns:
            Deletion result.
        """
        url = f"{self.api_url}/contents/{contentId}"
        return await self._api_request("DELETE", url)

    async def done(self) -> None:
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.done()