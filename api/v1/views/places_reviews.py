#!/usr/bin/python3
"""View for Review objects that handles all default RESTful API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<string:place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews_place(place_id):
    """Gets reviews of a place"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = place.reviews

    # Convert each review object to dictionary
    reviews = [review.to_dict() for review in reviews]

    return jsonify(reviews)


# _______________________________________________________________________________________

@app_views.route('/reviews/<string:review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review(review_id):
    """Gets a review by id"""

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


# _______________________________________________________________________________________

@app_views.route('/reviews/<string:review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object by id"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({})


# _______________________________________________________________________________________

@app_views.route('/places/<string:place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """Creates a review on a place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    requested_review = request.get_json()

    if not requested_review:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'user_id' not in requested_review:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    
    if 'text' not in requested_review:
        return make_response(jsonify({"error": "Missing text"}), 400)
    
    users = storage.all(User)
    user_id = requested_review.get("user_id")
    user_key = f"{User.__name__}.{user_id}"
    
    if user_key not in users:
        abort(404)

    review = Review(**requested_review)
    review.save()

    return jsonify(review.to_dict()), 201


# _______________________________________________________________________________________

@app_views.route('/reviews/<string:review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """Updates a review by id"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    requested_review = request.get_json()

    if not requested_review:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignored_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]

    for k, v in requested_review.items():
        if k in ignored_keys:
            continue
        else:
            setattr(review, k, v)

    review.save()

    return jsonify(review.to_dict())
