#!/usr/bin/python3
""" Api v1 entrypoint place route"""
from flask import abort, make_response, request
import json
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State


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
def put_place(place_id):
    """update place by id"""

    place = storage.get(Place, place_id)
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


@app_views.route("places_search", methods=["POST"])
def post_places_search():
    """search for all wanted places"""
    placesList = []
    filterList = []
    places = {}
    data = request.get_json()

    if data is None:
        abort(400, description="Not a JSON")
    if len(data) == 0 or (len(data.get('states')) == 0 and
                          len(data.get('cities')) == 0):
        places = storage.all(Place)
        placesList = list(places.values())

    else:
        if 'states' in data.keys():
            for id in data.get('states'):
                state = storage.get(State, id)
                if state != None:
                    for city in state.cities:
                        for place in city.places:
                            if place not in placesList:
                                placesList.append(place)

        if 'cities' in data.keys():
            for id in data.get('cities'):
                city = storage.get(City, id)
                if city != None:
                    for place in city.places:
                        if place not in placesList:
                            placesList.append(place)

    if 'amenities' in data.keys() and data.get('amenities') != []:
        for place in placesList:
            for amenity in place.amenities:
                if amenity.id in data['amenities']:
                    obj = place.to_dict()
                    obj.pop('amenities', None)
                    filterList.append(obj)
                    break
    else:
        for place in placesList:
            obj = place.to_dict()
            if obj.get('amenities'):
                obj.pop('amenities', None)
            filterList.append(obj)

    return make_response(json.dumps(filterList), 200)
