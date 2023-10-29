#!/usr/bin/python3
""" Api v1 entrypoint place route"""
from flask import abort, make_response, request
import json
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("cities/<city_id>/places", methods=["GET"])
def places(city_id):
    """return state places"""

    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    placesList = []
    places = storage.all(Place)

    for value in places.values():
        obj = value.to_dict()
        if obj.get('city_id') == city_id:
            placesList.append(obj)

    return make_response(json.dumps(placesList), 200)


@app_views.route("places/<place_id>", methods=["GET"])
def get_place(place_id):
    """return place by id"""

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return place.to_dict()


@app_views.route("places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """delete place by id"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route("cities/<city_id>/places", methods=["POST"])
def post_place(city_id):
    """create new place"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    if 'user_id' not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    if 'name' not in data:
        abort(400, description="Missing name")

    place = Place(city_id=city_id, **data)
    place.save()
    return make_response(place.to_dict(), 201)


@app_views.route("places/<place_id>", methods=["PUT"])
def put_places(place_id):
    """update place by id"""

    place = storage.get(place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    IgnoreKeys = {'id', 'user_id', 'city_id', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in IgnoreKeys:
            setattr(place, key, value)
    storage.save()
    return make_response(place.to_dict(), 200)
