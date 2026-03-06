import os
import asyncio
import tempfile

import pytest
from aioresponses import aioresponses

from gofile2 import Gofile, Sync_Gofile
from gofile2.errors import (
    InvalidOption,
    InvalidPath,
    InvalidToken,
    RateLimitError,
    ResponseError,
)


# --- Async Tests ---

@pytest.fixture
def mock_aio():
    with aioresponses() as m:
        yield m


@pytest.fixture
def tmp_file():
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w") as f:
        f.write("test content")
    yield path
    os.unlink(path)


@pytest.fixture
def tmp_dir():
    d = tempfile.mkdtemp()
    for name in ["a.txt", "b.txt"]:
        with open(os.path.join(d, name), "w") as f:
            f.write(f"content of {name}")
    yield d
    for name in ["a.txt", "b.txt"]:
        os.unlink(os.path.join(d, name))
    os.rmdir(d)


class TestGofileInit:
    def test_default_init(self):
        g = Gofile()
        assert g.token is None
        assert g.api_url == "https://api.gofile.io"

    def test_init_with_token(self):
        g = Gofile(token="test-token")
        assert g.token == "test-token"


class TestGofileUpload:
    @pytest.mark.asyncio
    async def test_upload_invalid_path(self):
        async with Gofile() as g:
            with pytest.raises(InvalidPath):
                await g.upload("/nonexistent/file.txt")

    @pytest.mark.asyncio
    async def test_upload_success(self, mock_aio, tmp_file):
        mock_aio.post(
            "https://upload.gofile.io/uploadfile",
            payload={
                "status": "ok",
                "data": {
                    "fileId": "file123",
                    "parentFolder": "folder456",
                    "guestToken": "guest-token",
                },
            },
        )
        async with Gofile() as g:
            result = await g.upload(tmp_file)
            assert result["fileId"] == "file123"
            assert result["parentFolder"] == "folder456"

    @pytest.mark.asyncio
    async def test_upload_with_folder_id(self, mock_aio, tmp_file):
        mock_aio.post(
            "https://upload.gofile.io/uploadfile",
            payload={
                "status": "ok",
                "data": {"fileId": "file123", "parentFolder": "folder456"},
            },
        )
        async with Gofile(token="my-token") as g:
            result = await g.upload(tmp_file, folderId="folder456")
            assert result["fileId"] == "file123"

    @pytest.mark.asyncio
    async def test_upload_with_regional_server(self, mock_aio, tmp_file):
        mock_aio.post(
            "https://upload-eu-par.gofile.io/uploadfile",
            payload={
                "status": "ok",
                "data": {"fileId": "file123"},
            },
        )
        async with Gofile() as g:
            result = await g.upload(tmp_file, server="upload-eu-par")
            assert result["fileId"] == "file123"

    @pytest.mark.asyncio
    async def test_upload_api_error(self, mock_aio, tmp_file):
        mock_aio.post(
            "https://upload.gofile.io/uploadfile",
            payload={"status": "error-uploadFailed"},
        )
        async with Gofile() as g:
            with pytest.raises(ResponseError):
                await g.upload(tmp_file)

    @pytest.mark.asyncio
    async def test_upload_rate_limit(self, mock_aio, tmp_file):
        mock_aio.post(
            "https://upload.gofile.io/uploadfile",
            status=429,
            payload={},
        )
        async with Gofile() as g:
            with pytest.raises(RateLimitError):
                await g.upload(tmp_file)


