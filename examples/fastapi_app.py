from fastapi import FastAPI
from invenio_client import InvenioManager

import uvicorn
import socket

sock = socket.socket()
sock.bind(("127.0.0.1", 0))
host, port = sock.getsockname()
sock.close()

INVENIO_HOST = "127.0.0.1"
INVENIO_PORT = 5000

app = FastAPI()
invenio_manager = InvenioManager(
    invenio_host=INVENIO_HOST,
    invenio_port=INVENIO_PORT,
    host=host,
    port=port,
    service_name="FASTAPI_SERVICE",
    is_async=True,
    fetch_registry=True,
)


@app.on_event("startup")
async def on_startup():
    invenio_manager.run()


@app.get("/get_service")
async def get_fastapi_app_uri():
    """Gets an instance's URL"""
    fastapi_service = await invenio_manager.client.get_instance_url("fastapi_service")
    return {"url": fastapi_service}


if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
