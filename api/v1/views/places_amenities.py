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