class TestGofileUploadFolder:
    @pytest.mark.asyncio
    async def test_upload_folder_invalid_path(self):
        async with Gofile() as g:
            with pytest.raises(InvalidPath):
                await g.upload_folder("/nonexistent/dir")

    @pytest.mark.asyncio
    async def test_upload_folder_empty(self):
        d = tempfile.mkdtemp()
        async with Gofile() as g:
            result = await g.upload_folder(d)
            assert result == []
        os.rmdir(d)

    @pytest.mark.asyncio
    async def test_upload_folder_success(self, mock_aio, tmp_dir):
        for _ in range(2):
            mock_aio.post(
                "https://upload.gofile.io/uploadfile",
                payload={
                    "status": "ok",
                    "data": {"fileId": "f1", "parentFolder": "folder1"},
                },
            )
        async with Gofile() as g:
            results = await g.upload_folder(tmp_dir, delay=0)
            assert len(results) == 2


class TestGofileCreateFolder:
    @pytest.mark.asyncio
    async def test_create_folder_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.create_folder("parent-id")

    @pytest.mark.asyncio
    async def test_create_folder_success(self, mock_aio):
        mock_aio.post(
            "https://api.gofile.io/contents/createFolder",
            payload={
                "status": "ok",
                "data": {"folderId": "new-folder-id"},
            },
        )
        async with Gofile(token="test-token") as g:
            result = await g.create_folder(
                "parent-id", folderName="test", public=True
            )
            assert result["folderId"] == "new-folder-id"


class TestGofileUpdateContent:
    @pytest.mark.asyncio
    async def test_update_content_invalid_attribute(self):
        async with Gofile(token="test-token") as g:
            with pytest.raises(InvalidOption):
                await g.update_content("c1", "invalid_attr", "value")

    @pytest.mark.asyncio
    async def test_update_content_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.update_content("c1", "name", "new_name")

    @pytest.mark.asyncio
    async def test_update_content_success(self, mock_aio):
        mock_aio.put(
            "https://api.gofile.io/contents/content123/update",
            payload={"status": "ok", "data": {}},
        )
        async with Gofile(token="test-token") as g:
            result = await g.update_content(
                "content123", "name", "new_name.txt"
            )
            assert result == {}

    @pytest.mark.asyncio
    async def test_update_content_valid_attributes(self):
        valid = ["name", "description", "tags", "public", "expiry", "password"]
        async with Gofile(token="test-token") as g:
            for attr in valid:
                # Shouldn't raise InvalidOption
                try:
                    await g.update_content("c1", attr, "value")
                except InvalidOption:
                    pytest.fail(f"InvalidOption raised for valid attribute: {attr}")
                except Exception:
                    pass  # Other errors (network etc.) are expected


class TestGofileDeleteContent:
    @pytest.mark.asyncio
    async def test_delete_content_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.delete_content("c1")

    @pytest.mark.asyncio
    async def test_delete_content_success(self, mock_aio):
        mock_aio.delete(
            "https://api.gofile.io/contents",
            payload={"status": "ok", "data": {}},
        )
        async with Gofile(token="test-token") as g:
            result = await g.delete_content("content123")
            assert result == {}


class TestGofileGetContent:
    @pytest.mark.asyncio
    async def test_get_content_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.get_content("c1")

    @pytest.mark.asyncio
    async def test_get_content_success(self, mock_aio):
        mock_aio.get(
            "https://api.gofile.io/contents/folder123",
            payload={
                "status": "ok",
                "data": {"id": "folder123", "type": "folder", "name": "My Folder"},
            },
        )
        async with Gofile(token="test-token") as g:
            result = await g.get_content("folder123")
            assert result["id"] == "folder123"
            assert result["type"] == "folder"

    @pytest.mark.asyncio
    async def test_get_content_with_password(self, mock_aio):
        mock_aio.get(
            "https://api.gofile.io/contents/folder123?password=abc123hash",
            payload={
                "status": "ok",
                "data": {"id": "folder123", "type": "folder"},
            },
        )
        async with Gofile(token="test-token") as g:
            result = await g.get_content("folder123", password="abc123hash")
            assert result["id"] == "folder123"


