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

import socketio
import threading
import requests


class Client:
    def __init__(self, invenio_manager):
        self.invenio_manager = invenio_manager
        self.sio = socketio.Client(reconnection=True)

    def _register_callbacks(self):
        @self.sio.on("connect")
        def on_connection():
            print(
                f"Connected to Invenio on {self.invenio_manager._server_host}:{self.invenio_manager._server_port}"
            )

        @self.sio.on("disconnect")
        def on_disconnect():
            print("Disconnected from Invenio")

    def _run_forever(self):
        self.sio.connect(
            url=f"http://{self.invenio_manager._server_host}:{self.invenio_manager._server_port}",
            auth={
                "host": self.invenio_manager._host,
                "port": self.invenio_manager._port,
                "service_name": self.invenio_manager._service_name,
            }
        )
        self.sio.wait()

    def _start(self):
        self._register_callbacks()
        client_thread = threading.Thread(
            target=self._run_forever, name="Invenio Client", daemon=True
        )
        client_thread.start()

    def get_instance(self, service_name: str):
        """Returns the URL of a load balanced service instance

        Format: `host:port` (e.g `192.11.0.34:5000`)
        """
        host, port = self.invenio_manager._server_host, self.invenio_manager._server_port
        resp = requests.get(
            f"http://{host}:{port}/service/{service_name}/instance"
        )
        resp.raise_for_status()
        return resp.text
