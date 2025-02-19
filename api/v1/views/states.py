#!/usr/bin/python3
"""handles all default RESTFul API actions for State objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=["GET"], strict_slashes=False)
@app_views.route('/states/<string:state_id>', methods=["GET"],
                 strict_slashes=False)
def state(state_id=None):
    """ retrieves a list of all states"""
    if state_id is None:
        the_states = [value.to_dict()
                      for value in storage.all(State).values()]
        return jsonify(the_states)

    the_states = storage.get(State, state_id)
    if the_states is not None:
        return jsonify(the_states.to_dict())

    abort(404)


# _______________________________________________________________________________________

@app_views.route('/states/<string:s_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_states(s_id):
    """Deletes a specific state based on its id"""

    the_state = storage.get(State, s_id)

    if the_state is None:
        abort(404)

    the_state.delete()
    storage.save()

    return (jsonify({}))


# _______________________________________________________________________________________

@app_views.route('/states', methods=["POST"], strict_slashes=False)
def post_states():
    """Updates a state"""

    requested_state = request.get_json()

    if requested_state is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    name = requested_state.get("name")

    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new_state = State(**requested_state)
    new_state.save()

    return (jsonify(new_state.to_dict()), 201)


# _______________________________________________________________________________________

@app_views.route('/states/<string:state_id>', methods=["PUT"],
                 strict_slashes=False)
def update_states(state_id):
    """Updates a state"""

    the_state = storage.get(State, state_id)

    if the_state is None:
        abort(404)

    requested_state = request.get_json()

    if requested_state is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    not_allowed = ["id", "created_at", "updated_at"]
    for k, v in requested_state.items():
        if k not in not_allowed:
            setattr(the_state, k, v)

    the_state.save()
    return jsonify(the_state.to_dict())
