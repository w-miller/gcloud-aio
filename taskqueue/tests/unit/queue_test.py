from typing import Optional

import pytest
from gcloud.aio.taskqueue import PushQueue


def test_importable():
    assert True


# =========
# client
# =========

class _MockToken:
    @staticmethod
    async def get() -> Optional[str]:
        return 'Unit-Test-Bearer-Token'


@pytest.mark.asyncio
async def test_client_api_is_dev():
    """
    Test that the api_is_dev constructor parameter controls whether the
    Authorization header is set on requests
    """
    api_root = 'https://foobar/v1'

    # With no API root specified, assume API not dev, so auth header should be
    # set
    async with PushQueue('foo', 'bar', token=_MockToken()) as queue:
        assert 'Authorization' in await queue.headers()
    # If API root set and not otherwise specified, assume API is dev, so auth
    # header should not be set
    async with PushQueue(
            'foo', 'bar', api_root=api_root, token=_MockToken(),
    ) as queue:
        assert 'Authorization' not in await queue.headers()
    # If API specified to be dev, auth header should not be set
    async with PushQueue(
            'foo', 'bar', api_root=api_root, api_is_dev=True,
            token=_MockToken(),
    ) as queue:
        assert 'Authorization' not in await queue.headers()
    # If API specified to not be dev, auth header should be set
    async with PushQueue(
            'foo', 'bar', api_root=api_root, api_is_dev=False,
            token=_MockToken(),
    ) as queue:
        assert 'Authorization' in await queue.headers()
