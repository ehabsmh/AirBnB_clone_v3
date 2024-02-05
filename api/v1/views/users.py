#!/usr/bin/python3
"""View for User objects that handles all default RESTful API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from models.user import User


@app_views.route('/users', strict_slashes=False,
                 methods=['GET'])
def get_users():
    """Gets users"""

    users = storage.all(User)

    # Convert each city object to dictionary
    users = [user.to_dict() for user in users]

    return jsonify(users)


# _______________________________________________________________________________________

@app_views.route('/users/<string:user_id>', strict_slashes=False,
                 methods=['GET'])
def get_user_by_id(user_id):
    """Gets user by id"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


# _______________________________________________________________________________________

@app_views.route('/users/<string:user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """Deletes user by id"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({})


# _______________________________________________________________________________________

@app_views.route('/users', strict_slashes=False,
                 methods=['POST'])
def create_user(user_id):
    """Creates a user"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    requested_user = request.get_json()

    if not requested_user:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'email' not in requested_user:
        return make_response(jsonify({"error": "Missing email"}), 400)

    if 'password' not in requested_user:
        return make_response(jsonify({"error": "Missing password"}), 400)

    user = user(**requested_user)
    user.save()

    return jsonify(user.to_dict()), 201


# _______________________________________________________________________________________

# @app_views.route('/cities/<string:city_id>', strict_slashes=False,
#                  methods=['PUT'])
# def update_city(city_id):
#     """Updates a city by id"""
#     city = storage.get(City, city_id)

#     if not city:
#         abort(404)

#     requested_city = request.get_json()

#     if not requested_city:
#         return make_response(jsonify({"error": "Not a JSON"}), 400)

#     ignored_keys = ["id", "state_id", "created_at", "updated_at"]

#     for k, v in requested_city.items():
#         if k in ignored_keys:
#             continue
#         else:
#             setattr(city, k, v)

#     city.save()
#     return jsonify(city.to_dict())