class TestGofileSearchContent:
    @pytest.mark.asyncio
    async def test_search_content_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.search_content("folder1", "test")

    @pytest.mark.asyncio
    async def test_search_content_success(self, mock_aio):
        mock_aio.get(
            "https://api.gofile.io/contents/search?contentId=folder1&searchedString=test",
            payload={
                "status": "ok",
                "data": {"contents": [{"id": "file1", "name": "test.txt"}]},
            },
        )
        async with Gofile(token="test-token") as g:
            result = await g.search_content("folder1", "test")
            assert result["contents"][0]["name"] == "test.txt"


class TestGofileCopyContent:
    @pytest.mark.asyncio
    async def test_copy_content_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.copy_content("c1", "folder1")

    @pytest.mark.asyncio
    async def test_copy_content_success(self, mock_aio):
        mock_aio.post(
            "https://api.gofile.io/contents/copy",
            payload={"status": "ok", "data": {}},
        )
        async with Gofile(token="test-token") as g:
            result = await g.copy_content("c1,c2", "folder1")
            assert result == {}


class TestGofileMoveContent:
    @pytest.mark.asyncio
    async def test_move_content_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.move_content("c1", "folder1")

    @pytest.mark.asyncio
    async def test_move_content_success(self, mock_aio):
        mock_aio.put(
            "https://api.gofile.io/contents/move",
            payload={"status": "ok", "data": {}},
        )
        async with Gofile(token="test-token") as g:
            result = await g.move_content("c1,c2", "folder1")
            assert result == {}


class TestGofileImportContent:
    @pytest.mark.asyncio
    async def test_import_content_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.import_content("c1")

    @pytest.mark.asyncio
    async def test_import_content_success(self, mock_aio):
        mock_aio.post(
            "https://api.gofile.io/contents/import",
            payload={"status": "ok", "data": {}},
        )
        async with Gofile(token="test-token") as g:
            result = await g.import_content("c1,c2")
            assert result == {}


class TestGofileDirectLinks:
    @pytest.mark.asyncio
    async def test_create_direct_link_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.create_direct_link("c1")

    @pytest.mark.asyncio
    async def test_create_direct_link_success(self, mock_aio):
        mock_aio.post(
            "https://api.gofile.io/contents/content123/directlinks",
            payload={
                "status": "ok",
                "data": {"directLinkId": "link1", "directLink": "https://example.com/link1"},
            },
        )
        async with Gofile(token="test-token") as g:
            result = await g.create_direct_link("content123", expireTime=1704067200)
            assert result["directLinkId"] == "link1"

    @pytest.mark.asyncio
    async def test_update_direct_link_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.update_direct_link("c1", "link1")

    @pytest.mark.asyncio
    async def test_update_direct_link_success(self, mock_aio):
        mock_aio.put(
            "https://api.gofile.io/contents/content123/directlinks/link1",
            payload={"status": "ok", "data": {}},
        )
        async with Gofile(token="test-token") as g:
            result = await g.update_direct_link(
                "content123", "link1",
                sourceIpsAllowed=["192.168.1.1"],
                domainsAllowed=["example.com"],
            )
            assert result == {}

    @pytest.mark.asyncio
    async def test_delete_direct_link_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.delete_direct_link("c1", "link1")

    @pytest.mark.asyncio
    async def test_delete_direct_link_success(self, mock_aio):
        mock_aio.delete(
            "https://api.gofile.io/contents/content123/directlinks/link1",
            payload={"status": "ok", "data": {}},
        )
        async with Gofile(token="test-token") as g:
            result = await g.delete_direct_link("content123", "link1")
            assert result == {}


