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

from typing import Union
from .client import AsyncClient, Client


class InvenioManager:
    def __init__(
        self,
        invenio_host: str,
        invenio_port: int,
        host: str,
        port: int,
        service_name: str,
        is_async: bool = False,
    ):
        """Main class for all Invenio functionality"""
        self._server_host = invenio_host
        self._server_port = invenio_port
        self._host = host
        self._port = port
        self._service_name = service_name
        self._client = None
        self.is_async = is_async

    def _set_client(self):
        if self.is_async:
            self._client = AsyncClient(self)
        else:
            self._client = Client(self)

    @property
    def client(self) -> Union[Client, AsyncClient]:
        """Returns the used Inventio client instance"""
        if not self._client:
            self._set_client()

        return self._client

    def run(self):
        """Registers itself by connecting to an Invenio server. Not required if you don't want to register the instance

        Only set `is_async` to `True` if your application library is asynchronous. Defaults to `False`
        """
        self.client._start()
