#!/usr/bin/python3
"""handles all default RESTFul API actions for Place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<string:city_id>/places",
                 methods=["GET"], strict_slashes=False)
def city_places(city_id):
    """Retrives a list of all the places in a city"""

    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)

    the_places = [place.to_dict() for place in the_city.places]

    return (jsonify(the_places), 200)


# _______________________________________________________________________________________

@app_views.route("/places/<string:place_id>", methods=["GET"], strict_slashes=False)
def place_retriever(place_id):
    """Retrieves places based on their id"""

    the_places = storage.get(Place, place_id)
    if the_places is None:
        abort(404)
    return (jsonify(the_places.to_dict()), 200)


# _______________________________________________________________________________________

@app_views.route("/places/<string:place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """deletes a place based on its id"""

    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    the_place.delete()
    storage.save()

    return (jsonify({}), 200)


# _______________________________________________________________________________________

@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """creates a place linked to a city using the city id"""

    req_place = request.get_json()
    if req_place is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)

    user_id = req_place.get("user_id")
    if user_id is None:
        return (jsonify({"error": "Missing user_id"}), 400)

    my_user = storage.get("User", user_id)
    if my_user is None:
        abort(404)

    name = req_place.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new_place = Place()
    new_place.city_id = the_city.id

    for key, val in req_place.items():
        setattr(new_place, key, val)

    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


# _______________________________________________________________________________________

@app_views.route("/places/<place_id>",
                 methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a place based on its id"""

    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)

    req_place = request.get_json()
    if req_place is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    not_allowed = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for k, v in req_place.items():
        if k not in not_allowed:
            setattr(the_place, k, v)
    the_place.save()

    return (jsonify(the_place.to_dict()), 200)
