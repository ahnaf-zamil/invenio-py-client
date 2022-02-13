from flask import Flask
from invenio_client import InvenioManager
import socket

sock = socket.socket()
sock.bind(("127.0.0.1", 0))
host, port = sock.getsockname()
sock.close()

INVENIO_HOST = "127.0.0.1"
INVENIO_PORT = 5000

app = Flask(__name__)
invenio_manager = InvenioManager(
    invenio_host=INVENIO_HOST,
    invenio_port=INVENIO_PORT,
    host=host,
    port=port,
    service_name="FLASK_SERVICE",
)


@app.route("/get_service")
def get_flask_app_uri():
    """Gets an instance's URL"""
    flask_service = invenio_manager.client.get_instance("flask_service")
    return {"url": flask_service}


if __name__ == "__main__":
    invenio_manager.run()
    app.run(host=host, port=port)
