#!/usr/bin/python3
""" Api v1 entrypoint state route"""
from flask import abort, make_response, request
import json
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"])
def states():
    """return list of states"""
    states = storage.all(State)
    statesList = []

    for key in states:
        statesList.append(states[key].to_dict())

    return make_response(json.dumps(statesList), 200)


@app_views.route("/states/<state_id>", methods=["GET"])
def state_id(state_id):
    """return one state by id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    else:
        return (state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """delete state by id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    state.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route("/states", methods=["POST"])
def post_state():
    """create state by name"""
    name = request.get_json()

    if not name:
        abort(400, description="Not a JSON")

    if 'name' not in name:
        abort(400, description="Missing name")

    state = State(**name)
    state.save()
    return make_response(state.to_dict(), 201)


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_state(state_id):
    """update state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    keys = request.get_json()
    if not keys:
        abort(400, description="Not a JSON")

    for key, value in keys.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(state, key, value)

    state.save()
    return make_response(state.to_dict(), 200)
