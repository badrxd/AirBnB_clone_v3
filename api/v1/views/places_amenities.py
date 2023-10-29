#!/usr/bin/python3
""" Api v1 entrypoint places amenity route"""
from flask import abort, make_response, request
import json
from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity

# storage_t = getenv("HBNB_TYPE_STORAGE")


@app_views.route("places/<place_id>/amenities", methods=["GET"])
def get_amenities(place_id):
    """return amenities"""
    amenitiesList = []
    amenities = {}
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if storage_t == 'db':
        amenities = place.amenities

        for value in amenities:
            obj = value.to_dict()
            amenitiesList.append(obj)
    else:
        for id in place.amenity_ids:
            amenity = storage.get(Amenity, id)
            obj = amenity.to_dict()
            amenitiesList.append(obj)

    return make_response(json.dumps(amenitiesList), 200)


@app_views.route("places/<place_id>/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity_1(place_id, amenity_id):
    """delete amenity by id"""

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None or place is None:
        abort(404)

    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()

    return make_response({}, 200)
