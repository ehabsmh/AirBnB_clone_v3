#!/usr/bin/python3
"""View for City objects that handles all default RESTful API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def cities_by_state(state_id):
    """Gets cities of a state by state id"""

    state = storage.get(State, state_id)

    # Check if no state object has key of `state_key`
    if not state:
        abort(404)

    cities = state.cities

    # Convert each city object to dictionary
    cities = [city.to_dict() for city in cities]

    return jsonify(cities)


# _______________________________________________________________________________________

@app_views.route('/cities/<string:city_id>', strict_slashes=False,
                 methods=['GET'])
def city_by_id(city_id):
    """Gets city by id"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


# _______________________________________________________________________________________

@app_views.route('/cities/<string:city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Deletes city by id"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    city.delete()
    storage.save()

    return jsonify({})


# _______________________________________________________________________________________

@app_views.route('/states/<string:state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """Creates a city for a state by id"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    requested_city = request.get_json()

    if not requested_city:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in requested_city:
        return make_response(jsonify({"error": "Missing name"}), 400)

    requested_city['state_id'] = state_id
    city = City(**requested_city)
    city.save()

    return jsonify(city.to_dict()), 201


# _______________________________________________________________________________________

@app_views.route('/cities/<string:city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    """Updates a city by id"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    requested_city = request.get_json()

    if not requested_city:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignored_keys = ["id", "state_id", "created_at", "updated_at"]

    for k, v in requested_city.items():
        if k in ignored_keys:
            continue
        else:
            setattr(city, k, v)

    city.save()
    return jsonify(city.to_dict())
