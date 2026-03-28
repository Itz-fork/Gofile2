# Gofile2
```python
from gofile2 import Gofile

async with Gofile() as g:
    await g.upload("/home/partiallywritten/photo.png")
```
***An API Wrapper for Gofile API.***



# About API
> Gofile is in BETA version and this API will evolve over time. Check regularly if changes have been made.
>
Current version is compatible with `2025-05-16`


> [!NOTE]
> **Premium Requirement:** Most API endpoints require a premium account. Only basic operations like uploading, creating folders, renaming content, and removing content are accessible with free accounts.

# Installation
Install via pypi
[![Downloads](https://static.pepy.tech/badge/gofile2)](https://pypi.org/project/gofile2/)
```python
pip3 install gofile2
```

To install development version [Gofile2](https://github.com/partiallywritten/Gofile2), run the following command
```python
pip install git+https://github.com/partiallywritten/Gofile2.git
```

# Usage
**1. Import [Gofile2](https://github.com/partiallywritten/Gofile2) in your python file**

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

The token can be set at initialization or passed per-method call. When both are provided, the per-method token takes priority. You can also initialize without a token and pass it to individual method calls:

```python
# Initialize without a token
g_a = Gofile()

# Pass token per method call
await g_a.create_folder("parent_id", token="your_token")
await g_a.get_content("folder_id", token="another_token")
```

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

    # Get content information
    await g.get_content(contentId="folder_id")

    # Search for content within a folder
    await g.search_content(contentId="folder_id", searchedString="my_file")

    # Copy content to another folder
    await g.copy_content(contentsId="content_id", folderId="destination_folder_id")

    # Move content to another folder
    await g.move_content(contentsId="content_id", folderId="destination_folder_id")

    # Import public content into your account
    await g.import_content(contentsId="content_id")

    # Create a direct link
    await g.create_direct_link(contentId="content_id", expireTime=1735689600)

    # Update a direct link
    await g.update_direct_link(contentId="content_id", directLinkId="link_id", expireTime=1735689600)

    # Delete a direct link
    await g.delete_direct_link(contentId="content_id", directLinkId="link_id")

    # Get account ID
    await g.get_account_id()

    # Get account information
    await g.get_account(accountId="account_id")

    # Reset API token (new token will be sent via email)
    await g.reset_token(accountId="account_id")

    # Any method also accepts a per-call token to override the instance token
    await g.get_content(contentId="folder_id", token="different_token")
```

**Synchronous version with context manager**
```python
with Sync_Gofile(token="your_token") as g:
    g.upload(file="path_to_your_file")
    g.upload_folder(path="path_to_your_folder")
    g.create_folder(parentFolderId="root_folder_id", folderName="My Folder")
    g.update_content(contentId="content_id", attribute="name", attributeValue="new_name.txt")
    g.delete_content(contentId="content_id")
    g.get_content(contentId="folder_id")
    g.search_content(contentId="folder_id", searchedString="my_file")
    g.copy_content(contentsId="content_id", folderId="destination_folder_id")
    g.move_content(contentsId="content_id", folderId="destination_folder_id")
    g.import_content(contentsId="content_id")
    g.create_direct_link(contentId="content_id", expireTime=1735689600)
    g.update_direct_link(contentId="content_id", directLinkId="link_id", expireTime=1735689600)
    g.delete_direct_link(contentId="content_id", directLinkId="link_id")
    g.get_account_id()
    g.get_account(accountId="account_id")
    g.reset_token(accountId="account_id")

    # Any method also accepts a per-call token to override the instance token
    g.get_content(contentId="folder_id", token="different_token")
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

# Multi-Account Usage

All methods accept an optional `token` parameter, allowing you to use multiple accounts with a single client instance. The per-method token overrides the instance token for that specific call:

**Asynchronous version**
```python
async with Gofile() as g:
    # Operate on account A
    await g.create_folder("parent_id", folderName="Folder A", token="token_account_a")
    await g.upload(file="file.txt", folderId="folder_id", token="token_account_a")

    # Operate on account B without reinitializing
    await g.create_folder("parent_id", folderName="Folder B", token="token_account_b")
    await g.get_content(contentId="folder_id", token="token_account_b")
```

**Synchronous version**
```python
with Sync_Gofile() as g:
    # Operate on account A
    g.create_folder("parent_id", folderName="Folder A", token="token_account_a")

    # Operate on account B without reinitializing
    g.get_content(contentId="folder_id", token="token_account_b")
```

# Docs

- `Gofile(token: Optional[str] = None)`
    - Create an async Gofile2 client
    - `token: Optional[str]` - API token for authentication

- `Sync_Gofile(token: Optional[str] = None)`
    - Create a sync Gofile2 client
    - `token: Optional[str]` - API token for authentication

- `upload(file: str, folderId: Optional[str] = None, server: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]`
    - Upload a file to Gofile storage
    - `file: str` - Path to file to upload
    - `folderId: Optional[str]` - Destination folder ID
    - `server: Optional[str]` - Regional upload server
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `upload_folder(path: str, folderId: Optional[str] = None, delay: int = 3, server: Optional[str] = None, token: Optional[str] = None) -> List[Dict[str, Any]]`
    - Upload all files in a folder
    - `path: str` - Path to the folder to upload
    - `folderId: Optional[str]` - Destination folder ID
    - `delay: int` - Time interval between uploads in seconds
    - `server: Optional[str]` - Regional upload server
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `create_folder(parentFolderId: str, folderName: Optional[str] = None, public: Optional[bool] = None, token: Optional[str] = None) -> Dict[str, Any]`
    - Create a new folder
    - `parentFolderId: str` - Parent folder ID
    - `folderName: Optional[str]` - Custom folder name
    - `public: Optional[bool]` - Whether folder is publicly accessible
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `update_content(contentId: str, attribute: str, attributeValue: Any, token: Optional[str] = None) -> Dict[str, Any]`
    - Update an attribute of a file or folder
    - `contentId: str` - Content ID
    - `attribute: str` - Attribute to update (`name`, `description`, `tags`, `public`, `expiry`, `password`)
    - `attributeValue: Any` - New value for the attribute
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `delete_content(contentId: str, token: Optional[str] = None) -> Dict[str, Any]`
    - Delete a file or folder
    - `contentId: str` - Comma-separated list of content IDs to delete
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `get_content(contentId: str, password: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]`
    - Get information about a folder and its contents
    - `contentId: str` - Content ID (must be a folder ID)
    - `password: Optional[str]` - SHA-256 hash of the password for password-protected content
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `search_content(contentId: str, searchedString: str, token: Optional[str] = None) -> Dict[str, Any]`
    - Search for files and folders within a specific parent folder
    - `contentId: str` - Folder ID to search within
    - `searchedString: str` - Search string to match against content names or tags
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `copy_content(contentsId: str, folderId: str, password: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]`
    - Copy files or folders to a destination folder
    - `contentsId: str` - Comma-separated list of content IDs to copy
    - `folderId: str` - Destination folder ID
    - `password: Optional[str]` - SHA-256 hash of the password for password-protected content
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `move_content(contentsId: str, folderId: str, token: Optional[str] = None) -> Dict[str, Any]`
    - Move files or folders to a destination folder
    - `contentsId: str` - Comma-separated list of content IDs to move
    - `folderId: str` - Destination folder ID
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `import_content(contentsId: str, password: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]`
    - Import public content into your account's root folder
    - `contentsId: str` - Comma-separated list of content IDs to import
    - `password: Optional[str]` - SHA-256 hash of the password for password-protected content
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `create_direct_link(contentId: str, expireTime: Optional[int] = None, sourceIpsAllowed: Optional[List[str]] = None, domainsAllowed: Optional[List[str]] = None, domainsBlocked: Optional[List[str]] = None, auth: Optional[List[str]] = None, token: Optional[str] = None) -> Dict[str, Any]`
    - Create a direct access link to content
    - `contentId: str` - Content ID
    - `expireTime: Optional[int]` - Unix timestamp when the link should expire
    - `sourceIpsAllowed: Optional[List[str]]` - List of IP addresses allowed to access the link
    - `domainsAllowed: Optional[List[str]]` - List of domains allowed to access the link
    - `domainsBlocked: Optional[List[str]]` - List of domains blocked from accessing the link
    - `auth: Optional[List[str]]` - List of "user:password" combinations for basic authentication
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `update_direct_link(contentId: str, directLinkId: str, expireTime: Optional[int] = None, sourceIpsAllowed: Optional[List[str]] = None, domainsAllowed: Optional[List[str]] = None, domainsBlocked: Optional[List[str]] = None, auth: Optional[List[str]] = None, token: Optional[str] = None) -> Dict[str, Any]`
    - Update a direct link's configuration
    - `contentId: str` - Content ID
    - `directLinkId: str` - Direct link ID to update
    - `expireTime: Optional[int]` - New Unix timestamp for link expiration
    - `sourceIpsAllowed: Optional[List[str]]` - Updated list of allowed IP addresses
    - `domainsAllowed: Optional[List[str]]` - Updated list of allowed domains
    - `domainsBlocked: Optional[List[str]]` - Updated list of blocked domains
    - `auth: Optional[List[str]]` - Updated list of "user:password" combinations
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `delete_direct_link(contentId: str, directLinkId: str, token: Optional[str] = None) -> Dict[str, Any]`
    - Delete a direct link
    - `contentId: str` - Content ID
    - `directLinkId: str` - Direct link ID to delete
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `get_account_id(token: Optional[str] = None) -> Dict[str, Any]`
    - Get the account ID associated with the current API token
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `get_account(accountId: str, token: Optional[str] = None) -> Dict[str, Any]`
    - Get detailed information about a specific account
    - `accountId: str` - Account ID to retrieve information for
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `reset_token(accountId: str, token: Optional[str] = None) -> Dict[str, Any]`
    - Reset the API token for an account. A new token will be sent via email
    - `accountId: str` - Account ID
    - `token: Optional[str]` - Per-request token (overrides instance token)

- `done() -> None`
    - Close the HTTP session


## Contact
You can find me on;
[Telegram](https://t.me/Bruh_0x), [Bluesky](https://bsky.app/profile/partiallywritten.bsky.social), [Discord](http://discord.com/users/1182562178155413594)
