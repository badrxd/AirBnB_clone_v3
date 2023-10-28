#!/usr/bin/python3
""" Api v1 entrypoint amenity route"""
from flask import abort, make_response, request
import json
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("amenities", methods=["GET"])
def amenities():
    """return amenities"""
    amenitiesList = []
    amenities = storage.all(Amenity)

    for value in amenities.values():
        obj = value.to_dict()
        amenitiesList.append(obj)
    return make_response(json.dumps(amenitiesList), 200)


@app_views.route("amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """return amenity by id"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    return amenity.to_dict()


@app_views.route("amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """delete amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route("amenities", methods=["POST"])
def post_amenity():
    """create new amenity"""
    data = request.get_json()

    if data is None:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    amenity = Amenity(**data)
    amenity.save()
    return make_response(amenity.to_dict(), 201)


@app_views.route("amenities/<amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """update amenity by id"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    IgnoreKeys = {'id', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in IgnoreKeys:
            setattr(amenity, key, value)
    storage.save()
    return make_response(amenity.to_dict(), 200)
