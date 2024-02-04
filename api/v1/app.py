#!/usr/bin/python3
"""This script registers a blueprint"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(error):
    """Closes the storage session"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
