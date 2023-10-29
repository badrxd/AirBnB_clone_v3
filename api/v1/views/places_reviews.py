#!/usr/bin/python3
""" Api v1 entrypoint reviews route"""
from flask import abort, make_response, request
import json
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("places/<place_id>/reviews", methods=["GET"])
def reviews(place_id):
    """return reviews"""

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    reviewsList = []
    reviews = storage.all(Review)

    for value in reviews.values():
        obj = value.to_dict()
        if obj.get('place_id') == place_id:
            reviewsList.append(obj)

    return make_response(json.dumps(reviewsList), 200)


@app_views.route("reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """return review by id"""

    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return review.to_dict()


@app_views.route("reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """delete review by id"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route("places/<place_id>/reviews", methods=["POST"])
def post_review(place_id):
    """create new review"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    if 'user_id' not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data.get('user_id'))
    if user is None:
        abort(404)

    if 'text' not in data:
        abort(400, description="Missing text")

    review = Review(place_id=place_id, **data)
    review.save()
    return make_response(review.to_dict(), 201)


@app_views.route("reviews/<review_id>", methods=["PUT"])
def put_review(review_id):
    """update review by id"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    IgnoreKeys = {'id', 'user_id', 'place_id', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in IgnoreKeys:
            setattr(review, key, value)
    storage.save()
    return make_response(review.to_dict(), 200)
