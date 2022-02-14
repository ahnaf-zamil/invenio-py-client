# Copyright 2022 DevGuyAhnaf
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import Optional
from invenio_client.cache import RegistryCache
from .sync import Client

import socketio
import asyncio
import aiohttp
import zlib
import json


class AsyncClient(Client):
    def __init__(self, invenio_manager):
        self.invenio_manager = invenio_manager
        self.sio = socketio.AsyncClient(reconnection=True)
        self.loop: Optional[asyncio.AbstractEventLoop] = asyncio.get_event_loop()
        self._session: Optional[aiohttp.ClientSession] = None
        self._cache: Optional[RegistryCache] = None
        self.host, self.port = (
            self.invenio_manager._server_host,
            self.invenio_manager._server_port,
        )

        if self.invenio_manager.fetch_registry:
            self._cache = RegistryCache()
            self.loop.create_task(self._fetch_registry())

    async def _check_session(self):
        if not self._session:
            self._session = aiohttp.ClientSession(raise_for_status=True)

    async def _run_forever(self):
        await self.sio.connect(
            url=f"http://{self.invenio_manager._server_host}:{self.invenio_manager._server_port}",
            auth={
                "host": self.invenio_manager._host,
                "port": self.invenio_manager._port,
                "service_name": self.invenio_manager._service_name,
            },
        )
        await self.sio.wait()
        await self._session.close()

    def _start(self):
        self._register_callbacks()
        self.loop.create_task(self._run_forever())

    async def _fetch_registry(self):
        await self._check_session()

        # Sleeping for a few seconds so that application can start
        await asyncio.sleep(5)

        while True:
            resp = await self._session.get(
                f"http://{self.host}:{self.port}/registry/fetch"
            )
            reader = resp.content

            # Reading from StreamResponse
            data = bytearray()
            while True:
                chunk = await reader.read(8)
                if not chunk:
                    break
                data += chunk
            decompressed_str = zlib.decompress(data).decode()
            self._cache.set(json.loads(decompressed_str)["services"])

            await asyncio.sleep(30)

    async def get_instance_url(self, service_name: str) -> str:
        """Returns the URL of a load balanced service instance (this method is async)

        Format: `host:port` (e.g `192.11.0.34:5000`)
        """
        await self._check_session()

        cached_service = self._cache.get(service_name)

        if cached_service:
            # If cache exists, load balancing and returning
            if cached_service._last_instance_index == len(cached_service.instances):
                cached_service._last_instance_index = 0

            instance = cached_service.instances[cached_service._last_instance_index]
            cached_service._last_instance_index += 1

            return f"{instance.host}:{instance.port}"

        # If cache does not exist, fetching
        resp = await self._session.get(
            f"http://{self.host}:{self.port}/service/{service_name}/instance"
        )
        return await resp.text()
