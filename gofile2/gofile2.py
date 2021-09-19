# Re-built by Itz-fork
# Original Author: Codec04
# Project: Gofile2
import requests

class Gofile:
    """
    Gofile Class:
        Base class of Gofile2
    
    Arguments:
        token (optional for some functions)- The access token of an account. Can be retrieved from the profile page
    """

    def __init__(self, token=None):
        self.api_url = "https://api.gofile.io/"
        self.token = token
    
    def _api_resp_handler(self, response):
        api_status = response["status"]
        if api_status == "ok":
            return response["data"]
        else:
            if "error-" in response["status"]:
                error = response["status"].split("-")[1]
            else:
                error = "RESPONSE ERROR"
            raise Exception(error)

    def get_Server(self):
        """
        Get Server Function:
            Get server of Gofile

        Arguments:
            None
        """
        server_resp = requests.get(f"{self.api_url}getServer").json()
        return self._api_resp_handler(server_resp)
    
    def get_Account(self, check_account=False):
        """
        Get Account Function:
            Get information about the account
        
        Arguments:
            check_account (optional) - Boolean. Pass True to check if account exists or not. else it'll return all data of account
        """
        token = self.token
        if token is None:
            raise Exception("TOKEN IS NOT DEFINED")
        get_account_resp = requests.get(url=f"{self.api_url}getAccountDetails?token={token}&allDetails=true").json()
        if check_account is True:
            if get_account_resp["status"] == "ok":
                return True
            elif get_account_resp["status"] == "error-wrongToken":
                return False
            else:
                return self._api_resp_handler(get_account_resp)
        else:
            return self._api_resp_handler(get_account_resp)
        
    def upload(self,file: str, folderId: str = None, description: str = None, password: str = None, tags: str = None, expire: int = None):
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
        token = self.token
        server = self.get_Server()["server"]
        if password != None and len(password) < 4:
            raise Exception("passwordLength")
        
        upload_file = requests.post(
            url=f"https://{server}.gofile.io/uploadFile",
            data={
                "token": token,
                "folderId": folderId,
                "description": description,
                "password": password,
                "tags": tags,
                "expire": expire
            },
            files={"upload_file": open(file, "rb")}
        ).json()
        return self._api_resp_handler(upload_file)

    def create_folder(self, parentFolderId, folderName):
        """
        Create Folder Function:
            Create a new folder account
        
        Arguments:
            parentFolderId - The parent folder ID
            folderName - The name of the folder that wanted to create
        """
        token = self.token
        folder_resp = requests.put(
            url=f"{self.api_url}createFolder",
            data={
                "parentFolderId": parentFolderId,
                "folderName": folderName,
                "token": token
            }
        ).json()
        return self._api_resp_handler(folder_resp)
    
    def set_folder_options(self, folderId, option, value):
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
        token = self.token
        set_folder_resp = requests.put(
            url=f"{self.api_url}setFolderOptions",
            data={
                "token": token,
                "folderId": folderId,
                "option": option,
                "value": value
            }
        ).json()
        return self._api_resp_handler(set_folder_resp)

    def delete_content(self, contentId):
        """
        Delete Content Function:
            Delete a file or folder
        
        Arguments:
            contentId - The ID of the file or folder
        """
        token = self.token
        del_content_resp = requests.delete(
            url=f"{self.api_url}deleteContent",
            data={
                "contentId": contentId,
                "token": token
            }
        ).json()
        return self._api_resp_handler(del_content_resp)