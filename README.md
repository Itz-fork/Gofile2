# Gofile2
```python
from gofile2 import Gofile

async with Gofile() as g:
    await g.upload("/home/itz-fork/photo.png")
```
***An API Wrapper for Gofile API.***



# About API
> Gofile is in BETA version and this API will evolve over time. Check regularly if changes have been made.
>
Current version is compatible with `2025-05-16`

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
g_a = Gofile(token="your_gofile_api_token_here")
```
**Synchronous version**
```python
g_a = Sync_Gofile(token="your_gofile_api_token_here")
```
All API requests require authentication via a bearer token, which is sent automatically in the `Authorization` header. Tokens can be generated from the [profile page](https://gofile.io/myProfile). Guest uploads (without a token) are supported for the `upload` method only.

**3. Everything Done! Now Play with it!**

**Asynchronous version with context manager (recommended)**
```python
async with Gofile(token="your_token") as g:
    # Upload a file
    await g.upload(file="path_to_your_file")

    # Upload a file to a specific folder
    await g.upload(file="path_to_your_file", folderId="folder_id")

    # Upload a file to a specific region
    await g.upload(file="path_to_your_file", server="upload-eu-par")

    # Upload a folder
    await g.upload_folder(path="path_to_your_folder")

    # Create folder
    await g.create_folder(parentFolderId="your_root_folder_id", folderName="Folder Name")

    # Update content attributes (rename, set description, tags, etc.)
    await g.update_content(contentId="id_of_content", attribute="name", attributeValue="new_name.txt")

    # Delete file or folder
    await g.delete_content(contentId="id_of_the_file_or_folder")
```

**Synchronous version with context manager**
```python
with Sync_Gofile(token="your_token") as g:
    g.upload(file="path_to_your_file")
    g.create_folder(parentFolderId="root_folder_id", folderName="My Folder")
    g.update_content(contentId="content_id", attribute="name", attributeValue="new_name.txt")
    g.delete_content(contentId="content_id")
```

**Manual session management**
```python
g_a = Gofile(token="your_token")

await g_a.upload(file="path_to_your_file")

# Close the session when done
await g_a.done()
```

# Regional Upload Servers

By default, uploads go through `upload.gofile.io` which automatically selects the best server. You can also specify a regional server:

| Server | Location |
|--------|----------|
| `upload-eu-par` | Paris |
| `upload-na-phx` | Phoenix |
| `upload-ap-sgp` | Singapore |
| `upload-ap-hkg` | Hong Kong |
| `upload-ap-tyo` | Tokyo |
| `upload-sa-sao` | São Paulo |

```python
await g.upload(file="file.txt", server="upload-eu-par")
```

# Docs

- `Gofile(token: Optional[str] = None)`
    - Create an async Gofile2 client
    - `token: Optional[str]` - API token for authentication

- `Sync_Gofile(token: Optional[str] = None)`
    - Create a sync Gofile2 client
    - `token: Optional[str]` - API token for authentication

- `upload(file: str, folderId: Optional[str] = None, server: Optional[str] = None) -> Dict[str, Any]`
    - Upload a file to Gofile storage
    - `file: str` - Path to file to upload
    - `folderId: Optional[str]` - Destination folder ID
    - `server: Optional[str]` - Regional upload server

- `upload_folder(path: str, folderId: Optional[str] = None, delay: int = 3, server: Optional[str] = None) -> List[Dict[str, Any]]`
    - Upload all files in a folder
    - `path: str` - Path to the folder to upload
    - `folderId: Optional[str]` - Destination folder ID
    - `delay: int` - Time interval between uploads in seconds
    - `server: Optional[str]` - Regional upload server

- `create_folder(parentFolderId: str, folderName: Optional[str] = None, public: Optional[bool] = None) -> Dict[str, Any]`
    - Create a new folder
    - `parentFolderId: str` - Parent folder ID
    - `folderName: Optional[str]` - Custom folder name
    - `public: Optional[bool]` - Whether folder is publicly accessible

- `update_content(contentId: str, attribute: str, attributeValue: Any) -> Dict[str, Any]`
    - Update an attribute of a file or folder
    - `contentId: str` - Content ID
    - `attribute: str` - Attribute to update (`name`, `description`, `tags`, `public`, `expiry`, `password`)
    - `attributeValue: Any` - New value for the attribute

- `delete_content(contentId: str) -> Dict[str, Any]`
    - Delete a file or folder
    - `contentId: str` - Content ID to delete

- `done() -> None`
    - Close the HTTP session


## Thanks to
- [gofile](https://github.com/Codec04/gofile) - Base Project & Inspiration ❤️ ([Gofile2](https://github.com/Itz-fork/Gofile2) is a Re-built version of this)
- [Itz-fork](https://github.com/Itz-fork/) (me) - For Fixing & Improving this project