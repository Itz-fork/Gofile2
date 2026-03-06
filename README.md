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
    - `contentId: str` - Comma-separated list of content IDs to delete

- `get_content(contentId: str, password: Optional[str] = None) -> Dict[str, Any]`
    - Get information about a folder and its contents
    - `contentId: str` - Content ID (must be a folder ID)
    - `password: Optional[str]` - SHA-256 hash of the password for password-protected content

- `search_content(contentId: str, searchedString: str) -> Dict[str, Any]`
    - Search for files and folders within a specific parent folder
    - `contentId: str` - Folder ID to search within
    - `searchedString: str` - Search string to match against content names or tags

- `copy_content(contentsId: str, folderId: str, password: Optional[str] = None) -> Dict[str, Any]`
    - Copy files or folders to a destination folder
    - `contentsId: str` - Comma-separated list of content IDs to copy
    - `folderId: str` - Destination folder ID
    - `password: Optional[str]` - SHA-256 hash of the password for password-protected content

- `move_content(contentsId: str, folderId: str) -> Dict[str, Any]`
    - Move files or folders to a destination folder
    - `contentsId: str` - Comma-separated list of content IDs to move
    - `folderId: str` - Destination folder ID

- `import_content(contentsId: str, password: Optional[str] = None) -> Dict[str, Any]`
    - Import public content into your account's root folder
    - `contentsId: str` - Comma-separated list of content IDs to import
    - `password: Optional[str]` - SHA-256 hash of the password for password-protected content

- `create_direct_link(contentId: str, expireTime: Optional[int] = None, sourceIpsAllowed: Optional[List[str]] = None, domainsAllowed: Optional[List[str]] = None, domainsBlocked: Optional[List[str]] = None, auth: Optional[List[str]] = None) -> Dict[str, Any]`
    - Create a direct access link to content
    - `contentId: str` - Content ID
    - `expireTime: Optional[int]` - Unix timestamp when the link should expire
    - `sourceIpsAllowed: Optional[List[str]]` - List of IP addresses allowed to access the link
    - `domainsAllowed: Optional[List[str]]` - List of domains allowed to access the link
    - `domainsBlocked: Optional[List[str]]` - List of domains blocked from accessing the link
    - `auth: Optional[List[str]]` - List of "user:password" combinations for basic authentication

- `update_direct_link(contentId: str, directLinkId: str, expireTime: Optional[int] = None, sourceIpsAllowed: Optional[List[str]] = None, domainsAllowed: Optional[List[str]] = None, domainsBlocked: Optional[List[str]] = None, auth: Optional[List[str]] = None) -> Dict[str, Any]`
    - Update a direct link's configuration
    - `contentId: str` - Content ID
    - `directLinkId: str` - Direct link ID to update
    - `expireTime: Optional[int]` - New Unix timestamp for link expiration
    - `sourceIpsAllowed: Optional[List[str]]` - Updated list of allowed IP addresses
    - `domainsAllowed: Optional[List[str]]` - Updated list of allowed domains
    - `domainsBlocked: Optional[List[str]]` - Updated list of blocked domains
    - `auth: Optional[List[str]]` - Updated list of "user:password" combinations

- `delete_direct_link(contentId: str, directLinkId: str) -> Dict[str, Any]`
    - Delete a direct link
    - `contentId: str` - Content ID
    - `directLinkId: str` - Direct link ID to delete

- `get_account_id() -> Dict[str, Any]`
    - Get the account ID associated with the current API token

- `get_account(accountId: str) -> Dict[str, Any]`
    - Get detailed information about a specific account
    - `accountId: str` - Account ID to retrieve information for

- `reset_token(accountId: str) -> Dict[str, Any]`
    - Reset the API token for an account. A new token will be sent via email
    - `accountId: str` - Account ID

- `done() -> None`
    - Close the HTTP session


## Contact
You can find me on;
[Telegram](https://t.me/Bruh_0x), [Bluesky](https://bsky.app/profile/hiruu-sh.bsky.social), [Discord](http://discord.com/users/1182562178155413594)
