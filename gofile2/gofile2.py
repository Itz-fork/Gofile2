# Copyright (c) 2026 Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Gofile2
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

    VALID_SERVERS = {
        "upload",
        "upload-eu-par",
        "upload-na-phx",
        "upload-ap-sgp",
        "upload-ap-hkg",
        "upload-ap-tyo",
        "upload-sa-sao",
    }

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
        params: Optional[dict] = None,
        need_token: bool = True,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Make an API request to the Gofile server.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            url: Full URL for the request.
            json: JSON body for the request.
            data: Form data for the request (used for file uploads).
            params: Query parameters for the request.
            need_token: Whether a token is required for this request.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            The 'data' field from the API response.
        """
        auth_token = token or self.token

        if need_token and auth_token is None:
            raise InvalidToken()

        session = await self._get_session()
        headers: Dict[str, str] = {}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        async with session.request(
            method, url, json=json, data=data, params=params, headers=headers
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
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload a file to Gofile storage.

        Args:
            file: Path to the file to upload.
            folderId: Destination folder ID. If omitted, a new folder is created.
            server: Regional upload server (e.g. 'upload-eu-par' for Paris).
                    Defaults to automatic server selection via 'upload'.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Upload result containing file info, parentFolder, and (for guest
            uploads) guestToken.
        """
        if not os.path.isfile(file):
            raise InvalidPath(f"{file} is not a valid file path")

        if server:
            if server not in self.VALID_SERVERS:
                raise InvalidOption(server)
            url = f"https://{server}.gofile.io/uploadfile"
        else:
            url = "https://upload.gofile.io/uploadfile"

        fh = open(file, "rb")
        try:
            data = FormData()
            data.add_field(
                "file", fh, filename=os.path.basename(file)
            )
            if folderId:
                data.add_field("folderId", folderId)

            return await self._api_request(
                "POST", url, data=data, need_token=False, token=token
            )
        finally:
            fh.close()

    async def upload_folder(
        self,
        path: str,
        folderId: Optional[str] = None,
        delay: int = 3,
        server: Optional[str] = None,
        token: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Upload all files in a folder to Gofile storage.

        Args:
            path: Path to the folder to upload.
            folderId: Destination folder ID. If omitted, a new folder is created
                      from the first upload's response.
            delay: Time interval between file uploads in seconds (to avoid rate limits).
            server: Regional upload server.
            token: Optional per-request token. Overrides the instance token.

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
                file_path, folderId=folderId, server=server, token=token
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
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new folder.

        Args:
            parentFolderId: The parent folder ID.
            folderName: Custom folder name. If omitted, a unique name is generated.
            public: Whether the folder should be publicly accessible.
            token: Optional per-request token. Overrides the instance token.

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
        return await self._api_request("POST", url, json=payload, token=token)

    async def update_content(
        self,
        contentId: str,
        attribute: str,
        attributeValue: Any,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update an attribute of a file or folder.

        Args:
            contentId: The content ID.
            attribute: Attribute to update. One of: 'name', 'description',
                       'tags', 'public', 'expiry', 'password'.
            attributeValue: New value for the attribute.
            token: Optional per-request token. Overrides the instance token.

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
        return await self._api_request("PUT", url, json=payload, token=token)

    async def delete_content(self, contentId: str, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Delete files or folders.

        Args:
            contentId: Comma-separated list of content IDs to delete.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Deletion result.
        """
        url = f"{self.api_url}/contents"
        payload = {"contentsId": contentId}
        return await self._api_request("DELETE", url, json=payload, token=token)

    async def get_content(
        self,
        contentId: str,
        password: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get information about a folder and its contents.

        Args:
            contentId: The content ID (must be a folder ID).
            password: SHA-256 hash of the password for password-protected content.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Content information including metadata and file listings.
        """
        url = f"{self.api_url}/contents/{contentId}"
        params: Optional[Dict[str, str]] = None
        if password is not None:
            params = {"password": password}
        return await self._api_request("GET", url, params=params, token=token)

    async def search_content(
        self,
        contentId: str,
        searchedString: str,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search for files and folders within a specific parent folder.

        Args:
            contentId: The folder ID to search within.
            searchedString: Search string to match against content names or tags.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Search results.
        """
        url = f"{self.api_url}/contents/search"
        params = {"contentId": contentId, "searchedString": searchedString}
        return await self._api_request("GET", url, params=params, token=token)

    async def copy_content(
        self,
        contentsId: str,
        folderId: str,
        password: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Copy files or folders to a destination folder.

        Args:
            contentsId: Comma-separated list of content IDs to copy.
            folderId: Destination folder ID.
            password: SHA-256 hash of the password for password-protected content.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Copy result.
        """
        url = f"{self.api_url}/contents/copy"
        payload: Dict[str, str] = {"contentsId": contentsId, "folderId": folderId}
        if password is not None:
            payload["password"] = password
        return await self._api_request("POST", url, json=payload, token=token)

    async def move_content(
        self,
        contentsId: str,
        folderId: str,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Move files or folders to a destination folder.

        Args:
            contentsId: Comma-separated list of content IDs to move.
            folderId: Destination folder ID.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Move result.
        """
        url = f"{self.api_url}/contents/move"
        payload = {"contentsId": contentsId, "folderId": folderId}
        return await self._api_request("PUT", url, json=payload, token=token)

    async def import_content(
        self,
        contentsId: str,
        password: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Import public content into your account's root folder.

        Args:
            contentsId: Comma-separated list of content IDs to import.
            password: SHA-256 hash of the password for password-protected content.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Import result.
        """
        url = f"{self.api_url}/contents/import"
        payload: Dict[str, str] = {"contentsId": contentsId}
        if password is not None:
            payload["password"] = password
        return await self._api_request("POST", url, json=payload, token=token)

    # --- Direct Links ---

    @staticmethod
    def _build_direct_link_payload(
        expireTime: Optional[int] = None,
        sourceIpsAllowed: Optional[List[str]] = None,
        domainsAllowed: Optional[List[str]] = None,
        domainsBlocked: Optional[List[str]] = None,
        auth: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        if expireTime is not None:
            payload["expireTime"] = expireTime
        if sourceIpsAllowed is not None:
            payload["sourceIpsAllowed"] = sourceIpsAllowed
        if domainsAllowed is not None:
            payload["domainsAllowed"] = domainsAllowed
        if domainsBlocked is not None:
            payload["domainsBlocked"] = domainsBlocked
        if auth is not None:
            payload["auth"] = auth
        return payload

    async def create_direct_link(
        self,
        contentId: str,
        expireTime: Optional[int] = None,
        sourceIpsAllowed: Optional[List[str]] = None,
        domainsAllowed: Optional[List[str]] = None,
        domainsBlocked: Optional[List[str]] = None,
        auth: Optional[List[str]] = None,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a direct access link to content.

        Args:
            contentId: The content ID.
            expireTime: Unix timestamp when the link should expire.
            sourceIpsAllowed: List of IP addresses allowed to access the link.
            domainsAllowed: List of domains allowed to access the link.
            domainsBlocked: List of domains blocked from accessing the link.
            auth: List of "user:password" combinations for basic authentication.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Direct link creation result.
        """
        url = f"{self.api_url}/contents/{contentId}/directlinks"
        payload = self._build_direct_link_payload(
            expireTime, sourceIpsAllowed, domainsAllowed, domainsBlocked, auth
        )
        return await self._api_request("POST", url, json=payload, token=token)

    async def update_direct_link(
        self,
        contentId: str,
        directLinkId: str,
        expireTime: Optional[int] = None,
        sourceIpsAllowed: Optional[List[str]] = None,
        domainsAllowed: Optional[List[str]] = None,
        domainsBlocked: Optional[List[str]] = None,
        auth: Optional[List[str]] = None,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a direct link's configuration.

        Args:
            contentId: The content ID.
            directLinkId: The direct link ID to update.
            expireTime: New Unix timestamp for link expiration.
            sourceIpsAllowed: Updated list of allowed IP addresses.
            domainsAllowed: Updated list of allowed domains.
            domainsBlocked: Updated list of blocked domains.
            auth: Updated list of "user:password" combinations.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Direct link update result.
        """
        url = f"{self.api_url}/contents/{contentId}/directlinks/{directLinkId}"
        payload = self._build_direct_link_payload(
            expireTime, sourceIpsAllowed, domainsAllowed, domainsBlocked, auth
        )
        return await self._api_request("PUT", url, json=payload, token=token)

    async def delete_direct_link(
        self,
        contentId: str,
        directLinkId: str,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Delete a direct link.

        Args:
            contentId: The content ID.
            directLinkId: The direct link ID to delete.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Direct link deletion result.
        """
        url = f"{self.api_url}/contents/{contentId}/directlinks/{directLinkId}"
        return await self._api_request("DELETE", url, token=token)

    # --- Account ---

    async def get_account_id(self, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the account ID associated with the current API token.

        Args:
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Account ID information.
        """
        url = f"{self.api_url}/accounts/getid"
        return await self._api_request("GET", url, token=token)

    async def get_account(self, accountId: str, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detailed information about a specific account.

        Args:
            accountId: The account ID to retrieve information for.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Account information.
        """
        url = f"{self.api_url}/accounts/{accountId}"
        return await self._api_request("GET", url, token=token)

    async def reset_token(self, accountId: str, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Reset the API token for an account. A new token will be sent via email.

        Args:
            accountId: The account ID.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Token reset result.
        """
        url = f"{self.api_url}/accounts/{accountId}/resettoken"
        return await self._api_request("POST", url, token=token)

    async def done(self) -> None:
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.done()