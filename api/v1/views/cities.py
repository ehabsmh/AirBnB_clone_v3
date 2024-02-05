#!/usr/bin/python3
"""View for City objects that handles all default RESTful API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities_by_state(state_id):
    """Gets cities by state id"""
    
    # Get all objects of State class
    states = storage.all(State)

    cities = []
    for v in states.values():
        if v.id == state_id:
            cities = v.cities
    
    cities = [ city.to_dict() for city in cities ]
    
    print(cities)
    return jsonify(cities)


# @app_views.route('/states', strict_slashes=False)
# def cities_by_state():
#     """Gets cities by state id"""
#     states = storage.all(State)
#     for k, v in states.items():
#         states[k] = v.to_dict()
#     return jsonify({"states": states})


# california: 421a55f4-7d82-47d9-b54c-a76916479547
