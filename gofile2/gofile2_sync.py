# Copyright (c) 2026 Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Gofile2
import asyncio
from typing import Any, Dict, List, Optional

from .gofile2 import Gofile


class Sync_Gofile:
    """
    Synchronous API wrapper for the Gofile REST API.

    Wraps the async :class:`Gofile` client using an internal event loop.

    Args:
        token: API token for authentication.

    Supports use as a context manager:

        with Sync_Gofile(token="...") as g:
            g.upload("file.txt")

    Note:
        Cannot be used inside a running async event loop
        (e.g. Jupyter notebooks or async frameworks).
        Use :class:`Gofile` directly in those contexts.
    """

    def __init__(self, token: Optional[str] = None):
        try:
            running_loop = asyncio.get_running_loop()
        except RuntimeError:
            running_loop = None

        if running_loop is not None:
            raise RuntimeError(
                "Sync_Gofile cannot be used inside an already running "
                "event loop. Use the async Gofile client instead."
            )

        self._async_client = Gofile(token)
        self._loop = asyncio.new_event_loop()

    def _run(self, coro):
        return self._loop.run_until_complete(coro)

    def upload(
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
            folderId: Destination folder ID.
            server: Regional upload server.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Upload result dict.
        """
        return self._run(self._async_client.upload(file, folderId, server, token=token))

    def upload_folder(
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
            folderId: Destination folder ID.
            delay: Time interval between file uploads in seconds.
            server: Regional upload server.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            List of upload results for each file.
        """
        return self._run(
            self._async_client.upload_folder(path, folderId, delay, server, token=token)
        )

    def create_folder(
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
            folderName: Custom folder name.
            public: Whether the folder should be publicly accessible.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Folder creation result.
        """
        return self._run(
            self._async_client.create_folder(parentFolderId, folderName, public, token=token)
        )

    def update_content(
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
            attribute: Attribute to update.
            attributeValue: New value for the attribute.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Update result.
        """
        return self._run(
            self._async_client.update_content(
                contentId, attribute, attributeValue, token=token
            )
        )

    def delete_content(self, contentId: str, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Delete files or folders.

        Args:
            contentId: Comma-separated list of content IDs to delete.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Deletion result.
        """
        return self._run(self._async_client.delete_content(contentId, token=token))

    def get_content(
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
            Content information.
        """
        return self._run(self._async_client.get_content(contentId, password, token=token))

    def search_content(
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
        return self._run(
            self._async_client.search_content(contentId, searchedString, token=token)
        )

    def copy_content(
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
        return self._run(
            self._async_client.copy_content(contentsId, folderId, password, token=token)
        )

    def move_content(
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
        return self._run(
            self._async_client.move_content(contentsId, folderId, token=token)
        )

    def import_content(
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
        return self._run(self._async_client.import_content(contentsId, password, token=token))

    def create_direct_link(
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
        return self._run(
            self._async_client.create_direct_link(
                contentId, expireTime, sourceIpsAllowed, domainsAllowed,
                domainsBlocked, auth, token=token
            )
        )

    def update_direct_link(
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
        return self._run(
            self._async_client.update_direct_link(
                contentId, directLinkId, expireTime, sourceIpsAllowed,
                domainsAllowed, domainsBlocked, auth, token=token
            )
        )

    def delete_direct_link(
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
        return self._run(
            self._async_client.delete_direct_link(contentId, directLinkId, token=token)
        )

    def get_account_id(self, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the account ID associated with the current API token.

        Args:
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Account ID information.
        """
        return self._run(self._async_client.get_account_id(token=token))

    def get_account(self, accountId: str, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detailed information about a specific account.

        Args:
            accountId: The account ID.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Account information.
        """
        return self._run(self._async_client.get_account(accountId, token=token))

    def reset_token(self, accountId: str, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Reset the API token for an account.

        Args:
            accountId: The account ID.
            token: Optional per-request token. Overrides the instance token.

        Returns:
            Token reset result.
        """
        return self._run(self._async_client.reset_token(accountId, token=token))

    def done(self) -> None:
        """Close the HTTP session and event loop."""
        if not self._loop.is_closed():
            self._run(self._async_client.done())
            self._loop.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.done()