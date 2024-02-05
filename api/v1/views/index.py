#!/usr/bin/python3
"""This script runs RESTful API's routes"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    pass
