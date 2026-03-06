# Original Author: Codec04
# Re-built by Itz-fork
# Project: Gofile2
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
    """

    def __init__(self, token: Optional[str] = None):
        self._async_client = Gofile(token)
        self._loop = asyncio.new_event_loop()

    def _run(self, coro):
        return self._loop.run_until_complete(coro)

    def upload(
        self,
        file: str,
        folderId: Optional[str] = None,
        server: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload a file to Gofile storage.

        Args:
            file: Path to the file to upload.
            folderId: Destination folder ID.
            server: Regional upload server.

        Returns:
            Upload result dict.
        """
        return self._run(self._async_client.upload(file, folderId, server))

    def upload_folder(
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
            folderId: Destination folder ID.
            delay: Time interval between file uploads in seconds.
            server: Regional upload server.

        Returns:
            List of upload results for each file.
        """
        return self._run(
            self._async_client.upload_folder(path, folderId, delay, server)
        )

    def create_folder(
        self,
        parentFolderId: str,
        folderName: Optional[str] = None,
        public: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Create a new folder.

        Args:
            parentFolderId: The parent folder ID.
            folderName: Custom folder name.
            public: Whether the folder should be publicly accessible.

        Returns:
            Folder creation result.
        """
        return self._run(
            self._async_client.create_folder(parentFolderId, folderName, public)
        )

    def update_content(
        self,
        contentId: str,
        attribute: str,
        attributeValue: Any,
    ) -> Dict[str, Any]:
        """
        Update an attribute of a file or folder.

        Args:
            contentId: The content ID.
            attribute: Attribute to update.
            attributeValue: New value for the attribute.

        Returns:
            Update result.
        """
        return self._run(
            self._async_client.update_content(
                contentId, attribute, attributeValue
            )
        )

    def delete_content(self, contentId: str) -> Dict[str, Any]:
        """
        Delete a file or folder.

        Args:
            contentId: The ID of the file or folder to delete.

        Returns:
            Deletion result.
        """
        return self._run(self._async_client.delete_content(contentId))

    def done(self) -> None:
        """Close the HTTP session and event loop."""
        if not self._loop.is_closed():
            self._run(self._async_client.done())
            self._loop.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.done()