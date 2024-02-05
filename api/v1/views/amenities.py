#!/usr/bin/python3
"""handles all default RESTFul API actions for Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=["GET"], strict_slashes=False)
@app_views.route('/amenities/<string:am_id>', methods=["GET"],
                 strict_slashes=False)
def amenities(am_id=None):
    """Retrieves a list of all amenities"""

    if am_id is None:
        amenities = [v.to_dict() for v in storage.all(Amenity).values()]
        return jsonify(amenities)

    amenities = storage.get(Amenity, am_id)
    if amenities is None:
        abort(404)

    return jsonify(amenities.to_dict())


# _______________________________________________________________________________________

@app_views.route('/amenities/<string:am_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(am_id):
    """Deletes an amenity based on its id"""

    amenities = storage.get(Amenity, am_id)

    if amenities is None:
        abort(404)

    amenities.delete()
    storage.save()

    return jsonify({})


# _______________________________________________________________________________________

@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates an Amenity"""

    req_amenity = request.get_json()

    if req_amenity is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    name = req_amenity.get("name")

    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new_amenity = Amenity(**req_amenity)
    new_amenity.save()

    return (jsonify(new_amenity.to_dict()), 201)


# _______________________________________________________________________________________

@app_views.route('/amenities/<string:am_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(am_id):
    """Updates an amenity"""

    req_amenity = request.get_json()
    if req_amenity is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    my_amenity = storage.get(Amenity, am_id)
    if my_amenity is None:
        abort(404)

    not_allowed = ["id", "created_at", "updated_at"]
    for k, v in req_amenity.items():
        if k not in not_allowed:
            setattr(my_amenity, k, v)

    my_amenity.save()
    return jsonify(my_amenity.to_dict())
