#!/usr/bin/python3
"""This script registers a blueprint"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(error):
    """Closes the storage session"""
    storage.close()


# _______________________________________________________________________________________

@app.errorhandler(404)
def page_not_found(error):
    if type(error).__name__ == "NotFound":
        return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
