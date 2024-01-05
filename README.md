# Gofile2
```python
from gofile2 import Gofile

g_a = await Gofile.initialize()
await g_a.upload("/home/itz-fork/photo.png")
await g_a.done()
```
***An API Wrapper for Gofile API.***



# About API
> Gofile is in BETA version and this API will evolve over time. Check regularly if changes have been made.
>
Current version is compatible with `2023-04-20`

# Installation
Install via pypi
[![Downloads](https://static.pepy.tech/badge/gofile2)](https://pypi.org/project/gofile2/)
```python
pip3 install gofile2
```

To install development version [Gofile2](https://github.com/Itz-fork/Gofile2), run the following command
```python
pip install git+https://github.com/Itz-fork/Gofile2.git
```

# Usage
**1. Import [Gofile2](https://github.com/Itz-fork/Gofile2) in your python file**

**Asynchronous version**
```python
from gofile2 import Gofile
```
**Synchronous version**
```python
from gofile2 import Sync_Gofile
```

**2. Create an instance of Gofile2**

**Asynchronous version**
```python
g_a = await Gofile.initialize()
```
**Synchronous version**
```python
g_a = Sync_Gofile()
```
Above code will login as guest account. Keep in mind that only `get_server`, `upload` and `upload_folder` functions works in this mode. If you want to use other functions you will need to have a premium account (as of `2023-04-20`) token. If you need to login to your own account then pass your api token as `token` argument like below code.

```python
g_a = await Gofile.initialize(token="your_gofile_api_token_here")
```

**3. Everything Done! Now Play with it!**
```python
# Get current server
await g_a.get_server()

# Upload a folder
await g_a.upload_folder(path="path_to_your_folder")

# Upload a file
await g_a.upload(file="path_to_your_file")

# Get account info
await g_a.get_account()

# Get content details
await g_a.get_content(contentId="id_of_the_file_or_folder")

# Create folder
await g_a.create_folder(parentFolderId="your_root_folder_id", folderName="Folder Name")

# Set options
await g_a.set_option(contentId="id_of_the_contentr", option="your_option", value="your_value")

# Copy file or folder to another folder
await g_a.copy_content(contentsId="id_of_the_file_or_folder", folderIdDest="id_of_the_destination_folder")

# Delete file or folder
await g_a.delete_content(contentsId="id_of_the_file_or_folder")

# After everything, send close Gofile client
await g_a.done()
```

# Docs
- `initialize (token: Optional[str] = None) -> Gofile`
    - Create a Gofile2 object
    - `token: Optional[str]` - The access token of an account. Can be retrieved from the profile page

- `_api_request (method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[FormData] = None, need_token: bool = True) -> Dict[str, Any]`
    - Make an API request to Gofile server
    - `method: str` - The HTTP method to use for the request
    - `endpoint: str` - The API endpoint to request
    - `params: Optional[Dict[str, Any]]` - The query parameters to include in the request
    - `data: Optional[FormData]` - The form data to include in the request
    - `need_token: bool` - Whether a token is required for the request

- `validate_token (token: str) -> None`
    - Validate gofile token
    - `token: str` - The token to validate

- `get_server () -> str`
    - Get the best server available to receive files

- `get_account () -> Dict[str, Any]`
    - Get information about the account

- `get_content (contentId: str) -> Dict[str, Any]`
    - Get information about the content
    - `contentId: str` - The ID of the file or folder

- `upload (file: str, folderId: str) -> Dict[str, Any]`
    - Upload a file to Gofile server
    - `file: str` - Path to file that want to be uploaded
    - `folderId: str` - The ID of a folder. If you're using the folderId, make sure that you initialize the Gofile class with a token

- `upload_folder (path: str, folderId: Optional[str] = None, delay: int = 3) -> List[Dict[str, Any]]`
    - Upload a folder to Gofile server
    - `path: str` - Path to folder that you want to be uploaded
    - `folderId: Optional[str]` - The ID of a folder. If you're using the folderId, make sure that you initialize the Gofile class with a token
    - `delay: int` - Time interval between file uploads (in seconds)

- `create_folder (parentFolderId: str, folderName: str) -> None`
    - Create a new folder
    - `parentFolderId: str` - The parent folder ID
    - `folderName: str` - The name of the folder that wanted to create

- `set_option (contentId: str, option: str, value: str) -> None`
    - Set an option on a content
    - `contentId: str` - The content ID
    - `option: str` - Option that you want to set. Can be "public", "password", "description", "expire" or "tags"
    - `value: str` - The value of the option to be defined.

- `copy_content (contentsId: str, folderIdDest: str) -> None`
    - Copy one or multiple contents to another folder
    - `contentsId: str` - The ID(s) of the file or folder (Separate each one by comma if there are multiple IDs)
    - `folderIdDest: str` - Destination folder ID

- `delete_content (contentsId: str) -> None`
    - Delete one or multiple files/folders
    - `contentsId: str` - The ID(s) of the file or folder (Separate each one by comma if there are multiple IDs)

- `done () -> None`
    - Close the session

_Automatically generated on 2024:01:05:13:41:40_


## Thanks to
- [gofile](https://github.com/Codec04/gofile) - Base Project & Inspiration ❤️ ([Gofile2](https://github.com/Itz-fork/Gofile2) is a Re-built version of this)
- [Itz-fork](https://github.com/Itz-fork/) (me) - For Fixing & Improving this project