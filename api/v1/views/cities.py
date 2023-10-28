#!/usr/bin/python3
""" Api v1 entrypoint city route"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("states/<state_id>/cities", methods=["GET"])
def cities(state_id):
    """return state cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    citiesList = []
    cities = storage.all(City)
    for value in cities.values():
        obj = value.to_dict()
        if obj.get('state_id') == state_id:
            citiesList.append(obj)
    return citiesList


@app_views.route("cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """return city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return city.to_dict()


@app_views.route("cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """delete city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route("states/<state_id>/cities", methods=["POST"])
def post_city(state_id):
    """create new city"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    city = City(state_id=state_id, **data)
    city.save()
    return make_response(city.to_dict(), 201)


@app_views.route("cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """update city by id"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    IgnoreKeys = {'id', 'state_id', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in IgnoreKeys:
            setattr(city, key, value)
    storage.save()
    return make_response(city.to_dict(), 200)
