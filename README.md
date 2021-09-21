# Gofile2
```python
from gofile2 import Gofile

g_a = Gofile()
print(g_a.upload(file="/home/itz-fork/photo.png"))
```
***An API Wrapper for Gofile API.***

# About API
> Gofile is in BETA version and this API will evolve over time. Check regularly if changes have been made.
>
Current version is compatible with `2021-06-22`

# Installation
Install via pypi
```python
pip3 install gofile2
```

To install development version [Gofile2](https://github.com/Itz-fork/Gofile2), run the following command
```python
pip install git+https://github.com/Itz-fork/Gofile2.git
```

# Usage
**1. Import [Gofile2](https://github.com/Itz-fork/Gofile2) in your python file**

**Synchronous version**
```python
from gofile2 import Gofile
```
**Asynchronous version**
```python
from gofile2 import Async_Gofile
```

**2. Create an instance of Gofile2**

**Synchronous version**
```python
g_a = Gofile()
```
**Asynchronous version**
```python
g_a = Async_Gofile()
```
Above code will login as guest account (Some functions won't work in this mode). If you need to login to your own account then pass your api token as `token` argument like below code.

**Synchronous version**
```python
g_a = Gofile(token="your_gofile_api_token_here")
```
**Asynchronous version**
```python
g_a = Async_Gofile(token="your_gofile_api_token_here")
```

**3. Everything Done! Now Play with it!**
```python
# Get current server
g_a.get_Server()

# Get account info
g_a.get_Account()

# Upload a file
g_a.upload(file="path_to_your_file")

# Create folder
g_a.create_folder(parentFolderId="your_root_folder_id", folderName="Folder Name")

# Set folder options
g_a.set_folder_options(folderId="id_of_the_folder", option="your_option", value="your_value")

# Delete file or folder
g_a.delete_content(contentId="id_of_the_file_or_folder")
```

# Docs
For now there is no documentation for [Gofile2](https://github.com/Itz-fork/Gofile2). However you can get some help from Docstrings using,
```python
from gofile2 import Gofile

# Replace upload with the function you want
print(help(Gofile().upload))
```

## Thanks to
- [gofile](https://github.com/Codec04/gofile) - Base Project & Inspiration ❤️ ([Gofile2](https://github.com/Itz-fork/Gofile2) is a Re-built version of this)
- [Itz-fork](https://github.com/Itz-fork/) (me) - For Fixing & Improving this project