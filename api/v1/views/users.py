#!/usr/bin/python3
""" Api v1 entrypoint user route"""
from flask import abort, make_response, request
import json
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("users", methods=["GET"])
def users():
    """return users"""
    usersList = []
    users = storage.all(User)

    for value in users.values():
        obj = value.to_dict()
        usersList.append(obj)

    return make_response(json.dumps(usersList), 200)


@app_views.route("users/<user_id>", methods=["GET"])
def get_user(user_id):
    """return user by id"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    return user.to_dict()


@app_views.route("users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """delete user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route("users", methods=["POST"])
def post_user():
    """create new user"""
    data = request.get_json()

    if data is None:
        abort(400, description="Not a JSON")

    if 'email' not in data:
        abort(400, description="Missing email")

    if 'password' not in data:
        abort(400, description="Missing password")

    user = User(**data)
    user.save()
    return make_response(user.to_dict(), 201)


@app_views.route("users/<user_id>", methods=["PUT"])
def put_user(user_id):
    """update user by id"""

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    IgnoreKeys = {'id', 'email', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in IgnoreKeys:
            setattr(user, key, value)
    storage.save()
    return make_response(user.to_dict(), 200)
