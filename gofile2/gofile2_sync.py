# Original Author: Codec04
# Re-built by Itz-fork
# Project: Gofile2
from asyncio import get_event_loop
from typing import Any, Dict, List

from .gofile2 import Gofile


class Sync_Gofile:
    def __init__(self, token=None):
        self.gofile = Gofile(token)
        self.loop = get_event_loop()

    def validate_token(self, token):
        """
        ## Validate Token:

            Validate gofile token

        ### Arguments:

            - `token` - The token to validate
        """
        return self.loop.run_until_complete(self.gofile.validate_token(token))

    def get_server(self) -> str:
        """
        ## Get Server:

            Get the best server available to receive files
        """
        return self.loop.run_until_complete(self.gofile.get_server())

    def get_account(self) -> Dict[str, Any]:
        """
        ## Premium function
            This function can only be executed by gofile premium members

        ### Get Account:

            Get information about the account
        """
        return self.loop.run_until_complete(self.gofile.get_account())

    def get_content(self, contentId) -> Dict[str, Any]:
        """
        ## Premium function
            This function can only be executed by gofile premium members

        ## Get Content:

            Get information about the content

        ### Arguments:

            - `contentId` - The ID of the file or folder
        """
        return self.loop.run_until_complete(self.gofile.get_content(contentId))

    def upload(self, file, folderId) -> Dict[str, Any]:
        """
        ## Upload:

            Upload a file to Gofile server

        ### Arguments:

            - `file` - Path to file that want to be uploaded
            - `folderId` (optional) - The ID of a folder. If you're using the folderId, make sure that you initialize the Gofile class with a token
        """
        return self.loop.run_until_complete(self.gofile.upload(file, folderId))

    def upload_folder(self, path, folderId=None, delay=3) -> List[Dict[str, Any]]:
        """
        ## Upload Folder:

            Upload a folder to Gofile server

        ### Arguments:

            - `path` - Path to folder that you want to be uploaded
            - `folderId` (optional) - The ID of a folder. If you're using the folderId, make sure that you initialize the Gofile class with a token
            - `delay` (optional) - Time interval between file uploads (in seconds)
        """
        return self.loop.run_until_complete(
            self.gofile.upload_folder(path, folderId, delay)
        )

    def create_folder(self, parentFolderId, folderName) -> None:
        """
        ## Premium function
            This function can only be executed by gofile premium members

        ### Create Folder Function:

            Create a new folder

        ### Arguments:

            - `parentFolderId` - The parent folder ID
            - `folderName` - The name of the folder that wanted to create
        """
        return self.loop.run_until_complete(
            self.gofile.create_folder(parentFolderId, folderName)
        )

    def set_option(self, contentId, option, value) -> None:
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
        return self.loop.run_until_complete(
            self.gofile.set_option(contentId, option, value)
        )

    def copy_content(self, contentsId, folderIdDest) -> None:
        """
        ## Premium function
            This function can only be executed by gofile premium members

        ### Copy Content Function:

            Copy one or multiple contents to another folder

        ### Arguments:

            - `contentsId` - The ID(s) of the file or folder (Separate each one by comma if there are multiple IDs)
            - `folderIdDest` - Destinatination folder ID
        """
        return self.loop.run_until_complete(
            self.gofile.copy_content(contentsId, folderIdDest)
        )

    def delete_content(self, contentsId) -> None:
        """
        ## Premium function
            This function can only be executed by gofile premium members

        ### Delete Content Function:

            Delete one or multiple files/folders

        ### Arguments:

            - `contentsId` - The ID(s) of the file or folder (Separate each one by comma if there are multiple IDs)
        """
        return self.loop.run_until_complete(self.gofile.delete_content(contentsId))