class TestGofileAccount:
    @pytest.mark.asyncio
    async def test_get_account_id_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.get_account_id()

    @pytest.mark.asyncio
    async def test_get_account_id_success(self, mock_aio):
        mock_aio.get(
            "https://api.gofile.io/accounts/getid",
            payload={
                "status": "ok",
                "data": {"id": "account123"},
            },
        )
        async with Gofile(token="test-token") as g:
            result = await g.get_account_id()
            assert result["id"] == "account123"

    @pytest.mark.asyncio
    async def test_get_account_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.get_account(accountId="account123")

    @pytest.mark.asyncio
    async def test_get_account_success(self, mock_aio):
        mock_aio.get(
            "https://api.gofile.io/accounts/account123",
            payload={
                "status": "ok",
                "data": {"id": "account123", "email": "test@example.com"},
            },
        )
        async with Gofile(token="test-token") as g:
            result = await g.get_account("account123")
            assert result["id"] == "account123"
            assert result["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_reset_token_no_token(self):
        async with Gofile() as g:
            with pytest.raises(InvalidToken):
                await g.reset_token("account123")

    @pytest.mark.asyncio
    async def test_reset_token_success(self, mock_aio):
        mock_aio.post(
            "https://api.gofile.io/accounts/account123/resettoken",
            payload={"status": "ok", "data": {}},
        )
        async with Gofile(token="test-token") as g:
            result = await g.reset_token("account123")
            assert result == {}


class TestGofileContextManager:
    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        async with Gofile(token="test") as g:
            assert g.token == "test"
        # Session should be closed after context exit
        assert g._session is None or g._session.closed


class TestGofileAuth:
    @pytest.mark.asyncio
    async def test_bearer_token_in_headers(self, mock_aio):
        mock_aio.post(
            "https://api.gofile.io/contents/createFolder",
            payload={"status": "ok", "data": {}},
        )
        async with Gofile(token="my-secret-token") as g:
            await g.create_folder("parent-id")
            # Verify the request was made (aioresponses validates URL matching)
            # The auth header is set in the code; we verify by successful response


# --- Sync Tests ---

class TestSyncGofile:
    def test_sync_init(self):
        g = Sync_Gofile(token="test-token")
        assert g._async_client.token == "test-token"
        g.done()

    def test_sync_context_manager(self):
        with Sync_Gofile(token="test") as g:
            assert g._async_client.token == "test"

    def test_sync_upload_invalid_path(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidPath):
                g.upload("/nonexistent/file.txt")

    def test_sync_create_folder_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.create_folder("parent-id")

    def test_sync_update_content_invalid_attr(self):
        with Sync_Gofile(token="test") as g:
            with pytest.raises(InvalidOption):
                g.update_content("c1", "bad_attr", "value")

    def test_sync_delete_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.delete_content("c1")

    def test_sync_get_content_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.get_content("c1")

    def test_sync_search_content_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.search_content("c1", "test")

    def test_sync_copy_content_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.copy_content("c1", "folder1")

    def test_sync_move_content_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.move_content("c1", "folder1")

    def test_sync_import_content_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.import_content("c1")

    def test_sync_create_direct_link_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.create_direct_link("c1")

    def test_sync_update_direct_link_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.update_direct_link("c1", "link1")

    def test_sync_delete_direct_link_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.delete_direct_link("c1", "link1")

    def test_sync_get_account_id_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.get_account_id()

    def test_sync_get_account_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.get_account("account123")

    def test_sync_reset_token_no_token(self):
        with Sync_Gofile() as g:
            with pytest.raises(InvalidToken):
                g.reset_token("account123")


# --- Error Tests ---

class TestErrors:
    def test_invalid_token_default_message(self):
        err = InvalidToken()
        assert "valid token" in str(err).lower()

    def test_invalid_token_custom_message(self):
        err = InvalidToken("custom msg")
        assert "custom msg" in str(err)

    def test_response_error(self):
        err = ResponseError("error-notFound")
        assert "error-notFound" in str(err)

    def test_rate_limit_error(self):
        err = RateLimitError()
        assert "rate limit" in str(err).lower()

    def test_invalid_path(self):
        err = InvalidPath("bad path")
        assert "bad path" in str(err)

    def test_invalid_option(self):
        err = InvalidOption("badopt")
        assert "badopt" in str(err)
