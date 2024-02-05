#!/usr/bin/python3
''' blueprint for state '''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import State


@app_views.route('/states', methods=["GET"], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def state(state_id=None):
    ''' retrieves a list of all states'''
    if state_id is None:
        the_states = [v.to_dict() for v in storage.all("State").values()]
        return jsonify(the_states)

    the_states = storage.get("State", state_id)
    if the_states is not None:
        return jsonify(the_states.to_dict())
    abort(404)


# _______________________________________________________________________________________

@app_views.route('/states/<s_id>', methods=["DELETE"], strict_slashes=False)
def delete_states(s_id):
    '''Deletes an specific state based on its id'''

    the_state = storage.get("State", s_id)
    if the_state is None:
        abort(404)
    storage.delete(the_state)
    storage.save()
    return (jsonify({}))


# _______________________________________________________________________________________

@app_views.route('/states', methods=["POST"], strict_slashes=False)
def post_states():

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

@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def update_states(state_id):
    '''Updates a state'''

    requested_state = request.get_json()
    if requested_state is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    the_state = storage.get("State", state_id)
    if the_state is None:
        abort(404)

    not_allowed = ["id", "created_at", "updated_at"]
    for key, value in requested_state.items():
        if key not in not_allowed:
            setattr(the_state, key, value)

    the_state.save()
    return jsonify(the_state.to_dict())
